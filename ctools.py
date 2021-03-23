from menu import menu
from cterasdk import *
import logging
from GUI import Menu

def set_logging(p_level=logging.INFO,log_file="log.txt"):
    """Set up logging to a given file name.
    
    Keyword arguments:
    p_level --  DEBUG, INFO, WARNING, ERROR, Critical. (default INFO)
    log_file -- file name for log file. (default "log.txt")
    """
    logging.root.handlers = []
    logging.basicConfig(
        level=p_level,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
   )

if __name__ == "__main__":
    set_logging(logging.DEBUG)
    logging.info('Starting ctools')
    GUI_TER=input("Switch to GUI or Not? (Y/N)",)
    if GUI_TER in ('y','Y'):
        Menu() # Gui window
    elif GUI_TER in ('n','N'):
        menu() # terminal Window
