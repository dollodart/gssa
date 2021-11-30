from time import time, sleep
class Checker:
    hourly_limit = 100000

    def __init__(self, logger, cum_search=0, fail_thresh=10):
        self.cum_search = cum_search
        self.fail = 0
        self.fail_thresh = fail_thresh
        self.logger = logger

    def increment(self):
        self.cum_search += 1
        if self.cum_search > self.hourly_limit * 0.95:
            self.logger.info('##\n'
                         f'past hourly limit of {self.hourly_limit}, sleeping until limit refresh')
            sleep(3600)
            self.cum_search = 0

    def increment_failure(self):
        self.fail += 1
        if self.fail > self.fail_thresh:
            i = input(
                'there have been greater than 10 failures, continue? [y/N]: ')
            if i == 'y':
                fail_thresh = input(
                    'input an integer number for failure threshold [10]: ')
                while True:
                    if fail_thresh:
                        try:
                            self.fail_thresh = int(fail_thresh)
                            break
                        except ValueError:
                            fail_thresh = input(
                                'try again, input an integer number of failures [10]: ')
                    else:
                        self.fail_thresh = 10
                        break
            self.fail = 0


class Indent:
    def __init__(self):
        self.indent = 0
    def __add__(self, other): 
        # should also be used for __radd__ in case of `3 + indent` or similar
        if type(other) is int:
            self.indent += other
            return self
        elif type(other) is Indent:
            self.indent += other.indent
            return self
        elif type(other) is str:
            return str(self) + other
    def __radd__(self, other):
        if type(other) is int:
            self.indent += other
            return self
        elif type(other) is Indent:
            self.indent += other.indent
            return self
        elif type(other) is str:
            return other + str(self)
    def __sub__(self, other):
        if type(other) is int:
            self.indent -= other
        elif type(other) is Indent:
            self.indent += other.indent
        return self
    def __str__(self):
        if self.indent > 0:
            return f' (l={self.indent}) '
        return ' (l=0) '
