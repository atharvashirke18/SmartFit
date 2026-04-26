import pickle
from sklearn.metrics import accuracy_score, roc_auc_score, classification_report
from feature_engineer import load_and_merge

def evaluate():
    test_df = load_and_merge('test')
    X_test, y_test = test_df.drop('selected', axis=1), test_df['selected']
    
    with open('models/xgb_model.pkl', 'rb') as f: model = pickle.load(f)
    
    y_pred = model.predict(X_test)
    print(f"Accuracy: {accuracy_score(y_test, y_pred):.4f}")
    print(f"ROC AUC:  {roc_auc_score(y_test, model.predict_proba(X_test)[:, 1]):.4f}")
    print(classification_report(y_test, y_pred))

if __name__ == "__main__":
    evaluate()