def center_window(root, width, height):
    # Get screen width and height
    ws = root.winfo_screenwidth() 
    hs = root.winfo_screenheight() 

    # Calculate x and y coordinates for the centered window
    x = (ws/2) - (width/2)
    y = (hs/2) - (height/2)

    # Set the geometry to the calculated position
    root.geometry('%dx%d+%d+%d' % (width, height, x, y))


BG_COLOR = "#020617"          # overall background
CARD_BG = "#020617"           # container background
TEXT_COLOR = "#e5e7eb"        # main text
SUBTLE_TEXT = "#9ca3af"       # secondary text
ACCENT = "#3b82f6"            # blue buttons
ACCENT_HOVER = "#2563eb"
DANGER = "#ef4444"            # red button
DANGER_HOVER = "#dc2626"
BORDER_COLOR = "#1f2937"

label_style = {
    "bg": BG_COLOR,
    "fg": TEXT_COLOR,
    "font": ("Segoe UI", 12, "bold"),
}

text_style = {
    "bg": BG_COLOR,
    "fg": SUBTLE_TEXT,
    "font": ("Segoe UI", 10),
}

button_style = {
    "width": 18,
    "height": 2,
    "bg": ACCENT,
    "fg": "white",
    "activebackground": ACCENT_HOVER,
    "activeforeground": "white",
    "bd": 0,
    "relief": "flat",
    "font": ("Segoe UI", 10, "bold"),
    "cursor": "hand2",
}

button_style_negative = {
    "width": 18,
    "height": 2,
    "bg": DANGER,
    "fg": "white",
    "activebackground": DANGER_HOVER,
    "activeforeground": "white",
    "bd": 0,
    "relief": "flat",
    "font": ("Segoe UI", 10, "bold"),
    "cursor": "hand2",
}

entry_style = {
    "width": 10,
    "bg": CARD_BG,
    "fg": TEXT_COLOR,
    "insertbackground": TEXT_COLOR,
    "bd": 1,
    "relief": "flat",
    "highlightthickness": 1,
    "highlightbackground": BORDER_COLOR,
    "highlightcolor": ACCENT,
    "font": ("Segoe UI", 10),
}

entry_style_large = {
    **entry_style,
    "width": 50,
}