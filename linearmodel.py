import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import matplotlib.pyplot as plt
import numpy as np
import tkintertest as tktest


# ============================================================
# LOAD DATA
# ============================================================
def load_data(file_path):
    df = pd.read_excel(file_path)
    X = df.iloc[:, 8:29]     # SOE + U1–U21
    y = df["SOH"]
    return df, X, y


# ============================================================
# TRAIN HYBRID MODELS
# ============================================================
def train_hybrid_models(X, y):
    # Linear Regression
    lin_reg = LinearRegression()
    lin_reg.fit(X, y)

    # Random Forest (robust for missing values)
    rf = RandomForestRegressor(
        n_estimators=300,
        max_depth=None,
        random_state=42
    )
    rf.fit(X, y)

    return lin_reg, rf


# ============================================================
# EVALUATE LINEAR REGRESSION MODEL
# ============================================================
def evaluate_model(model, X_test, y_test):
    y_pred = model.predict(X_test)

    metrics = {
        "R² Score": r2_score(y_test, y_pred),
        "MSE": mean_squared_error(y_test, y_pred),
        "MAE": mean_absolute_error(y_test, y_pred),
    }

    return y_pred, metrics


# ============================================================
# FEATURE IMPORTANCE (Linear Regression)
# ============================================================
def compute_feature_importance(model, feature_names):
    coef = model.coef_

    # Flatten if shape is (1, n_features)
    if coef.ndim > 1:
        coef = coef.ravel()

    coefficients = pd.DataFrame({
        "Feature": feature_names,
        "Coefficient": coef,
        "AbsCoefficient": np.abs(coef),
    })

    coefficients = coefficients.sort_values("AbsCoefficient", ascending=False)
    coefficients = coefficients.drop(columns=["AbsCoefficient"]).reset_index(drop=True)

    return coefficients


# ============================================================
# SAVE RESULTS TO EXCEL
# ============================================================
def save_results(df_results, threshold):
    filename = f"SOH_Predictions_{threshold}_threshold.xlsx"
    df_results.to_excel(filename, index=False)
    return filename


# ============================================================
# PLOT PREDICTIONS
# ============================================================
def plot_predictions(y_test, y_pred):
    plt.figure(figsize=(10, 6))
    plt.scatter(y_test, y_pred, alpha=0.6)
    plt.plot([y_test.min(), y_test.max()],
             [y_test.min(), y_test.max()],
             linestyle='--')
    plt.title("Actual vs Predicted SOH")
    plt.xlabel("Actual SOH")
    plt.ylabel("Predicted SOH")
    plt.grid()
    plt.savefig("actual_vs_predicted.png")
    plt.show()


# ============================================================
# FILL MISSING FEATURES USING TRAINING MEANS
# ============================================================
def prepare_input_mean(df_partial, expected_features, X_train):
    df_full = df_partial.copy()
    for col in expected_features:
        if col not in df_full.columns:
            df_full[col] = X_train[col].mean()
    return df_full[expected_features]


# ============================================================
# AUTOMATIC HYBRID MODEL SELECTION
# ============================================================
def choose_model(user_df, expected_features, lin_reg, rf, threshold=0.9):
    
    # If ANY NaN exists in user input → RandomForest handles missing values better
    if user_df.isna().any().any():
        print("Choosing RandomForest (missing values found)")
        return rf

    # Otherwise fall back to number of supplied features
    supplied = len(user_df.columns)
    total = len(expected_features)

    if supplied >= total * threshold:
        print("Choosing LinearRegression (enough features supplied)")
        return lin_reg
    else:
        print("Choosing RandomForest (not enough features supplied)")
        return rf


# ============================================================
# HYBRID PREDICTION FUNCTION
# ============================================================
def hybrid_predict(df_partial, expected_features, X_train, lin_reg, rf):
    # Replace empty strings with NaN
    df_partial = df_partial.replace("", np.nan).infer_objects(copy=False)
    model = choose_model(df_partial, expected_features, lin_reg, rf)
    prepared = prepare_input_mean(df_partial, expected_features, X_train)
    return model.predict(prepared)[0]


# ============================================================
# USER INPUT HANDLING
# ============================================================
def get_partial_user_input(expected_features):
    print("\nEnter ANY subset of features (press ENTER to skip):\n")
    user_vals = {}

    for feature in expected_features:
        val = input(f"{feature}: ").strip()
        if val == "":
            continue
        try:
            user_vals[feature] = float(val)
        except ValueError:
            print("Invalid number, skipping.")

    if len(user_vals) == 0:
        return None

    return pd.DataFrame([user_vals])


# ============================================================
# MAIN WORKFLOW
# ============================================================
def main():
    # Load and split data
    df, X, y = load_data("PulseBatDataset.xlsx")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    expected_features = X.columns.tolist()

    # Train hybrid models
    lin_reg_model, rf_model = train_hybrid_models(X_train, y_train)

    # Evaluate linear regression on full test set
    y_pred, metrics = evaluate_model(lin_reg_model, X_test, y_test)

    print("\nModel Evaluation Metrics:")
    for name, value in metrics.items():
        print(f"{name}: {value:.4f}")

    # User threshold
    threshold = float(input("\nEnter SOH threshold (default=0.6): ") or 0.6)

    # Classification for evaluation
    battery_class = ["Healthy" if s >= threshold else "Unhealthy"
                     for s in y_pred]

    df_results = pd.DataFrame({
        "Actual SOH": y_test.values,
        "Predicted SOH": y_pred,
        "Classification": battery_class
    })

    # Feature importance
    importance = compute_feature_importance(lin_reg_model, expected_features)
    print("\nTop 5 Features by Coefficient Importance:")
    print(importance.head().reset_index(drop=True))

    print("\nSample predictions:")
    print(df_results.head())

    # Save results
    excel_file = save_results(df_results, threshold)
    print(f"\nResults saved to '{excel_file}'")

    # Plot
    plot_predictions(y_test, y_pred)

    # Start Tkinter GUI for user input
    tktest.startTkinter(
        expected_features,
        X_train,
        lin_reg_model,
        rf_model
    )


r'''
How to set up virtual environment:
python -m venv venv
^only needed to make venv once^

--.\venv\Scripts\Activate.ps1

pip install google-genai python-dotenv
pip install pandas scikit-learn matplotlib openpyxl
^only needed to install packages once^

To run:
python linearmodel.py
Make sure to create a .env file with your GEMINI_API_KEY in the same directory as all the other files:
deactivate venv when done with:

--.\venv\Scripts\Deactivate.ps1
or just deactivate

'''
# ENTRY POINT
if __name__ == "__main__":
    main()
