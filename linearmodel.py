import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import matplotlib.pyplot as plt
import numpy as np
import with_ai_window as tktest
from logging_system import get_logger
logger = get_logger(__name__)

import globalvalues as gv
import save_to_excel as ste
import math_plot_graph as mpg


# ============================================================
# LOAD DATA
# ============================================================
def load_data(file_path):
    df = pd.read_excel(file_path)
    X = df.iloc[:, 8:29]     # SOE + U1–U21
    y = df["SOH"]
    logger.info(f"Data loaded from {file_path} with {df.shape[0]} records.")
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
    logger.info("Hybrid models trained: Linear Regression and Random Forest.")
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
    logger.info(f"Model evaluation metrics: {metrics}")
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
    logger.info("Computed feature importance based on linear regression coefficients.")
    return coefficients


# ============================================================
# FILL MISSING FEATURES USING TRAINING MEANS
# ============================================================
def prepare_input_mean(df_partial, expected_features, X_train):
    df_full = df_partial.copy()
    for col in expected_features:
        if col not in df_full.columns:
            df_full[col] = X_train[col].mean()
    logger.info("Prepared input data by filling missing features with training means.")
    return df_full[expected_features]


# ============================================================
# AUTOMATIC HYBRID MODEL SELECTION
# ============================================================
def choose_model(user_df, expected_features, lin_reg, rf, threshold=0.9):
    
    # If ANY NaN exists in user input → RandomForest handles missing values better
    if user_df.isna().any().any():
        logger.info("Choosing RandomForest model due to presence of missing values in input.")
        gv.MODEL_CHOICE = "Choosing RandomForest (missing values detected)"
        return rf

    # Otherwise fall back to number of supplied features
    supplied = len(user_df.columns)
    total = len(expected_features)

    if supplied >= total * threshold:
        logger.info("Choosing LinearRegression model due to sufficient features supplied.")
        gv.MODEL_CHOICE = "Choosing LinearRegression (enough features supplied)"
        return lin_reg
    else:
        logger.info("Choosing RandomForest model due to insufficient features supplied.")
        gv.MODEL_CHOICE = "Choosing RandomForest (not enough features supplied)"
        return rf


# ============================================================
# HYBRID PREDICTION FUNCTION
# ============================================================
def hybrid_predict(df_partial, expected_features, X_train, lin_reg, rf):
    pd.set_option('future.no_silent_downcasting', True)
    # Replace empty strings with NaN
    df_partial = df_partial.replace("", np.nan).infer_objects(copy=False)
    model = choose_model(df_partial, expected_features, lin_reg, rf)
    prepared = prepare_input_mean(df_partial, expected_features, X_train)
    logger.info("Running hybrid prediction on prepared input data.")
    return model.predict(prepared)[0]


# ============================================================
# MAIN WORKFLOW
# ============================================================
def train():
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

    gv.INITALIZING_TEXT += "\nModel Evaluation Metrics:"
    parts = []
    for name, value in metrics.items():
        parts.append(f"{name}: {value:.4f}")
        gv.INITALIZING_TEXT = "".join(parts)


    # User threshold
    # threshold = float(input("\nEnter SOH threshold (default=0.6): ") or 0.6)
    threshold = gv.SOH

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
    gv.INITALIZING_TEXT += str("\nTop 5 Features by Coefficient Importance:")
    gv.INITALIZING_TEXT += str(importance.head().reset_index(drop=True))

    gv.INITALIZING_TEXT += str("\nSample predictions:")
    gv.INITALIZING_TEXT += str(df_results.head())

    logger.info("Training complete. Storing models and data in global values.")
    gv.change_exp_features(expected_features)
    gv.change_x_train(X_train)
    gv.change_lin_reg_model(lin_reg_model)
    gv.change_rf_model(rf_model)
    gv.training_results(df_results)


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
    train()
