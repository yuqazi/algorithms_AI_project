# Battery SOH Checker with Gemini AI integration

This is a battery State-of-Health (SOH) checker with Gemini AI integration. Uses different prediction models to predict the SOH of your battery pack and allows conversation with a friendly AI companion.

### Features
- Full Gemini AI integration
- Mode that avoid AI and uses only the prediction model
- Persistant Gemini API storage
- Produces Excel sheets based on user input
- Plots graphs using Matplotlib
- System logging
- Simple, clean and easy to use UI made using Python Tkinter
***
### How to Run
- Clone this repository or download it as a zip
- Setup python virtual environment (run the following commands in your console line-by-line)
    1. `python -m venv venv` (only needed to make venv once)
    2. `.\venv\Scripts\Activate.ps1`
    3. `pip install google-genai python-dotenv` (only needed to install packages once)
    4. `pip install pandas scikit-learn matplotlib openpyxl` (only needed to install packages once)
- Run `startup.py` to launch the application.
- Close `venv` by running `deactivate` in the console when done.
***