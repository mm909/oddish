
import os
import webbrowser

def open_browser(out_file):
    """
    Open a file in the browser.

    Parameters
    ----------
    out_file : str
        The path to save the plot.
    """
    chrome_path = 'C:/Program Files/Google/Chrome/Application/chrome.exe %s'
    full_path = os.path.abspath(out_file)
    webbrowser.get(chrome_path).open(full_path)