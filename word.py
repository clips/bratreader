__author__ = 'stephantulkens'


class Word(object):

    def __init__(self, key, sentkey, form, start, end):

        self.key = key
        self.sentkey = sentkey
        self.form = form
        self.start = start
        self.end = end

    def __repr__(self):

        return self.form
