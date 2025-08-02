import pandas as pd
import joblib
import mlflow
import mlflow.xgboost
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, roc_auc_score
import xgboost as xgb
from preprocess import LeadPreprocessor

mlflow.set_tracking_uri("file:///mlruns")

def train_and_log_model():
    with mlflow.start_run():
        df = pd.read_csv('leads_data.csv')
        prep = LeadPreprocessor()
        X = prep.preprocess_features(df)
        y = df['converted']

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )

        params = {
            'objective': 'binary:logistic',
            'max_depth': 6,
            'learning_rate': 0.1,
            'n_estimators': 100,
            'random_state': 42,
            'eval_metric': 'logloss'
        }
        mlflow.log_params(params)

        model = xgb.XGBClassifier(**params)
        model.fit(X_train, y_train)

        y_pred = model.predict(X_test)
        y_proba = model.predict_proba(X_test)[:, 1]

        acc = accuracy_score(y_test, y_pred)
        auc = roc_auc_score(y_test, y_proba)

        mlflow.log_metrics({'accuracy': acc, 'auc': auc})

        # Save model and preprocessor
        joblib.dump(model, 'lead_model.pkl')
        joblib.dump(prep, 'preprocessor.pkl')

        # Log model as artifact with mlflow.xgboost flavor
        mlflow.xgboost.log_model(model, "lead_scoring_model")
        mlflow.log_artifact('lead_model.pkl')
        mlflow.log_artifact('preprocessor.pkl')

        print(f"Accuracy={acc:.3f}, AUC={auc:.3f}")

if __name__ == "__main__":
    train_and_log_model()
