import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

def evaluate_model(file_path="historique_courses.csv"):
    df = pd.read_csv(file_path).dropna(subset=["position"])
    df["is_winner"] = (df["position"] == 1).astype(int)

    X = df[["odds"]]
    y = df["is_winner"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    print("=== Évaluation du modèle ===")
    print(classification_report(y_test, y_pred))

if __name__ == "__main__":
    evaluate_model()
