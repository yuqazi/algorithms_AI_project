import tkinter as tk
import pandas as pd
import linearmodel as mod
import geminiMessage as gem

def startTkinter(expected_features, X_train, lin_reg_model, rf_model):
    client, chat = gem.start_gemini()

    root = tk.Tk()
    root.title("UI Layout Example")
    root.configure(bg="#111111")

    # Styling
    label_style = {"bg": "#111111", "fg": "white", "font": ("Arial", 10)}
    entry_style = {"width": 10}

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

    # --- Rows based on your image ----
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

    # --- Function for Submit ---
    def open_new_window(inputmessage):
        new_win = tk.Toplevel(root)
        new_win.title("Gemini Response")
        new_win.configure(bg="#222222")

        # --- Scrollable Canvas Setup ---
        container = tk.Frame(new_win, bg="#222222")
        container.pack(fill="both", expand=True)

        canvas = tk.Canvas(container, bg="#222222", highlightthickness=0)
        canvas.pack(side="left", fill="both", expand=True)

        scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scrollbar.pack(side="right", fill="y")

        canvas.configure(yscrollcommand=scrollbar.set)

        # Internal scroll frame
        scroll_frame = tk.Frame(canvas, bg="#222222")
        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")

        def update_scroll(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
        scroll_frame.bind("<Configure>", update_scroll)

        # -------------- EVERYTHING CENTERED --------------

        # Wrapper that expands full width and centers children
        center_frame = tk.Frame(scroll_frame, bg="#222222")
        center_frame.pack(fill="x")  # Forces width → allows centering

        # Title
        tk.Label(
            center_frame,
            text="Response from Gemini:",
            bg="#222222",
            fg="white",
            font=("Arial", 18, "bold"),
        ).pack(pady=10, anchor="center")

        # Input question
        tk.Label(
            center_frame,
            text=f"Input Question:\n{input_question.get()}",
            bg="#222222",
            fg="cyan",
            font=("Arial", 14, "bold"),
            wraplength=650,
            justify="center",
        ).pack(pady=10, anchor="center")

        # Gemini response (U values)
        tk.Label(
            center_frame,
            text=inputmessage,
            bg="#222222",
            fg="white",
            font=("Arial", 12),
            wraplength=650,
            justify="center",
        ).pack(pady=10, anchor="center")



    def submit():
        Uvalues = {}
        count = 0
        for key in entries:
            value = entries[key].get()
            Uvalues[key] = value

        question = input_question.get()
        prediction = mod.hybrid_predict(pd.DataFrame([Uvalues]), expected_features, X_train, lin_reg_model, rf_model)
        print(f"\nPredicted SOH from UI Input: {prediction:.4f}")
        print("Battery Classification:", "Healthy" if prediction >= 0.6 else "Unhealthy")
        gemini_initial = "Based on the provided battery cell voltages ({}) our Data model got the predicted State of Health (SOH): {:.4f} which we consider {}. Please use this for the following question.".format(Uvalues, prediction, "Healthy" if prediction >= 0.6 else "Unhealthy")
        #prompt gemini with question and take response
        gemini_reply = gem.gemini_response(question, gemini_initial)
        open_new_window(gemini_reply)

    # --- Submit Button ---
    submit_btn = tk.Button(root, text="Submit", width=15, command=submit)
    submit_btn.pack(pady=20)


    root.mainloop()
