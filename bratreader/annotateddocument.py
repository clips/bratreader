from itertools import chain
from lxml import etree


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

        self.text = u"\n".join([u" ".join([x.form for x in s.words])
                               for s in sentences])

    def export_xml(self, pathtofile):
        """
        Export the current document to an XML file at the specified location.

        :param pathtofile: The path where the .XML file needs to be saved.
        :return: None
        """
        document = etree.Element("document", source=self.key)

        sentences = etree.Element("sentences")
        for s in self.sentences:

            sentence = etree.Element("sentence", id="s.{0}".format(s.key),
                                     start=str(s.start),
                                     end=str(s.end))

            for w in s.words:

                word = etree.Element("word",
                                     start=str(w.start),
                                     end=str(w.end),
                                     id="s.{0}.w.{1}".format(w.sentkey, w.key))
                word.text = w.form
                sentence.append(word)

            sentences.append(sentence)

        document.append(sentences)

        annotations = etree.Element("annotations")

        for v in self.annotations:

            annotations.append(etree.Element("annotation",
                                             id=str("ann{0}".format(v.id))))
            ann = annotations.getchildren()[-1]

            ann.set("words", u" ".join(["s.{0}.w.{1}".format(w.sentkey, w.key)
                                       for w in v.words]))
            ann.set("repr", v.repr)
            ann.set("spans", u",".join(["|".join([str(y) for y in x])
                                      for x in v.spans]))

            for label, valency in v.labels.items():
                ann.set(str(label), "|".join(valency))

            for linktype, linked in v.links.items():

                linked = u" ".join(["ann{0}".format(link.id) for link in linked])
                ann.set(str("link.{0}".format(linktype)), linked)

        document.append(annotations)

        with open(pathtofile, 'w') as f:
            etree.ElementTree(document).write(f, pretty_print=True)
