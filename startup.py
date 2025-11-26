import tkinter as tk
from tkinter import messagebox
import tkinter_helpers as tkh
import os
from dotenv import load_dotenv
from logging_system import get_logger

logger = get_logger(__name__)

import linearmodel as mod
import api_check_UI as apic_ui 
import api_check as apic
import with_ai_window as withai
import without_ai_window as waiw

def start_with_ai(root):
    logger.info("Start with AI button pressed. Starting application with AI features.")
    # Destroy the current startup window
    root.destroy()
    # Load the .env file to get the API key
    load_dotenv()
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    if(apic.check_api_key_validity(gemini_api_key)):
        mod.train()
        messagebox.showinfo("Success", "✅ Your saved API key is valid and working.")
        logger.info("Valid API key found in .env file, launching main UI.")
        withai.startTkinter()
    else:
        logger.warning("No valid API key found, launching API key entry UI.")
        apic_ui.start()

def start_without_ai(root):
    logger.info("Start without AI button pressed. Starting application without AI features.")
    mod.train()
    root.destroy()
    waiw.startTkinter()

def clear_dot_env():
    logger.info("Delete saved API key button pressed. Clearing .env file.")
    with open(".env", "w") as f:
        f.write("GEMINI_API_KEY=")
    logger.info("API key removed from .env file.")
    messagebox.showinfo("Removed", "The API key has been removed.")


# The main function to launch the startup window
def main():
    root = tk.Tk()
    root.title("Startup")
    root.configure(bg="#111111")

    label_style = tkh.label_style
    button_style = tkh.button_style
    cancel_button_style = tkh.button_style_negative

    tk.Label(root, text="Welcome to Battery SOH Checker!", **label_style).pack(pady=10)

    start_with_frame = tk.Frame(root, bg="#111111")
    start_with_frame.pack(pady=10)

    start_without_frame = tk.Frame(root, bg="#111111")
    start_without_frame.pack(pady=10)

    start_with_button = tk.Button(
        start_with_frame,
        text="Start with AI",
        command=lambda: start_with_ai(root),
        **button_style
    )

    start_without_button = tk.Button(
        start_without_frame,
        text="Start without AI",
        command=lambda: start_without_ai(root),
        **button_style
    )

    start_with_button.grid(row=0, column=1, padx=15)
    start_without_button.grid(row=0, column=1, padx=15)

    delete_dot_env_button = tk.Button(
        root,
        text="Delete saved API key",
        command=lambda: clear_dot_env(),
        **cancel_button_style
    )
    delete_dot_env_button.pack(pady=30)

    tkh.center_window(root, 400, 320)

    logger.info("Startup window launched successfully.")

    root.mainloop()

# Ensure the app runs when the file is executed directly
if __name__ == "__main__":
    main()