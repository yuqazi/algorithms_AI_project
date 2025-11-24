import tkinter as tk

import tkinter_helpers as tkh
import globalvalues as gv
#def change_soh_start():
root = tk.Tk()
root.title("Change SOH Threshold")
root.configure(bg="#111111")

label_style = tkh.label_style
entry_style = tkh.entry_style

tk.Label(root, text="Current SOH Threshold: " + str(gv.SOH), **label_style).pack(pady=10)

input_frame = tk.Frame(root, bg="#111111")
input_frame.pack(pady=10)

tk.Label(input_frame, text="New SOH Threshold:", **label_style).grid(row=0, column=0, padx=5, pady=5)
soh_entry = tk.Entry(input_frame, **entry_style)
soh_entry.grid(row=0, column=1, padx=5, pady=5)

tk.submit_button = tk.Button(
    root,
    text="Submit",
    command=lambda: gv.change_soh(float(soh_entry.get()))
)
tk.submit_button.pack(pady=15)

tkh.center_window(root, 400, 200)
root.mainloop()