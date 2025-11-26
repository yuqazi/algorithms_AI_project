import tkinter as tk
import pandas as pd
from tkinter import scrolledtext
from tkinter import filedialog
from tkinter import messagebox


import startup as startup_module
import geminiMessage as gem
import linearmodel as mod
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


def submit(root, entries, input_question, output_textbox):
    Uvalues = {}
    for key in entries:
        Uvalues[key] = entries[key].get()

    question = input_question.get()
    if question == "" or question == "Enter your question for Gemini here...":
        messagebox.showwarning("Input Error", "Please enter a question for Gemini.")
        return
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
        "Using the {} model, and {} as the healthy/unhealthy threshold.\n"
        "Please use this for the following question."
    ).format(
        Uvalues,
        prediction,
        "Healthy" if prediction >= gv.SOH else "Unhealthy",
        gv.MODEL_CHOICE,
        gv.SOH
    )

    gemini_reply = gem.gemini_response(question, gemini_initial)
    gemini_output(output_textbox, gemini_reply, input_question)
    input_question.delete(0, tk.END)
    input_question.selection_clear()
    root.focus_set()


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
        else:
            print("Save operation cancelled by user.")
    
    # except block to catch any file operation errors.
    except Exception as e:
        print(f"An error occurred during save operation: {e}")

def new_chat_session(textbox):
    gv.CLIENT, gv.CHAT = gem.start_gemini()
    textbox.configure(state='normal')
    textbox.delete("1.0", tk.END)
    messagebox.showwarning("New Chat Session", "New Gemini chat session started.")
    initalizing_print(textbox)
    textbox.see(tk.END)


def add_placeholder(entry, placeholder):
    entry.insert(0, placeholder)
    entry.config(fg="grey")

    def on_focus_in(event):
        if entry.get() == placeholder:
            entry.delete(0, "end")
            entry.config(fg="black")  # text color when typing

    def on_focus_out(event):
        if entry.get() == "":
            entry.insert(0, placeholder)
            entry.config(fg="grey")

    entry.bind("<FocusIn>", on_focus_in)
    entry.bind("<FocusOut>", on_focus_out)


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
    add_placeholder(input_question, "Enter your question for Gemini here...")

    def submit():
        Uvalues = {}
        for key in entries:
            Uvalues[key] = entries[key].get()

        question = input_question.get()
        if question == "" or question == "Enter your question for Gemini here...":
            messagebox.showwarning("Input Error", "Please enter a question for Gemini.")
            return
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

    label_m_text = tk.StringVar()
    label_m_text.set(f"Results with SOH threshold: {gv.SOH}")
    # Results Label (packed to the left with anchor='w')
    label_main = tk.Label(content_frame, textvariable=label_m_text, **label_style)
    label_main.pack(pady=(20, 10), anchor='w')

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

    # RIGHT-SIDE BUTTON COLUMN (scrolls too)
    button_column = tk.Frame(main_container, bg="#111111")
    button_column.grid(row=0, column=1, sticky="n", pady=10)

    button_style = tkh.button_style
    cancel_button_style = tkh.button_style_negative

    tk.Button(
        button_column, 
        text="Submit", 
        command=lambda: submit(root, entries, input_question, output_textbox),
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
        text="New Chat Session", 
        command=lambda: new_chat_session(output_textbox),
        **button_style
    ).pack(pady=10)

    tk.Button(
        button_column, 
        text="Return to Startup", 
        command=lambda: return_action(root),
        **cancel_button_style
    ).pack(pady=10)

    # Center window
    tkh.center_window(root, 960, 800)
    root.mainloop()

