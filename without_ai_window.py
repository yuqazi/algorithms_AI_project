import tkinter as tk
from tkinter import scrolledtext
from tkinter import filedialog
from tkinter import messagebox
import pandas as pd
from logging_system import get_logger

logger = get_logger(__name__)

import linearmodel as mod
import tkinter_helpers as tkh
import globalvalues as gv
import startup as startup_module
import change_soh_threshold as csoth
import math_plot_graph as mpg
import save_to_excel as ste

def run_pred(textbox, entries):
    logger.info("Run button pressed. Running prediction with user input values.")
    Uvalues = {}
    for key in entries:
        value = entries[key].get()
        Uvalues[key] = value
    try:
        logger.debug(f"Input U values: {Uvalues}")
        prediction = mod.hybrid_predict(pd.DataFrame([Uvalues]), gv.EXP_FEATURES, gv.X_TRAIN, gv.LIN_REG_MODEL, gv.RF_MODEL)
        line1 = f"\nPredicted SOH from UI Input: {prediction:.4f}\n"
        line2 = "Battery Classification: " + ("Healthy" if prediction >= gv.SOH else "Unhealthy") + "\n"
        line3 = gv.MODEL_CHOICE + "\n"
        textbox.configure(state='normal')
        textbox.insert(tk.END, line3)
        textbox.insert(tk.END, line1)
        textbox.insert(tk.END, line2 + "\n" + "-"*90 + "\n")
        textbox.see(tk.END)
        textbox.configure(state='disabled')
    except ValueError:
        logger.error("Invalid input values provided for U1-U21. Cannot run prediction.")
        messagebox.showerror("Error", "❌ Invalid input. Please ensure all U values are numeric.")

def initalizing_print(textbox):
    logger.info("Printing initializing text and current SOH threshold to output textbox.")
    textbox.configure(state='normal')
    textbox.insert(tk.END, "-"*90 + "\n")
    textbox.insert(tk.END, gv.INITALIZING_TEXT + "\n")
    textbox.insert(tk.END, "Current SOH threshold: " + str(gv.SOH) + "\n")
    textbox.insert(tk.END, "-"*90 + "\n")
    textbox.see(tk.END)
    textbox.insert(tk.END, "Press 'Run' to run predictions with current U values\n")
    textbox.insert(tk.END, "-"*90 + "\n")
    textbox.configure(state='disabled')
    gv.INITALIZING_TEXT = ""

def change_soh(master, textbox, label_text):
    logger.info("Change SOH Threshold button pressed. Opening change SOH threshold window.")
    csoth.change_soh_start(master)
    label_text.set(f"Results with SOH threshold: {gv.SOH}")
    initalizing_print(textbox)

def open_graph():
    logger.info("Open Graph button pressed. Displaying SOH prediction graph.")
    plt = mpg.create_soh_plot(gv.Y_TEST, gv.Y_PRED)
    mpg.show_soh_plot(plt)

def save_graph():
    logger.info("Save Graph button pressed. Saving SOH prediction graph.")
    plt = mpg.create_soh_plot(gv.Y_TEST, gv.Y_PRED)
    mpg.save_soh_plot(plt)

def save_excel_sheet():
    logger.info("Save Excel Sheet button pressed. Saving prediction results to Excel.")
    ste.save_results(gv.df_results, gv.SOH)

def save_runs(textbox):
    logger.info("Save Runs button pressed. Saving output textbox content to a text file.")
    content = textbox.get("1.0", "end-1c")
    try:
        # options for the save dialog
        file_options = {
            'defaultextension': '.txt',
            'filetypes': [
                ('Text files', '*.txt'),
                ('All files', '*.*')
            ]
        }
        # asksaveasfilename prompts the user and returns the chosen file path string.
        filepath = filedialog.asksaveasfilename(
            title="Save Text Content As",
            **file_options
        )

        # If a valid filepath is returned, write the content to that file.
        if filepath:
            with open(filepath, 'w', encoding='utf-8') as file:
                file.write(content)
            logger.info(f"Content successfully saved to: {filepath}")
        else:
            logger.info("Save operation cancelled by user.")
    
    # except block to catch any file operation errors.
    except Exception as e:
        print(f"An error occurred during save operation: {e}")
        messagebox.showerror("Error", f"Failed to save content: {e}")

