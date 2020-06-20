# Developed by A N Zeyn

import logging
import sys


class LogPlus:
    """
    LogPlus has been created to add extra steps to logging.
    LogPlus can automate the following in a single line of code:
        - logging the log messages to the log file
        - printing the log messages to the console
        - exiting program if necessary
    """
    def __init__(self, log_file_name_or_path):

        self.log_file_name_or_path = log_file_name_or_path

        logging.basicConfig(
                filename=self.log_file_name_or_path,
                filemode='w',
                level=logging.DEBUG,
                format='%(name)s - %(asctime)s - %(process)d - %(levelname)s - %(message)s',
                datefmt='%d-%b-%y %H:%M:%S'
        )
        logging.info('Logger is on')

    def log_plus(self, action_code, log_msg):
        """
            log_plus action codes:
                usage format (order matters): [p][l][<log_level>][x]
                examples: plix, ld, lex, etc.
                    l: log to the log file
                    p: log to the console
                    x: exit the program
                    c: CRITICAL (50)
                    e: ERROR (40)
                    w: WARNING (30)
                    i: INFO (20)
                    d: DEBUG (10)
                    n: NOTSET (0)
        """
        if 'p' in action_code:
            print(log_msg)
        if 'lc' in action_code:
            logging.critical(log_msg)
        if 'le' in action_code:
            logging.error(log_msg)
        if 'lw' in action_code:
            logging.warning(log_msg)
        if 'li' in action_code:
            logging.info(log_msg)
        if 'ld' in action_code:
            logging.debug(log_msg)
        if 'x' in action_code:
            sys.exit()

"""
Usage example:
    log_obj = logplus.LogPlus("c:/Users/z3/AppData/Local/Programs/Python/Python37/Scripts/code/z3.log")
    log_obj.log_plus('p', 'Some print line ...')
    log_obj.log_plus('li', 'Some log info line ...')
    log_obj.log_plus('ple', 'Some print and log error line ...')
    log_obj.log_plus('plex', 'Some print and log error and exit line ...')
    print("I won't print :(")
"""