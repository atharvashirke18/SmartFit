import pandas as pd
import numpy as np
import random
import os
from datetime import datetime

np.random.seed(42)
random.seed(42)

skill_pool = {
    'data_science': ['Python', 'R', 'Machine Learning', 'Deep Learning', 'SQL', 'NoSQL', 'Data Visualization', 'Statistics', 'TensorFlow', 'PyTorch', 'Keras', 'Pandas', 'NumPy', 'Scikit-learn', 'Matplotlib', 'Seaborn', 'Tableau', 'Power BI', 'Spark', 'Hadoop', 'ETL', 'Big Data', 'A/B Testing', 'NLP', 'Computer Vision', 'Time Series', 'Reinforcement Learning', 'XGBoost', 'LightGBM', 'Feature Engineering', 'MLOps'],
    'web_dev': ['JavaScript', 'TypeScript', 'React', 'Angular', 'Vue.js', 'Node.js', 'Express.js', 'Next.js', 'HTML', 'CSS', 'SASS', 'Webpack', 'Babel', 'Redux', 'GraphQL', 'REST API', 'Git', 'MongoDB', 'Firebase', 'Responsive Design', 'Bootstrap', 'Tailwind CSS', 'jQuery', 'Ajax', 'WebSockets', 'Progressive Web Apps', 'Chrome DevTools', 'Jest', 'Cypress', 'npm', 'Yarn'],
    'backend': ['Python', 'Java', 'C#', 'Go', 'Rust', 'PHP', 'Ruby', 'Scala', 'Spring Boot', 'Django', 'Flask', 'FastAPI', '.NET', 'Ruby on Rails', 'SQL', 'PostgreSQL', 'MySQL', 'Oracle', 'MongoDB', 'Redis', 'Cassandra', 'Docker', 'Kubernetes', 'AWS', 'Azure', 'GCP', 'Microservices', 'REST API', 'gRPC', 'RabbitMQ', 'Kafka', 'Nginx', 'Apache', 'OAuth', 'JWT', 'WebSockets', 'GraphQL', 'SOA'],
    'mobile': ['React Native', 'Flutter', 'Swift', 'SwiftUI', 'Kotlin', 'Java', 'Objective-C', 'Dart', 'iOS Development', 'Android Development', 'Firebase', 'SQLite', 'Core Data', 'Realm', 'UI/UX', 'Material Design', 'Human Interface Guidelines', 'API Integration', 'Push Notifications', 'In-App Purchases', 'Maps Integration', 'Camera Integration', 'Bluetooth', 'ARKit', 'ARCore', 'Xamarin', 'Ionic', 'Cordova'],
    'devops': ['Docker', 'Kubernetes', 'AWS', 'Azure', 'GCP', 'CI/CD', 'Jenkins', 'GitLab CI', 'GitHub Actions', 'Terraform', 'Ansible', 'Chef', 'Puppet', 'Linux', 'Bash', 'Python', 'Monitoring', 'Prometheus', 'Grafana', 'ELK Stack', 'Splunk', 'Nagios', 'Git', 'Nginx', 'Apache', 'HAProxy', 'Load Balancing', 'Networking', 'Security', 'CloudFormation', 'Helm'],
    'cloud': ['AWS', 'Azure', 'GCP', 'Lambda', 'EC2', 'S3', 'RDS', 'DynamoDB', 'CloudFront', 'API Gateway', 'ECS', 'EKS', 'CloudWatch', 'IAM', 'VPC', 'Route 53', 'Serverless', 'Azure Functions', 'Cloud Functions', 'App Engine', 'BigQuery', 'Cloud Storage', 'Cloud SQL', 'Terraform', 'CloudFormation', 'ARM Templates', 'Cost Optimization'],
    'security': ['Cybersecurity', 'Penetration Testing', 'Ethical Hacking', 'OWASP', 'Firewalls', 'IDS/IPS', 'SIEM', 'Encryption', 'PKI', 'SSL/TLS', 'OAuth', 'SAML', 'Zero Trust', 'Compliance', 'ISO 27001', 'SOC 2', 'GDPR', 'HIPAA', 'Network Security', 'Application Security', 'Cloud Security', 'Incident Response', 'Threat Intelligence'],
    'blockchain': ['Blockchain', 'Ethereum', 'Solidity', 'Smart Contracts', 'Web3.js', 'Hyperledger', 'Bitcoin', 'Cryptocurrency', 'DApps', 'NFT', 'Consensus Algorithms', 'Cryptography', 'Truffle', 'Hardhat', 'Remix']
}

