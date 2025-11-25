import matplotlib.pyplot as plt
import numpy as np
import os
from tkinter import Tk, filedialog

# 1. Core plotting function
def create_soh_plot(y_test, y_pred):
    # Create a new figure and axes for the plot
    plt.figure(figsize=(10, 6))
    
    # Scatter plot of predicted vs actual values
    plt.scatter(y_test, y_pred, alpha=0.6, label="Data Points")

    min_val = min(min(y_test), min(y_pred))
    max_val = max(max(y_test), max(y_pred))
    plt.plot([min_val, max_val],
             [min_val, max_val],
             linestyle='--', color='red', linewidth=2, label="Prediction")
             
    # Set plot properties
    plt.title("Actual vs Predicted State of Health (SOH)", fontsize=16, fontweight='bold')
    plt.xlabel("Actual SOH Value", fontsize=12)
    plt.ylabel("Predicted SOH Value", fontsize=12)
    plt.legend()
    plt.grid(True, linestyle=':', alpha=0.7)
    plt.tight_layout() # Adjust layout to prevent labels from overlapping
    return plt

# 2. Function to show the plot to the user
def show_soh_plot(plt):
    """
    Displays the currently active Matplotlib figure.
    """
    print("Displaying the plot...")
    plt.show()

# 3. Function to save the plot as a file with a custom name
def save_soh_plot(plt, filename="actual_vs_predicted_soh.png"):
    """
    Opens a native system file save dialog for the user to select the
    location and filename, and saves the currently active Matplotlib figure.
    """
    # Initialize Tkinter and immediately hide the main window (we only need the dialog)
    root = Tk()
    root.withdraw() 
    
    # Define file types that the user can select in the dialog
    file_types = [
        ('PNG Image', '*.png'),
        ('PDF Document', '*.pdf'),
        ('JPEG Image', '*.jpg'),
        ('SVG Vector Graphics', '*.svg'),
        ('All Files', '*.*')
    ]
    
    filename = filedialog.asksaveasfilename(
        defaultextension=".png",
        filetypes=file_types,
        initialfile="actual_vs_predicted_soh.png",
        title="Save Plot As"
    )

    if filename:
        try:
            print(f"Saving plot to file: {filename}")
            plt.savefig(filename, dpi=300, bbox_inches='tight')
            print("Save complete.")
        except Exception as e:
            print(f"An error occurred while saving the file: {e}")
    else:
        print("Save cancelled by user.")

    root.destroy()