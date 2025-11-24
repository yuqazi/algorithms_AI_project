import tkinter as tk
import pandas as pd

import geminiMessage as gem

import linearmodel as mod
import gemini_window as gw
import tkinter_helpers as tkh
import globalvalues as gv

def startTkinter():
    client, chat = gem.start_gemini()

    root = tk.Tk()
    root.title("Battery SOH Predictor with Gemini AI")
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

    # --- Input Question Label ---
    tk.Label(root, text="Input Gemini Question", **label_style).pack(pady=10)

    # --- Large input box ---
    large_frame = tk.Frame(root, bg="#111111")
    large_frame.pack(pady=10)

    input_question = tk.Entry(large_frame, width=80)
    input_question.pack(ipady=10)

    def submit():
        Uvalues = {}
        for key in entries:
            value = entries[key].get()
            Uvalues[key] = value

        question = input_question.get()
        prediction = mod.hybrid_predict(pd.DataFrame([Uvalues]), gv.EXP_FEATURES, gv.X_TRAIN, gv.LIN_REG_MODEL, gv.RF_MODEL)
        print(f"\nPredicted SOH from UI Input: {prediction:.4f}")
        print("Battery Classification:", "Healthy" if prediction >= gv.SOH else "Unhealthy")
        gemini_initial = "Based on the provided battery cell voltages ({}) our Data model got the predicted State of Health (SOH): {:.4f} which we consider {}. Please use this for the following question.".format(Uvalues, prediction, "Healthy" if prediction >= gv.SOH else "Unhealthy")
        #prompt gemini with question and take response
        gemini_reply = gem.gemini_response(question, gemini_initial)
        gw.open_new_window(root ,gemini_reply, input_question)

    # --- Submit Button ---
    submit_btn = tk.Button(root, text="Submit", width=15, command=submit)
    submit_btn.pack(pady=20)

    tkh.center_window(root, 800, 500)
    root.mainloop()
