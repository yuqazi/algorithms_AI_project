def center_window(root, width, height):
    # Get screen width and height
    ws = root.winfo_screenwidth() 
    hs = root.winfo_screenheight() 

    # Calculate x and y coordinates for the centered window
    x = (ws/2) - (width/2)
    y = (hs/2) - (height/2)

    # Set the geometry to the calculated position
    root.geometry('%dx%d+%d+%d' % (width, height, x, y))


label_style = {"bg": "#111111", "fg": "white", "font": ("Arial", 14)}
text_style = {"bg": "#111111", "fg": "white", "font": ("Arial", 10)}
button_style = {'width': 18, 'height': 2, 'bg': "#A6CEFC", 'fg': 'black', 'relief': 'flat', 'font': ('Helvetica', 10, 'italic')}
button_style_negative = {'width': 18, 'height': 2, 'bg': "#FF6B6B", 'fg': 'black', 'relief': 'flat', 'font': ('Helvetica', 10, 'italic')}
entry_style = {"width": 10}
entry_style_large = {"width": 50}