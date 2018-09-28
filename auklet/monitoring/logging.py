class AukletLogging(object):
    def log(self, msg, data_type, level="INFO"):
        raise NotImplementedError("Must implement method: log")

    def debug(self, msg, data_type):
        self.log(msg, data_type, "DEBUG")

    def info(self, msg, data_type):
        self.log(msg, data_type, "INFO")

    def warning(self, msg, data_type):
        self.log(msg, data_type, "WARNING")

    def error(self, msg, data_type):
        self.log(msg, data_type, "ERROR")

    def critical(self, msg, data_type):
        self.log(msg, data_type, "CRITICAL")
