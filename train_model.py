import xgboost as xgb
import pickle
import os
from feature_engineer import load_and_merge

def train():
    train_df = load_and_merge('train')
    cv_df = load_and_merge('cv')
    
    X_train, y_train = train_df.drop('selected', axis=1), train_df['selected']
    X_cv, y_cv = cv_df.drop('selected', axis=1), cv_df['selected']
    
    model = xgb.XGBClassifier(
        n_estimators=150, max_depth=5, learning_rate=0.05, eval_metric='auc',
        early_stopping_rounds=20, scale_pos_weight=len(y_train[y_train==0])/len(y_train[y_train==1]),
        random_state=42
    )
    model.fit(X_train, y_train, eval_set=[(X_cv, y_cv)], verbose=10)
    
    os.makedirs('models', exist_ok=True)
    with open('models/xgb_model.pkl', 'wb') as f: pickle.dump(model, f)
    print("✓ Model saved!")

if __name__ == "__main__":
    train()