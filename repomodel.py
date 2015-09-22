# -*- coding: utf-8 -*-
from annotateddocument import AnnotatedDocument
from xml import importxml
from ann_filehandler import importann

import os


class RepoModel(object):
    """
    A class for modeling a local repository annotated with the Brat Rapid Annotation Tool. (http://brat.nlplab.org)

    Corpora annotated with Brat use 2 files for each document in the corpus: an .ann file
     containing the annotations in Brat Standoff Format (http://brat.nlplab.org/standoff.html),
     and a .txt file containing the actual text. This tool takes a folder containing pairs of these
     files as input, and creates a RepoModel object. This RepoModel object can be exported in an
     XML format, or operated on in memory.

    Currently the program ignores Notes, or # annotations.
    """

    def __init__(self, pathtorepo, fromxml=False):
        """
        Creates a RepoModel object.

        :param pathtorepo: (string) the path to a local repository, which contains pairs of .ann and .txt files. No checking
         is done to guarantee that the repository is consistent.
        :param fromxml: (bool) True if the local repository is in the .xml format produced by this program. Useful for
         saving RepoModels.
        :return: None
        """

        # Each document is saved as a textunit.
        self._documents = {}

        if os.path.isdir(pathtorepo):

            suffix = ".xml" if fromxml else ".ann"

            # Select the relevant import function
            importpath = importxml if fromxml else importann

            paths = [path for path in os.listdir(pathtorepo) if path.endswith(suffix)]
            for path in paths:

                # The key of each document is the document name without the suffix (i.e. "001.ann" becomes "001")
                key = u".".join(path.split('.')[:-1])
                annotations, context = importpath("/".join([pathtorepo, path]))
                self._documents[key] = AnnotatedDocument(key, context, annotations)

        else:
            raise IOError(u"{0} is not a valid directory".format(pathtorepo))

    @property
    def documents(self):
        return self._documents

    def export_xml_corpus(self, pathtofolder):
        """
        Exports a RepoModel as a XML to the specified folder. If the folder doesn't exist, it is created.
        No assumptions are made about the underlying filesystem or permissions.

        :param pathtofolder: (string) the path to the folder where the XML should be exported.
        :return: None
        """

        if not os.path.isdir(pathtofolder):
            os.mkdir(pathtofolder)
        # Guarantee that pathtofolder ends with a slash.
        pathtofolder = pathtofolder if pathtofolder.endswith("/") else "{0}/".format(pathtofolder)

        for document in self._documents.values():
            document.export_xml(pathtofolder+str(document.key)+".xml")