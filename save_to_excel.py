def save_results(df_results, threshold):
    filename = f"SOH_Predictions_{threshold}_threshold.xlsx"
    df_results.to_excel(filename, index=False)
    return filename