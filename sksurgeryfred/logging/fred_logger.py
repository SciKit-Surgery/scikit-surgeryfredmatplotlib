""" Class to handle sksurgeryfred logging """

from logging import getLogger, FileHandler, Formatter, INFO

class Logger():
    """Implements logging functionality for sksurgeryfred.
    Configuration is done by passing a dictionary on construction.
    Subsequent calls to log("message") will write to log file.
    """

    def __init__(self, config):
        """
        Initialises the logger based on the passed configuration:
        :params: config - a dictionary containing configuration
        parameters. If dictionary contains no "logger" entry then
        an empty logger is created and subsequent calls to log() will
        have no effect. Otherwise a logger is created according to the
        entries in the logger config dictionary. ("log file name",
        "overwrite existing"
        :raises: IOError if the user can't write to the named log file?
        """

        self._no_logging = True
        log_config = config.get("logger")
        if log_config is not None:
            self._logger = getLogger("sksurgeryfred")

            log_file_name = log_config.get("log file name",
                                           "sksurgeryfred.log")
            overwrite = log_config.get("overwrite existing", False)

            mode = 'a'
            if overwrite:
                mode = 'w'

            file_handler = FileHandler(log_file_name, mode)

            formatter = Formatter('%(asctime)s - %(name)s -' +
                                  ' %(levelname)s - %(message)s')

            file_handler.setFormatter(formatter)

            self._logger.addHandler(file_handler)
            self._logger.setLevel(INFO)
            self._no_logging = False

    def log(self, message):
        """If logging, passes message to logger"""
        if self._no_logging:
            return

        self._logger.info(message)

    def __del__(self):
        """Releases the log file"""
        if not self._no_logging:
            self._logger.handlers[0].flush()
            self._logger.handlers[0].close()
