from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import pandas as pd
import pickle
import PyPDF2
import re
import os
from feature_engineer import extract_features

app = Flask(__name__)
CORS(app)

with open('models/xgb_model.pkl', 'rb') as f: model = pickle.load(f)
jobs_df = pd.read_csv('datasets/jobs.csv').drop_duplicates(subset=['job_id'])

# Used for Regex matching in the resume parser
KNOWN_SKILLS = ['A/B Testing', 'API Gateway', 'API Integration', 'ARCore', 'ARKit', 'ARM Templates', 'AWS', 'Ajax', 'Android Development', 'Angular', 'Ansible', 'Apache', 'App Engine', 'Application Security', 'Azure', 'Azure Functions', 'Babel', 'Bash', 'Big Data', 'BigQuery', 'Bitcoin', 'Blockchain', 'Bluetooth', 'Bootstrap', 'C#', 'CI/CD', 'Camera Integration', 'Cassandra', 'Chef', 'Chrome DevTools', 'Cloud Functions', 'Cloud Security', 'Cloud SQL', 'Cloud Storage', 'CloudFormation', 'CloudFront', 'CloudWatch', 'Compliance', 'Computer Vision', 'Consensus Algorithms', 'Cordova', 'Core Data', 'Cost Optimization', 'Cryptography', 'Cryptocurrency', 'Cybersecurity', 'Cypress', 'DApps', 'Dart', 'Data Visualization', 'Deep Learning', 'Django', 'Docker', 'DynamoDB', 'EC2', 'ECS', 'EKS', 'ELK Stack', 'ETL', 'Encryption', 'Ethical Hacking', 'Ethereum', 'Express.js', 'FastAPI', 'Feature Engineering', 'Firebase', 'Firewalls', 'Flask', 'Flutter', 'GCP', 'GDPR', 'Git', 'GitHub Actions', 'GitLab CI', 'Go', 'Grafana', 'GraphQL', 'HAProxy', 'HIPAA', 'HTML', 'Hadoop', 'Hardhat', 'Helm', 'Human Interface Guidelines', 'Hyperledger', 'IAM', 'IDS/IPS', 'ISO 27001', 'In-App Purchases', 'Incident Response', 'Ionic', 'JSON', 'JWT', 'Java', 'JavaScript', 'Jenkins', 'Jest', 'Kafka', 'Keras', 'Kotlin', 'Kubernetes', 'Lambda', 'LightGBM', 'Linux', 'Load Balancing', 'MLOps', 'Machine Learning', 'Maps Integration', 'Material Design', 'Matplotlib', 'Microservices', 'MongoDB', 'Monitoring', 'MySQL', 'NFT', 'NLP', 'Nagios', 'Network Security', 'Networking', 'Next.js', 'Nginx', 'Node.js', 'NoSQL', 'NumPy', 'OAuth', 'OWASP', 'Objective-C', 'Oracle', 'PHP', 'PKI', 'Pandas', 'Penetration Testing', 'PostgreSQL', 'Power BI', 'Progressive Web Apps', 'Prometheus', 'Puppet', 'Push Notifications', 'PyTorch', 'Python', 'R', 'RDS', 'REST API', 'RabbitMQ', 'React', 'React Native', 'Realm', 'Redis', 'Redux', 'Reinforcement Learning', 'Remix', 'Responsive Design', 'Route 53', 'Ruby', 'Ruby on Rails', 'Rust', 'S3', 'SAML', 'SASS', 'SIEM', 'SOC 2', 'SOA', 'SQL', 'SQLite', 'SSL/TLS', 'Scala', 'Scikit-learn', 'Seaborn', 'Security', 'Serverless', 'Smart Contracts', 'Solidity', 'Spark', 'Splunk', 'Spring Boot', 'Statistics', 'Swift', 'SwiftUI', 'Tableau', 'Tailwind CSS', 'TensorFlow', 'Terraform', 'Threat Intelligence', 'Time Series', 'Truffle', 'TypeScript', 'UI/UX', 'VPC', 'Vue.js', 'Web3.js', 'WebSockets', 'Webpack', 'XGBoost', 'Xamarin', 'Yarn', 'Zero Trust', 'gRPC', 'jQuery', 'npm']

def get_learning_link(s):
    sl = s.lower()
    if 'aws' in sl or 'cloud' in sl: return 'https://aws.amazon.com/training/'
    if 'python' in sl: return 'https://www.coursera.org/learn/python'
    if 'react' in sl: return 'https://react.dev/learn'
    if 'sql' in sl: return 'https://www.w3schools.com/sql/'
    return f"https://www.youtube.com/results?search_query={s.replace(' ', '+')}+tutorial"

@app.route('/api/parse-resume', methods=['POST'])
def parse_resume():
    if 'resume' not in request.files: return jsonify({'error': 'No file uploaded'}), 400
    file = request.files['resume']
    try:
        reader = PyPDF2.PdfReader(file)
        clean_text = re.sub(r'[^a-zA-Z0-9\s\+\#\.]', ' ', "".join(p.extract_text() for p in reader.pages)).lower()
        skills = [s for s in KNOWN_SKILLS if re.search(r'\b' + re.escape(s.lower()) + r'\b', clean_text)]
        return jsonify({'success': True, 'skills': skills, 'message': f"Extracted {len(skills)} skills."})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/recommend', methods=['POST'])
def recommend():
    data = request.json
    cand_skills = data.get('skills', '')
    
    temp_df = jobs_df.copy()
    temp_df['skills'] = cand_skills
    temp_df['experience_years'] = int(data.get('experience_years', 0))
    temp_df['expected_salary'] = int(data.get('expected_salary', 80000))
    temp_df['preferred_location'] = data.get('preferred_location', 'Remote')

    X_pred = extract_features(temp_df)
    temp_df['selection_probability'] = (model.predict_proba(X_pred)[:, 1] * 100).round(1)
    top_jobs = temp_df.sort_values('selection_probability', ascending=False).head(int(data.get('top_n', 10)))
    
    recommendations = []
    user_skills_set = set([s.strip() for s in cand_skills.split(',')])

    for _, job in top_jobs.iterrows():
        job_skills = set(job['required_skills'].split(', '))
        missing_skills = list(job_skills - user_skills_set)
        
        apply_url = str(job.get('apply_link', '#'))
        if apply_url == 'nan' or apply_url == 'None':
            apply_url = f"https://www.google.com/search?q={job['company']}+careers+{job['title']}"

        recommendations.append({
            'job_id': job['job_id'], 'title': job['title'], 'company': job['company'],
            'location': job['location'], 'experience_level': job['experience_level'],
            'salary_min': int(job['salary_min']), 'salary_max': int(job['salary_max']),
            'required_skills': list(job_skills),
            'matching_skills': list(job_skills.intersection(user_skills_set)),
            'missing_skills': missing_skills,
            'learning_resources': [{'skill': s, 'link': get_learning_link(s)} for s in missing_skills],
            'selection_probability': job['selection_probability'],
            'apply_link': apply_url
        })
    return jsonify({'success': True, 'recommendations': recommendations})

@app.route('/api/stats', methods=['GET'])
def get_stats(): return jsonify({'success': True, 'total_jobs': len(jobs_df), 'total_skills': len(KNOWN_SKILLS)})

@app.route('/', methods=['GET'])
def serve_root():
    return send_from_directory('frontend', 'index.html')

@app.route('/<path:filename>', methods=['GET'])
def serve_frontend(filename):
    return send_from_directory('frontend', filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))