job_titles = {k: [f"{k.replace('_', ' ').title()} Engineer", f"Senior {k.replace('_', ' ').title()} Developer"] for k in skill_pool.keys()}
companies = ['Google', 'Microsoft', 'Amazon', 'Meta', 'Apple', 'Netflix', 'Deloitte', 'PwC', 'Stripe', 'Coinbase']
locations = ['Remote', 'San Francisco, CA', 'New York, NY', 'London, UK', 'Bangalore, India', 'Pune, India']
exp_map = {'Entry Level': 2, 'Mid Level': 5, 'Senior Level': 8, 'Lead': 12, 'Principal': 15}

def generate_correlated_data(n_samples=50000):
    print(f"Generating {n_samples} highly correlated records...")
    os.makedirs('datasets', exist_ok=True)
    jobs, candidates, applications = [], [], []

    for i in range(n_samples):
        category = random.choice(list(skill_pool.keys()))
        job_skills = set(random.sample(skill_pool[category], k=random.randint(5, 10)))
        exp_level = random.choice(list(exp_map.keys()))
        job_exp = exp_map[exp_level]
        job_id = f"JOB{i+1:07d}"
        job_location = random.choice(locations)
        salary_base = job_exp * 15000 + 40000
        
        jobs.append({
            'job_id': job_id, 'title': random.choice(job_titles[category]),
            'company': random.choice(companies), 'location': job_location,
            'experience_level': exp_level, 'required_skills': ', '.join(job_skills),
            'salary_min': salary_base, 'salary_max': salary_base + 50000,
            'category': category, 'apply_link': np.nan # Pre-allocate for JSearch
        })

        cand_id = f"CAND{i+1:07d}"
        is_good_fit = random.random() > 0.5
        
        if is_good_fit:
            cand_skills = set(random.sample(list(job_skills), k=int(len(job_skills)*0.8)))
            cand_skills.update(random.sample(skill_pool[category], k=2))
            cand_exp = max(0, job_exp + random.randint(-2, 3))
            cand_location = job_location if random.random() > 0.3 else 'Remote'
        else:
            cand_skills = set(random.sample(skill_pool[random.choice(list(skill_pool.keys()))], k=6))
            cand_exp = random.randint(0, 15)
            cand_location = random.choice(locations)

        candidates.append({
            'candidate_id': cand_id, 'skills': ', '.join(cand_skills), 
            'experience_years': cand_exp, 'preferred_location': cand_location,
            'expected_salary': (cand_exp * 14000) + 45000
        })

        skill_match = len(job_skills.intersection(cand_skills)) / len(job_skills)
        exp_match = max(0, 1 - (abs(job_exp - cand_exp) / 8))
        loc_match = 1.0 if (job_location == 'Remote' or job_location == cand_location) else 0.5
        
        prob = (skill_match * 0.55) + (exp_match * 0.35) + (loc_match * 0.10)
        selected = 1 if prob > 0.65 else 0
        if random.random() < 0.05: selected = 1 - selected # 5% Noise

        applications.append({'application_id': f"APP{i+1:07d}", 'job_id': job_id, 'candidate_id': cand_id, 'selected': selected})

    pd.DataFrame(jobs).to_csv('datasets/jobs.csv', index=False)
    pd.DataFrame(candidates).to_csv('datasets/candidates.csv', index=False)
    pd.DataFrame(applications).to_csv('datasets/applications.csv', index=False)
    print("✓ Datasets generated!")

if __name__ == "__main__":
    generate_correlated_data()