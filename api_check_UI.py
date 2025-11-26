import tkinter as tk
from tkinter import messagebox
from logging_system import get_logger

logger = get_logger(__name__)

import startup as startup_module
import linearmodel as mod
import api_check as apic
import tkinter_helpers as tkh
import tkintertest as tktest
import globalvalues as gv

def use_api_key(root, api_key_entry):
    logger.info("Use API Key button pressed. Validating API key.")
    api_key = api_key_entry.get().strip()
    if not api_key:
        logger.warning("No API key entered.")
        messagebox.showwarning("Input Error", "❌ Please enter an API key.")
        return
    
    valid = apic.check_api_key_validity(api_key)
    if valid:
        logger.info("Valid API key entered. Proceeding to train model and launch main AI UI.")
        mod.train()
        messagebox.showinfo("Success", "✅ The API key is valid and working.")
        gv.change_key(api_key)
        root.destroy()
        tktest.startTkinter()
    else:
        logger.error("Invalid API key entered.")
        messagebox.showerror("Invalid Key", "❌ The API key is invalid or has issues.")

def save_api_key(root, api_key_entry):
    logger.info("Save API Key button pressed. Validating and saving API key.")
    api_key = api_key_entry.get().strip()
    if not api_key:
        logger.warning("No API key entered for saving.")
        messagebox.showwarning("Input Error", "❌ Please enter an API key.")
        return
    
    valid = apic.check_api_key_validity(api_key)
    if valid:
        logger.info("Valid API key entered. Saving to .env file.")
        with open(".env", "w") as f:
            f.write("GEMINI_API_KEY=" + api_key + "\n")
        messagebox.showinfo("Saved", "✅ The API key has been saved successfully.")
    else:
        logger.error("Invalid API key entered for saving.")
        messagebox.showerror("Invalid Key", "❌ The API key is invalid or has issues.")

def cancel(root):
    logger.info("Cancel button pressed. Returning to startup module.")
    root.destroy()
    startup_module.main()

def start():
    root = tk.Tk()
    root.title("API Key Entry")
    root.configure(bg="#111111")
    
    label_style = tkh.label_style
    entry_style = tkh.entry_style_large
    button_style = tkh.button_style
    cancel_button_style = tkh.button_style_negative

    tk.Label(root, text="Enter your API Key:", **label_style).pack(pady=10)
    api_key_entry = tk.Entry(root, **entry_style)
    api_key_entry.pack(pady=12)

    button_frame = tk.Frame(root, bg="#111111")
    button_frame.pack(pady=10)

    submit_button_use = tk.Button(
        button_frame,
        text="Use", 
        command=lambda: use_api_key(root, api_key_entry),
        **button_style
    )

    submit_button_use.grid(row=0, column=0, padx=15)

    submit_button_save = tk.Button(
        button_frame,
        text="Save", 
        command=lambda: save_api_key(root, api_key_entry), 
        **button_style
    )

    submit_button_save.grid(row=0, column=1, padx=15)

    submit_button_cancel = tk.Button(
        text="Cancel", 
        command=lambda: cancel(root),
        **cancel_button_style
    )
    submit_button_cancel.pack(padx=15, pady=10)

    tkh.center_window(root, 600, 250)
    logger.info("API Key Entry window launched successfully.")
    root.mainloop()
