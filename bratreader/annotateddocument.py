from itertools import chain


class AnnotatedDocument(object):
    """Represent a document in a Brat Corpus."""

    def __init__(self, key, sentences):
        """
        Create a brat document.

        :param key: (string) The key of the document.
        Generally the name of the file without the extension
        (e.g. "022.ann" becomes 022)
        :param sentences: A list of dictionaries containing words.
        Represents the text of the review on a word-by-word basis.
        :return: None
        """
        self.sentences = sentences
        annotations = [chain.from_iterable([w.annotations for w in x.words])
                       for x in sentences]
        self.annotations = list(chain.from_iterable(annotations))

        self.key = key

        self.text = "\n".join([" ".join([x.form for x in s.words])
                               for s in sentences])
