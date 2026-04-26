import requests
import pandas as pd
import os
import random

RAPID_API_KEY = "787346fa82msh59175c4c94095eep1e862djsnc451ce6df17e"

KNOWN_SKILLS = ['A/B Testing', 'API Gateway', 'API Integration', 'ARCore', 'ARKit', 'ARM Templates', 'AWS', 'Ajax', 'Android Development', 'Angular', 'Ansible', 'Apache', 'App Engine', 'Application Security', 'Azure', 'Azure Functions', 'Babel', 'Bash', 'Big Data', 'BigQuery', 'Bitcoin', 'Blockchain', 'Bluetooth', 'Bootstrap', 'C#', 'CI/CD', 'Camera Integration', 'Cassandra', 'Chef', 'Chrome DevTools', 'Cloud Functions', 'Cloud Security', 'Cloud SQL', 'Cloud Storage', 'CloudFormation', 'CloudFront', 'CloudWatch', 'Compliance', 'Computer Vision', 'Consensus Algorithms', 'Cordova', 'Core Data', 'Cost Optimization', 'Cryptography', 'Cryptocurrency', 'Cybersecurity', 'Cypress', 'DApps', 'Dart', 'Data Visualization', 'Deep Learning', 'Django', 'Docker', 'DynamoDB', 'EC2', 'ECS', 'EKS', 'ELK Stack', 'ETL', 'Encryption', 'Ethical Hacking', 'Ethereum', 'Express.js', 'FastAPI', 'Feature Engineering', 'Firebase', 'Firewalls', 'Flask', 'Flutter', 'GCP', 'GDPR', 'Git', 'GitHub Actions', 'GitLab CI', 'Go', 'Grafana', 'GraphQL', 'HAProxy', 'HIPAA', 'HTML', 'Hadoop', 'Hardhat', 'Helm', 'Human Interface Guidelines', 'Hyperledger', 'IAM', 'IDS/IPS', 'ISO 27001', 'In-App Purchases', 'Incident Response', 'Ionic', 'JSON', 'JWT', 'Java', 'JavaScript', 'Jenkins', 'Jest', 'Kafka', 'Keras', 'Kotlin', 'Kubernetes', 'Lambda', 'LightGBM', 'Linux', 'Load Balancing', 'MLOps', 'Machine Learning', 'Maps Integration', 'Material Design', 'Matplotlib', 'Microservices', 'MongoDB', 'Monitoring', 'MySQL', 'NFT', 'NLP', 'Nagios', 'Network Security', 'Networking', 'Next.js', 'Nginx', 'Node.js', 'NoSQL', 'NumPy', 'OAuth', 'OWASP', 'Objective-C', 'Oracle', 'PHP', 'PKI', 'Pandas', 'Penetration Testing', 'PostgreSQL', 'Power BI', 'Progressive Web Apps', 'Prometheus', 'Puppet', 'Push Notifications', 'PyTorch', 'Python', 'R', 'RDS', 'REST API', 'RabbitMQ', 'React', 'React Native', 'Realm', 'Redis', 'Redux', 'Reinforcement Learning', 'Remix', 'Responsive Design', 'Route 53', 'Ruby', 'Ruby on Rails', 'Rust', 'S3', 'SAML', 'SASS', 'SIEM', 'SOC 2', 'SOA', 'SQL', 'SQLite', 'SSL/TLS', 'Scala', 'Scikit-learn', 'Seaborn', 'Security', 'Serverless', 'Smart Contracts', 'Solidity', 'Spark', 'Splunk', 'Spring Boot', 'Statistics', 'Swift', 'SwiftUI', 'Tableau', 'Tailwind CSS', 'TensorFlow', 'Terraform', 'Threat Intelligence', 'Time Series', 'Truffle', 'TypeScript', 'UI/UX', 'VPC', 'Vue.js', 'Web3.js', 'WebSockets', 'Webpack', 'XGBoost', 'Xamarin', 'Yarn', 'Zero Trust', 'gRPC', 'jQuery', 'npm']

def fetch_live_jobs(query="Software Engineer"):
    url = "https://jsearch.p.rapidapi.com/search"
    headers = {"X-RapidAPI-Key": RAPID_API_KEY, "X-RapidAPI-Host": "jsearch.p.rapidapi.com"}
    response = requests.get(url, headers=headers, params={"query": query, "page": "1", "num_pages": "1"})
    
    if response.status_code != 200: return print("API Error")
    new_jobs = []
    for job in response.json().get('data', []):
        desc = job.get('job_description', '').lower()
        skills = [s for s in KNOWN_SKILLS if s.lower() in desc]
        if len(skills) < 2: continue
        
        new_jobs.append({
            'job_id': f"LIVE_{job.get('job_id', str(random.randint(10000,99999)))}",
            'title': job.get('job_title', ''), 'company': job.get('employer_name', 'Unknown'),
            'location': f"{job.get('job_city', '')}, {job.get('job_country', '')}".strip(', '),
            'experience_level': 'Mid Level' if 'mid' in desc else 'Entry Level',
            'required_skills': ', '.join(skills),
            'salary_min': job.get('job_min_salary') or 60000,
            'salary_max': job.get('job_max_salary') or 120000,
            'category': 'web_dev',
            'apply_link': job.get('job_apply_link', '#')
        })
    
    if new_jobs:
        existing = pd.read_csv('datasets/jobs.csv')
        combined = pd.concat([pd.DataFrame(new_jobs), existing]).drop_duplicates(subset=['title', 'company'])
        combined.to_csv('datasets/jobs.csv', index=False)
        print(f"✓ Added live jobs to dataset!")

if __name__ == "__main__":
    fetch_live_jobs("Software Engineer")