import sys
import logging
from PySide2 import QtWidgets

class QtLogHandler(logging.Handler):
    def __init__(self, widget):
        super().__init__()
        self.widget = widget

    def emit(self, record):
        log_message = self.format(record)
        self.widget.append(log_message)

def set_logging(p_level=logging.INFO, log_file="info-log.txt", output_widget=None):
    """
    Set up logging to a given file name.
    Doesn't require CTERASDK_LOG_FILE to be set.

    p_level --  DEBUG, INFO, WARNING, ERROR, Critical. (default INFO)
    log_file -- file name for log file. (default "log.txt")
    """
    logging.root.handlers = []
    
    log_format = "%(asctime)s [%(levelname)s] %(message)s"
    handlers = [logging.FileHandler(log_file), logging.StreamHandler()]
    
    if output_widget:
        qt_log_handler = QtLogHandler(output_widget)
        qt_log_handler.setFormatter(logging.Formatter(log_format))
        handlers.append(qt_log_handler)
    
    logging.basicConfig(level=p_level, format=log_format, handlers=handlers)