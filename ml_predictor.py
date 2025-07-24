import pandas as pd
from sklearn.ensemble import RandomForestClassifier

def train_model(file_path="historique_courses.csv"):
    df = pd.read_csv(file_path).dropna(subset=["position"])
    df["position"] = df["position"].astype(int)
    df["odds"] = df["odds"].astype(float)
    df["is_winner"] = (df["position"] == 1).astype(int)

    X = df[["odds"]]
    y = df["is_winner"]

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X, y)
    return model

def predict_proba(model, dogs):
    import pandas as pd
    df = pd.DataFrame(dogs)
    df["odds"] = df["odds"].astype(float)
    df["proba"] = model.predict_proba(df[["odds"]])[:, 1]
    return df
