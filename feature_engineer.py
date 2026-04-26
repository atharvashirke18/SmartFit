import pandas as pd

def extract_features(merged_df):
    features = []
    exp_map = {'Entry Level': 2, 'Mid Level': 5, 'Senior Level': 8, 'Lead': 12, 'Principal': 15}
    
    for _, row in merged_df.iterrows():
        job_skills = set(str(row['required_skills']).split(', ')) if pd.notna(row['required_skills']) else set()
        cand_skills = set(str(row['skills']).split(', ')) if pd.notna(row['skills']) else set()
        
        skill_match_count = len(job_skills.intersection(cand_skills))
        skill_match_ratio = skill_match_count / len(job_skills) if len(job_skills) > 0 else 0
        expected_exp = exp_map.get(row['experience_level'], 5)
        cand_exp = row['experience_years']
        
        feat = {
            'skill_match_ratio': skill_match_ratio,
            'skill_match_count': skill_match_count,
            'exp_diff': cand_exp - expected_exp,
            'cand_exp': cand_exp,
            'salary_fit': 1 if row['salary_min'] <= row['expected_salary'] <= row['salary_max'] else 0,
            'loc_match': 1 if (row['location'] == 'Remote' or row['location'] == row['preferred_location']) else 0
        }
        if 'selected' in row: feat['selected'] = row['selected']
        features.append(feat)
    return pd.DataFrame(features)

def load_and_merge(split='train'):
    apps = pd.read_csv(f'datasets/Splits/{split}/applications.csv')
    jobs = pd.read_csv(f'datasets/Splits/{split}/jobs.csv')
    cands = pd.read_csv(f'datasets/Splits/{split}/candidates.csv')
    merged = apps.merge(jobs, on='job_id', how='left').merge(cands, on='candidate_id', how='left')
    return extract_features(merged)