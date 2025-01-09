class ExportError(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message

class ProcessingError(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message