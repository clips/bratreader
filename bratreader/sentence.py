from word import Word


class Sentence(object):

    def __init__(self, key, line, start):
        """
        Sentence object.

        :param key: The key to which this sentence belongs.
        :param line: The line on which this sentences occurs.
        :param start: The start index of this line in characters.
        """
        self.key = key
        self.words = []
        self.start = start
        self.end = start + len(line)

        for windex, w in enumerate(line.split()):

            start = start
            end = start+len(w)

            self.words.append(Word(key=windex,
                                   sentkey=self.key,
                                   form=w,
                                   start=start,
                                   end=end))
            start = end+1

    def getwordsinspan(self, start, end):
        """
        Retrieve all words in the specified character span.

        :param start: The start index in characters.
        :param end: The end index in characters.
        :return a list of words that fall inside the span.
        """
        return [word for word in self.words if
                (word.start <= start < word.end)
                or (word.start < end <= word.end)
                or (start < word.start < end and start < word.end < end)]

    def __repr__(self):
        """Representation as string."""
        return " ".join([x.form for x in self.words])
