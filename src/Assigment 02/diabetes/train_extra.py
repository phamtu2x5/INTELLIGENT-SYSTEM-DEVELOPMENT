import pandas as pd
import joblib
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
import os

print("Training extra models for Diabetes...")
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Load Data
df = pd.read_csv(os.path.join(BASE_DIR, 'data', 'diabetes_prediction_dataset.csv'))

# Create interaction features
df['glucose_hba1c_interaction'] = df['blood_glucose_level'] * df['HbA1c_level']
df['age_hypertension_risk'] = df['age'] * df['hypertension']

y = df['diabetes']
X = df.drop('diabetes', axis=1)

# Load preprocessor
prep = joblib.load(os.path.join(BASE_DIR, 'model', 'preprocessor.joblib'))

# Transform
print("Transforming data...")
X_trans = prep.transform(X)

# Train Logistic Regression
print("Training Logistic Regression...")
lr = LogisticRegression(max_iter=1000, random_state=42)
lr.fit(X_trans, y)
joblib.dump(lr, os.path.join(BASE_DIR, 'model', 'model_lr.joblib'))

# Train Random Forest (lighter version for fast inference)
print("Training Random Forest...")
rf = RandomForestClassifier(n_estimators=50, max_depth=10, random_state=42, n_jobs=-1)
rf.fit(X_trans, y)
joblib.dump(rf, os.path.join(BASE_DIR, 'model', 'model_rf.joblib'))

print("Done! Extra models saved.")
