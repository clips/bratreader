__author__ = 'stephantulkens'
from word import Word

class Sentence(object):

    def __init__(self, key, line, start):

        self.key = key
        self._words = []
        self.start = start
        self.end = start + len(line)

        for windex, w in enumerate(line.split()):

            start = start
            end = start+len(w)

            self._words.append(Word(key=windex, sentkey=self.key, form=w, start=start, end=end))

            start = end+1

    @property
    def words(self):
        return self._words

    def getwordsinspan(self, start, end):

        return [word for word in self._words if (word.start <= start < word.end)
                or (word.start < end <= word.end)
                or (start < word.start < end and start < word.end < end)]

    def __repr__(self):

        return " ".join([x.repr for x in self._words])