from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
import pandas as pd
import joblib

def train_model(data, model_type='random_forest'):
    """
    Trains a model of the specified type on the given data.
    """
    df = pd.DataFrame(data)
    # One-hot encode categorical features
    df = pd.get_dummies(df, drop_first=True)
    
    # Ensure 'target' column exists after encoding, if not, something is wrong with data prep
    if 'target' not in df.columns:
        raise ValueError("Target column is not in the dataframe after encoding")

    X = df.drop("target", axis=1)
    y = df["target"]
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    if model_type == 'random_forest':
        model = RandomForestClassifier(n_estimators=100, random_state=42)
    elif model_type == 'logistic_regression':
        model = LogisticRegression(random_state=42)
    else:
        raise ValueError("Invalid model type specified")
        
    model.fit(X_train, y_train)
    
    joblib.dump(model, 'model.pkl')
    joblib.dump(list(X.columns), 'model_columns.pkl') # Save column names
    return model.score(X_test, y_test)

def predict(data):
    """
    Makes predictions on the given data using the trained model.
    """
    model = joblib.load('model.pkl')
    train_cols = joblib.load('model_columns.pkl')
    df = pd.DataFrame(data, index=[0])
    # One-hot encode the new data just like the training data.
    df = pd.get_dummies(df)
    # Align columns
    df = df.reindex(columns=train_cols, fill_value=0)

    return model.predict(df)[0]
