import sys
import inspect

class Error():
    def error(self, message, line, stop = False):
        print('ERROR: ' + message, "(" + str(line) + ")" )
        if stop:
            sys.exit()

    def lineon(self):
        # Determines the current line in the program
        return inspect.currentframe().f_back.f_lineno
