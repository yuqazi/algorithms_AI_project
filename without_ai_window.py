import tkinter as tk
from tkinter import scrolledtext
import pandas as pd

import linearmodel as mod
import tkinter_helpers as tkh
import globalvalues as gv
import startup as startup_module

def submit(entries):
    Uvalues = {}
    for key in entries:
        value = entries[key].get()
        Uvalues[key] = value

    prediction = mod.hybrid_predict(pd.DataFrame([Uvalues]), gv.EXP_FEATURES, gv.X_TRAIN, gv.LIN_REG_MODEL, gv.RF_MODEL)
    print(f"\nPredicted SOH from UI Input: {prediction:.4f}")
    print("Battery Classification:", "Healthy" if prediction >= gv.SOH else "Unhealthy")

def change_soh(root):
    print("Placeholder for Change SOH")

def return_action(root):
    root.destroy()
    startup_module.main()

def startTkinter():
    root = tk.Tk()
    root.title("Battery SOH Predictor")
    root.configure(bg="#111111")

    # Styling
    label_style = tkh.label_style
    entry_style = tkh.entry_style

    # Store entry widgets so we can retrieve their values
    entries = {}

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

    make_row(root, ["U1", "U2", "U3", "U4", "U5", "U6"])
    make_row(root, ["U7", "U8", "U9", "U10", "U11", "U12"])
    make_row(root, ["U13", "U14", "U15", "U16", "U17", "U18"])
    make_row(root, ["U19", "U20", "U21"])

    # --- Results Label ---
    tk.Label(root, text="Results with SOH threshold: " + str(gv.SOH), **label_style).pack(pady=15)

    output_textbox = scrolledtext.ScrolledText(
        root, 
        width=80, 
        height=12, # Set a visible height
        bg="#333333", 
        fg="#FFFFFF", 
        insertbackground="#FFFFFF", 
        borderwidth=0,
        relief="flat",
        font=('Helvetica', 10)
    )

    output_textbox.pack(pady=10, padx=20)
    output_textbox.insert(tk.END, "Press 'Submit' to run prediction.")

    # --- Button Frame for organization ---
    button_frame = tk.Frame(root, bg="#111111")
    button_frame.pack(pady=20)

    # --- Submit Button ---
    submit_btn = tk.Button(button_frame, text="Submit", width=15, command=lambda: submit(entries))
    submit_btn.pack(side="left", padx=10)

    # --- Change SOH Button ---
    soh_btn = tk.Button(button_frame, text="Change SOH", width=15, command=lambda: change_soh(root))
    soh_btn.pack(side="left", padx=10)

    # --- Return Button ---
    return_btn = tk.Button(button_frame, text="Return", width=15, command=lambda: return_action(root))
    return_btn.pack(side="left", padx=10)

    tkh.center_window(root, 800, 700)
    root.mainloop()
