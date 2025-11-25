import tkinter as tk
from tkinter import messagebox

import tkinter_helpers as tkh
import globalvalues as gv

def change_soh(new_soh, label_text, text_widget):
    try:
        if(float(new_soh) < 0 or float(new_soh) > 1):
            tk.messagebox.showerror("Warning", "❌ SOH must be between 0 and 1.")
            return
        new_soh_value = float(new_soh)
        gv.change_soh(new_soh_value)
        tk.messagebox.showinfo("Success", f"✅ SOH threshold changed to {new_soh_value}.")
        label_text.set(f"Current SOH Threshold: {gv.SOH}")
    except ValueError:
        text_widget.delete("0", "end")
        tk.messagebox.showerror("Error", "❌ Invalid input. Please enter a numeric value.")

#def change_soh_start():
root = tk.Tk()
root.title("Change SOH Threshold")
root.configure(bg="#111111")

label_style = tkh.label_style
entry_style = tkh.entry_style
button_style = tkh.button_style

label_text = tk.StringVar()
label_text.set(f"Current SOH Threshold: {gv.SOH}")

label = tk.Label(root, textvariable=label_text, **label_style)
label.pack(pady=10)

input_frame = tk.Frame(root, bg="#111111")
input_frame.pack(pady=10)

tk.Label(input_frame, text="New SOH Threshold:", **label_style).grid(row=0, column=0, padx=5, pady=5)
soh_entry = tk.Entry(input_frame, **entry_style)
soh_entry.grid(row=0, column=1, padx=5, pady=5)

tk.submit_button = tk.Button(
    root,
    text="Submit",
    command=lambda: change_soh(soh_entry.get(), label_text, soh_entry),
    **button_style
)
tk.submit_button.pack(pady=15)

tkh.center_window(root, 400, 200)
root.mainloop()