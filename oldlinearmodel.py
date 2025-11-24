import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import matplotlib.pyplot as plt

# Load dataset
file_path = "PulseBatDataset.xlsx"
df = pd.read_excel(file_path)

# Select features (cols 8-29) and target SOH (col 30)
X = df.iloc[:, 8:29]
y = df["SOH"]


# Split dataset 80% train / 20% test
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train Linear Regression model
model = LinearRegression()
model.fit(X_train, y_train)

# Predict test SOH
y_pred = model.predict(X_test)


# Evaluate model performance
r2 = r2_score(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)
mae = mean_absolute_error(y_test, y_pred)

print("Model Evaluation Metrics:")
print(f"R² Score: {r2:.4f}")
print(f"Mean Squared Error (MSE): {mse:.4f}")
print(f"Mean Absolute Error (MAE): {mae:.4f}")


# Threshold classification from User input
threshold = float(input("\nEnter SOH threshold (default=0.6): ") or 0.6)

# Classify predicted SOH
battery_class = ["Healthy" if soh >= threshold else "Unhealthy" for soh in y_pred]
df_results = pd.DataFrame({
    "Actual SOH": y_test.values,
    "Predicted SOH": y_pred,
    "Classification": battery_class
})

# Feature importance based on coefficients
coefficients = pd.DataFrame({
    "Feature": X.columns,
    "Coefficient": model.coef_
}).sort_values(by="Coefficient", ascending=False)

# Display Top 5 based on feature importance
print("\nTop 5 Features based on Coefficient Importance:")
top5 = coefficients.head().reset_index(drop=True)
top5.insert(0, "Rank", range(1, len(top5) + 1))
print(top5.to_string(index=False))

# Display and save results
print("\nSample predictions:")
print(df_results.head())

# Save results to Excel
excelname = "SOH_Predictions_" + str(threshold) + "_threshold.xlsx"

df_results.to_excel(excelname, index=False)
print(f"\nResults saved to '{excelname}'")

test = model.predict(X_test)

# Plot Actual vs Predicted SOH
plt.figure(figsize=(10, 6))
plt.scatter(y_test, y_pred, color='blue', alpha=0.6)
plt.plot([y.min(), y.max()], [y.min(), y.max()], color='red', linestyle='--')
plt.title("Actual vs Predicted SOH")
plt.xlabel("Actual SOH")
plt.ylabel("Predicted SOH")
plt.grid()
plt.savefig('actual_vs_predicted.png')
plt.show()

