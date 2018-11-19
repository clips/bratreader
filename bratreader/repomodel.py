from bratreader.annotateddocument import AnnotatedDocument
from bratreader.annotationimporter import importann
from glob import iglob

import os


class RepoModel(object):
    """
    A class for modeling a local repository annotated with BRAT.

    Corpora annotated with Brat use 2 files for each document in the corpus:
    an .ann file containing the annotations in Brat Standoff Format
    (http://brat.nlplab.org/standoff.html), and a .txt file containing the
    actual text. This tool takes a folder containing pairs of these files as
    input, and creates a RepoModel object. This RepoModel object can be
    exported in an XML format, or operated on in memory.

    Currently the program ignores Notes, or # annotations.
    """

    def __init__(self, pathtorepo):
        """
        Create a RepoModel object.

        :param pathtorepo: (string) the path to a local repository, which
        contains pairs of .ann and .txt files. No checking is done to guarantee
        that the repository is consistent.
        :return: None
        """
        # Each document is saved as a textunit.
        self.documents = {}

        if os.path.isdir(pathtorepo):
            for path in iglob("{0}/*.ann".format(pathtorepo)):

                # The key of each document is the document name without
                # the suffix (i.e. "001.ann" becomes "001")
                key = os.path.splitext(path)[0]
                key = os.path.split(key)[-1]
                context = importann(path)
                self.documents[key] = AnnotatedDocument(key, context)

        else:
            raise IOError(u"{0} is not a valid directory".format(pathtorepo))

    def save_xml(self, pathtofolder):
        """
        Export a RepoModel as a XML to the specified folder.

        If the folder doesn't exist, it is created.
        :param pathtofolder: (string) the path to the folder where the XML
        should be exported.
        """
        if not os.path.isdir(pathtofolder):
            os.mkdir(pathtofolder)

        for document in self.documents.values():
            path = os.path.join(pathtofolder,
                                "{0}.xml".format(str(document.key)))
            document.export_xml(path)
