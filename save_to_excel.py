import tkinter as tk
from tkinter import filedialog
from logging_system import get_logger

logger = get_logger(__name__)

def save_results(df_results, threshold, filename="SOH_Predictions_Excel.xlsx"):
    tempfilename = f"SOH_Predictions_{threshold}_threshold.xlsx"
    df_results.to_excel(filename, index=False)

    """
    Opens a native system file save dialog for the user to select the
    location and filename, and saves the currently active Matplotlib figure.
    """
    # Initialize Tkinter and immediately hide the main window (we only need the dialog)
    root = tk.Tk()
    root.withdraw() 
    
    # Define file types that the user can select in the dialog
    file_types = [
        ('Excel', '*.xlsx'),
    ]
    
    filename = filedialog.asksaveasfilename(
        defaultextension=".xlsx",
        filetypes=file_types,
        initialfile=tempfilename,
        title="Save Excel As"
    )

    if filename:
        try:
            df_results.to_excel(filename, index=False)
            logger.info(f"Excel file saved successfully as: {filename}")
        except Exception as e:
            logger.error(f"Failed to save Excel file: {e}")
    else:
        logger.info("Save operation cancelled by user.")

    root.destroy()