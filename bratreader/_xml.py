__author__ = 'stephantulkens'

from lxml import etree
from collections import OrderedDict
from annotation import Annotation
from sentence import Sentence

import codecs


def importxml(filename):
    """
    Import an XML file formatted with the format created by this program.

    Used for persistency and to operate on RepoModels in memory.

    :param filename: (string) the path to the file to be imported.
    :return: A tuple containing a dictionary of annotations and a list of
    dictionaries representing the context.
    """
    anndict = OrderedDict()
    sentobjects = []

    with codecs.open(filename, 'r', encoding='utf-8') as f:
        data = f.read()

    doc = etree.fromstring(data)

    sentences, annotations = doc.getchildren()

    for s in sentences.getchildren():

        repr = " ".join([w.text for w in s.getchildren()])
        sentobjects.append(Sentence(key=s.get('id').split(".")[1],
                                    line=repr,
                                    start=int(s.get("start"))))

    for annotation in annotations.getchildren():

        id = annotation.get('id')[3:]
        repr = annotation.get('repr')
        spans = [[int(y) for y in x.split("|")]
                 for x in annotation.get('spans').split(",")]

        ann = Annotation(id, repr, spans)

        for span in ann.spans:
            for s in sentobjects:

                start, end = span
                ann.words.extend(s.getwordsinspan(start, end))

        anndict[id] = ann

    for annotation in annotations.getchildren():

        id = annotation.get('id')[3:]
        ann = anndict[id]

        for x, y in {x: y for x, y in annotation.attrib.items()
                     if x not in ["id", "repr", "spans", "words"]}.items():

            if x.startswith("link."):
                ann.links[x[5:]].extend([anndict[key[3:]] for key in y.split()])
            else:
                ann.labels[x].append(y)

    return anndict, sentobjects