def return_action(root):
    logger.info("Return to Startup button pressed. Closing current window and returning to startup.")
    root.destroy()
    startup_module.main()

def startTkinter():
    root = tk.Tk()
    root.title("Battery SOH Predictor (No AI)")
    root.configure(bg="#111111")

    # Store entry widgets
    entries = {}
    label_style = tkh.label_style
    entry_style = tkh.entry_style

    # --- Main Layout Container ---
    # This frame holds the entire application content and uses a 1-row, 2-column grid.
    main_container = tk.Frame(root, bg="#111111")
    # Sticky 'w' ensures the whole container is left-justified in the root window.
    main_container.grid(row=0, column=0, padx=20, pady=20, sticky="w") 

    # --- Column 1: Input and Output Content (Left Justified) ---
    content_frame = tk.Frame(main_container, bg="#111111")
    # Sticky 'nw' anchors the content to the top-left of the cell.
    content_frame.grid(row=0, column=0, sticky="nw", padx=(0, 30)) 

    def make_row(parent, labels):
        """Creates a row with label-entry pairs."""
        row_frame = tk.Frame(parent, bg="#111111")
        row_frame.pack(pady=10)
        for text in labels:
            cell = tk.Frame(row_frame, bg="#111111")
            cell.pack(side="left", padx=15)
            tk.Label(cell, text=text, **label_style).pack()
            e = tk.Entry(cell, **entry_style)
            e.pack()
            entries[text] = e   # store reference

    # Input Rows go into the content_frame
    make_row(content_frame, ["U1", "U2", "U3", "U4", "U5", "U6"])
    make_row(content_frame, ["U7", "U8", "U9", "U10", "U11", "U12"])
    make_row(content_frame, ["U13", "U14", "U15", "U16", "U17", "U18"])
    make_row(content_frame, ["U19", "U20", "U21"])

    label_m_text = tk.StringVar()
    label_m_text.set(f"Results with SOH threshold: {gv.SOH}")
    # Results Label (packed to the left with anchor='w')
    label_main = tk.Label(content_frame, textvariable=label_m_text, **label_style)
    label_main.pack(pady=(20, 10), anchor='w')

    # Output Textbox (packed to the left with anchor='w')
    output_textbox = scrolledtext.ScrolledText(
        content_frame, 
        width=80, 
        height=18, 
        bg="#333333", 
        fg="#FFFFFF", 
        insertbackground="#FFFFFF", 
        borderwidth=0,
        relief="flat",
        font=('Helvetica', 10)
    )
    output_textbox.pack(pady=10, padx=0, fill='x', anchor='w') 
    initalizing_print(output_textbox)
    output_textbox.configure(state='disabled')


    button_column = tk.Frame(main_container, bg="#111111")
    # Place the button column in the second column of the main_container grid.
    # Sticky 'n' aligns buttons to the top of the cell.
    button_column.grid(row=0, column=1, sticky="n", pady=10) 

    # Consistent Button styling
    button_style = tkh.button_style
    cancel_button_style = tkh.button_style_negative

    tk.Button(
        button_column, 
        text="Run", 
        command=lambda: run_pred(output_textbox, entries),
        **button_style
    ).pack(pady=10)

    tk.Button(
        button_column, 
        text="Change SOH Threshold", 
        command=lambda: change_soh(root, output_textbox, label_m_text),
        **button_style
    ).pack(pady=10)

    tk.Button(
        button_column, 
        text="Open Graph", 
        command=lambda: open_graph(),
        **button_style
    ).pack(pady=10)

    tk.Button(
        button_column, 
        text="Save Graph", 
        command=lambda: save_graph(),
        **button_style
    ).pack(pady=10)

    tk.Button(
        button_column, 
        text="Save Excel Sheet", 
        command=lambda: save_excel_sheet(),
        **button_style
    ).pack(pady=10)

    tk.Button(
        button_column, 
        text="Save Runs", 
        command=lambda: save_runs(output_textbox),
        **button_style
    ).pack(pady=10)

    tk.Button(
        button_column, 
        text="Return to Startup", 
        command=lambda: return_action(root),
        **cancel_button_style
    ).pack(pady=10)

    tkh.center_window(root, 960, 750)
    logger.info("Without AI application window launched successfully.")
    root.mainloop()