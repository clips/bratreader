__author__ = 'stephantulkens'


class Word(object):

    def __init__(self, key, sentkey, form, start, end):
        """
        Define a word object.

        :param key: The key of the document to which this belongs.
        :param sentkey: The key of the sentence to which this word belongs.
        :param form: The string form of this word.
        :param start: The start index of this word.
        :param end: The end index of this word.
        """
        self.key = key
        self.sentkey = sentkey
        self.form = form
        self.start = start
        self.end = end
        self.annotations = []

    def __repr__(self):
        """Form."""
        return self.form
