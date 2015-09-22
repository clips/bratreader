# -*- coding: utf-8 -*-

from lxml import etree
import hashlib


class AnnotatedDocument(object):
    """
    This class represents a document in a brat corpus.
    """

    def __init__(self, key, sentences, annotations):
        """
        Creates a brat document

        :param key: (string) The key of the document. Generally the name of the file without the extension
        (e.g. "022.ann" becomes 022)
        :param sentences: A list of dictionaries containing words. Represents the text of the review on a word-by-word
        basis.
        :param annotations: A dictionary of dictionaries containing Annotation objects. Represents the annotations.
        :return: None
        """

        self.sentences = sentences

        self.key = key
        self.annotations = annotations

        # Every review has a hash key, which is the MD5 hash of the text of the review. Made for comparing documents
        # Across different Brat corpora.

        self.text = "\n".join([" ".join([x.form for x in s.words]) for s in sentences])

        self.hashkey = hashlib.md5(self.text.encode("utf-8")).hexdigest()

    def __repr__(self):

        return str(self.hashkey)

    def export_xml(self, pathtofile):
        """
        Exports the current document to an XML file at the specified location.

        :param pathtofile: The path where the .XML file needs to be saved.
        :return: None
        """

        document = etree.Element("document", source=self.key, md5=self.hashkey)

        sentences = etree.Element("sentences")
        for s in self.sentences:

            sentence = etree.Element("sentence", id="s.{0}".format(s.key), start=str(s.start), end=str(s.end))

            for w in s.words:

                word = etree.Element("word", start=str(w.start), end=str(w.end), id="s.{0}.w.{1}".format(w.sentkey, w.key))
                word.text = w.form
                sentence.append(word)

            sentences.append(sentence)

        document.append(sentences)

        annotations = etree.Element("annotations")

        for k, v in self.annotations.items():

            annotations.append(etree.Element("annotation", id=str("ann{0}".format(k))))
            ann = annotations.getchildren()[-1]

            ann.set("words", " ".join(["s.{0}.w.{1}".format(w.sentkey, w.key) for w in v.words]))
            ann.set("repr", v.repr)
            ann.set("spans", ",".join(["|".join([str(y) for y in x]) for x in v.spans]))

            for label, valency in v.labels.items():
                ann.set(str(label), "|".join(valency))

            for linktype, linked in v.links.items():

                linked = " ".join(["ann{0}".format(link.id) for link in linked])
                ann.set(str("link.{0}".format(linktype)), linked)

        document.append(annotations)

        with open(pathtofile, 'w') as f:
            etree.ElementTree(document).write(f, pretty_print=True)