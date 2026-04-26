import pandas as pd
import os
from sklearn.model_selection import train_test_split

def split_data():
    apps = pd.read_csv('datasets/applications.csv')
    train, temp = train_test_split(apps, test_size=0.3, random_state=42, stratify=apps['selected'])
    cv, test = train_test_split(temp, test_size=0.5, random_state=42, stratify=temp['selected'])
    
    for split in ['train', 'cv', 'test']:
        os.makedirs(f'datasets/Splits/{split}', exist_ok=True)
    
    train.to_csv('datasets/Splits/train/applications.csv', index=False)
    cv.to_csv('datasets/Splits/cv/applications.csv', index=False)
    test.to_csv('datasets/Splits/test/applications.csv', index=False)
    
    jobs = pd.read_csv('datasets/jobs.csv')
    cands = pd.read_csv('datasets/candidates.csv')
    for split in ['train', 'cv', 'test']:
        jobs.to_csv(f'datasets/Splits/{split}/jobs.csv', index=False)
        cands.to_csv(f'datasets/Splits/{split}/candidates.csv', index=False)
    print("✓ Data split successfully!")

if __name__ == "__main__":
    split_data()