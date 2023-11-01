from PySide2.QtCore import Signal, QObject

class EmittingStream(QObject):

    textWritten = Signal(str)

    def write(self, text):
        self.textWritten.emit(str(text))

    def flush(self):
        pass