#Step 1: Custom print function to log output
class LoggerWrapper:
    def __init__(self, logger):
        self.logger = logger
    
    def write(self, message):
        if message.strip():
            self.logger.info(message.strip())

    def flush(self):
        pass # Required for compatibility with sys.stdout


