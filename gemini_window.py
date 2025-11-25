import tkinter as tk

def open_new_window(root, inputmessage, input_question_box):
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
        text=f"Input Question:\n{input_question_box.get()}",
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