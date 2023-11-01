import sys
import logging
import time
from PySide2 import QtWidgets

class QtLogHandler(logging.Handler):
    def __init__(self, widget):
        super().__init__()
        self.widget = widget

    def emit(self, record):
        log_message = self.format(record)
        self.widget.append(log_message)

class LogWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Logging Output")

        layout = QtWidgets.QVBoxLayout()

        self.log_textedit = QtWidgets.QTextEdit()
        self.log_textedit.setReadOnly(True)
        layout.addWidget(self.log_textedit)

        self.button = QtWidgets.QPushButton("Press Me")
        layout.addWidget(self.button)

        self.setLayout(layout)

def set_logging(p_level=logging.INFO, log_file="info-log.txt", output_widget=None):
    logging.root.handlers = []
    
    log_format = "%(asctime)s [%(levelname)s] %(message)s"
    handlers = [logging.FileHandler(log_file), logging.StreamHandler()]
    
    if output_widget:
        qt_log_handler = QtLogHandler(output_widget)
        qt_log_handler.setFormatter(logging.Formatter(log_format))
        handlers.append(qt_log_handler)
    
    logging.basicConfig(level=p_level, format=log_format, handlers=handlers)

def on_button_click():
    logger.info("Button Pressed")
    app.processEvents()  # Handle pending events to update the GUI
    time.sleep(2)
    app.processEvents()  # Handle pending events to update the GUI
    logger.info("Button Processing Complete")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    log_widget = LogWidget()

    set_logging(output_widget=log_widget.log_textedit)  # Initialize logging with the QTextEdit widget

    logger = logging.getLogger()  # Get the root logger

    log_widget.button.clicked.connect(on_button_click)

    log_widget.show()
    sys.exit(app.exec_())
