import tkinter as tk
import pandas as pd
from tkinter import scrolledtext
from tkinter import filedialog
from tkinter import messagebox


import startup as startup_module
import geminiMessage as gem
import linearmodel as mod
import gemini_window as gw
import tkinter_helpers as tkh
import globalvalues as gv
import change_soh_threshold as csoth
import math_plot_graph as mpg
import save_to_excel as ste

def return_action(root):
    root.destroy()
    startup_module.main()

def gemini_output(textbox, gemini_reply, input_question):

    line1 = f"\nGemini's Response to: '{input_question.get()}'\n"
    line2 = gemini_reply + "\n"

    textbox.configure(state='normal')
    textbox.insert(tk.END,"\n" + "-"*90 + "\n")
    textbox.insert(tk.END, line1)
    textbox.insert(tk.END, line2)
    textbox.insert(tk.END,"\n" + "-"*90 + "\n")
    textbox.see(tk.END)
    textbox.configure(state='disabled')

def run_pred(textbox, entries):
    Uvalues = {}
    for key in entries:
        value = entries[key].get()
        Uvalues[key] = value

    prediction = mod.hybrid_predict(pd.DataFrame([Uvalues]), gv.EXP_FEATURES, gv.X_TRAIN, gv.LIN_REG_MODEL, gv.RF_MODEL)
    line1 = f"\nPredicted SOH from UI Input: {prediction:.4f}\n"
    line2 = "Battery Classification: " + ("Healthy" if prediction >= gv.SOH else "Unhealthy") + "\n"
    line3 = gv.MODEL_CHOICE + "\n"

    textbox.configure(state='normal')
    textbox.insert(tk.END,"\n" + "-"*90 + "\n")
    textbox.insert(tk.END, line3)
    textbox.insert(tk.END, line1)
    textbox.insert(tk.END, line2 + "\n" + "-"*90 + "\n")
    textbox.see(tk.END)
    textbox.configure(state='disabled')

def initalizing_print(textbox):
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
    csoth.change_soh_start(master)
    label_text.set(f"Results with SOH threshold: {gv.SOH}")
    initalizing_print(textbox)

def open_graph():
    plt = mpg.create_soh_plot(gv.Y_TEST, gv.Y_PRED)
    mpg.show_soh_plot(plt)

def save_graph():
    plt = mpg.create_soh_plot(gv.Y_TEST, gv.Y_PRED)
    mpg.save_soh_plot(plt)

def save_excel_sheet():
    ste.save_results(gv.df_results, gv.SOH)

def save_runs(textbox):
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
            print(f"Content successfully saved to: {filepath}")
            messagebox.showinfo("Success", f"Content saved to:\n{filepath}")
        else:
            print("Save operation cancelled by user.")
    
    # except block to catch any file operation errors.
    except Exception as e:
        print(f"An error occurred during save operation: {e}")
        messagebox.showerror("Error", f"Failed to save content: {e}")

def startTkinter():
    client, chat = gem.start_gemini()

    root = tk.Tk()
    root.title("Battery SOH Predictor with Gemini AI")
    root.configure(bg="#111111")

    label_style = tkh.label_style
    entry_style = tkh.entry_style

    # ==========================================================
    #                FULL-WINDOW SCROLLBAR
    # ==========================================================
    outer_frame = tk.Frame(root, bg="#111111")
    outer_frame.pack(fill="both", expand=True)

    canvas = tk.Canvas(
        outer_frame,
        bg="#111111",
        highlightthickness=0
    )
    canvas.pack(side="left", fill="both", expand=True)

    scrollbar = tk.Scrollbar(
        outer_frame,
        orient="vertical",
        command=canvas.yview
    )
    scrollbar.pack(side="right", fill="y")

    canvas.configure(yscrollcommand=scrollbar.set)

    # Resize scroll-region automatically
    canvas.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    # Frame inside the canvas that will contain EVERYTHING
    main_container = tk.Frame(canvas, bg="#111111")
    canvas.create_window((0, 0), window=main_container, anchor="nw")

    # Smooth mouse wheel scrolling
    def _on_mousewheel(event):
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    canvas.bind_all("<MouseWheel>", _on_mousewheel)

    # ==========================================================
    #                      MAIN CONTENT
    # ==========================================================

    # LEFT CONTENT AREA (uses pack)
    content_frame = tk.Frame(main_container, bg="#111111")
    content_frame.grid(row=0, column=0, sticky="nw", padx=(20, 30), pady=20)

    # Store entry widgets
    entries = {}

    def make_row(parent, labels):
        row_frame = tk.Frame(parent, bg="#111111")
        row_frame.pack(pady=10)

        for text in labels:
            cell = tk.Frame(row_frame, bg="#111111")
            cell.pack(side="left", padx=15)

            tk.Label(cell, text=text, **label_style).pack()
            e = tk.Entry(cell, **entry_style)
            e.pack()
            entries[text] = e

    make_row(content_frame, ["U1", "U2", "U3", "U4", "U5", "U6"])
    make_row(content_frame, ["U7", "U8", "U9", "U10", "U11", "U12"])
    make_row(content_frame, ["U13", "U14", "U15", "U16", "U17", "U18"])
    make_row(content_frame, ["U19", "U20", "U21"])

    tk.Label(content_frame, text="Input Gemini Question", **label_style).pack(pady=10)

    # LARGE TEXT ENTRY
    large_frame = tk.Frame(content_frame, bg="#111111")
    large_frame.pack(pady=10)

    input_question = tk.Entry(large_frame, width=80)
    input_question.pack(ipady=10)

    def submit():
        Uvalues = {}
        for key in entries:
            Uvalues[key] = entries[key].get()

        question = input_question.get()
        prediction = mod.hybrid_predict(pd.DataFrame([Uvalues]),
                                        gv.EXP_FEATURES,
                                        gv.X_TRAIN,
                                        gv.LIN_REG_MODEL,
                                        gv.RF_MODEL)

        print(f"\nPredicted SOH from UI Input: {prediction:.4f}")
        print("Battery Classification:", "Healthy" if prediction >= gv.SOH else "Unhealthy")

        gemini_initial = (
            "Respond only in plain, unformatted text. Do not use markdown.\n"
            "Based on the provided battery cell voltages ({}), "
            "our Data model predicted SOH: {:.4f}, which is {}. "
            "Please use this for the following question."
        ).format(
            Uvalues,
            prediction,
            "Healthy" if prediction >= gv.SOH else "Unhealthy"
        )

        gemini_reply = gem.gemini_response(question, gemini_initial)
        gemini_output(output_textbox, gemini_reply, input_question)

    submit_btn = tk.Button(content_frame, text="Submit", width=15, command=submit)
    submit_btn.pack(pady=20)

    # OUTPUT TEXT BOX
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
    output_textbox.pack(pady=10, fill='x', anchor='w')
    initalizing_print(output_textbox)
    output_textbox.configure(state='disabled')

    label_m_text = tk.StringVar()
    label_m_text.set(f"Results with SOH threshold: {gv.SOH}")
    # Results Label (packed to the left with anchor='w')
    label_main = tk.Label(content_frame, textvariable=label_m_text, **label_style)
    label_main.pack(pady=(20, 10), anchor='w')

    # RIGHT-SIDE BUTTON COLUMN (scrolls too)
    button_column = tk.Frame(main_container, bg="#111111")
    button_column.grid(row=0, column=1, sticky="n", pady=10)

    button_style = tkh.button_style

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
        text="Return to Startup", 
        command=lambda: return_action(root),
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

    # Center window
    tkh.center_window(root, 800, 500)

    root.mainloop()

