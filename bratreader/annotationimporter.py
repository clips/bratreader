import os

from io import open
from collections import OrderedDict, defaultdict
from annotation import Annotation
from sentence import Sentence


def importann(pathtofile):
    """
    Import ann and .txt files from a folder.

    :param pathtofile: (string) the path to the folder containing both the
    .ann and .txt files.
    :return: a tuple containing a dictionary of annotations and a string,
    representing the text of the document
    """
    annotations = readannfile(pathtofile)
    path, extension = os.path.splitext(pathtofile)

    sentences = []

    char_index = 0

    for sent_index, line in enumerate(open(path + ".txt")):
        sentences.append(Sentence(sent_index, line, char_index))
        char_index += len(line)+1

    _join(annotations.values(), sentences)
    return sentences


def _join(annotations, sentences):
    """
    join a list of annoations with a list of sentences.

    :param annotations: list of annotations
    :param sentences:
    :return:
    """
    for ann in annotations:
        for span in ann.spans:

            begin, end = span

            for s in sentences:
                words = s.getwordsinspan(begin, end)
                ann.words.extend(words)
                for w in words:
                    w.annotations.append(ann)


def _createannotationobjects(annotations):
    """
    Create instances of the Annotation class for each of the "T" annotations.

    Input is assumed to only be "T" annotations.

    :param annotations: (dict) dictionary of "T" annotations.
    :return: (OrderedDict) an ordered dictionary of Annotations objects.
    Length of this dictionary should be equal to the input dictionary.
    """
    targets = OrderedDict()

    for key, t in annotations.items():
        splitted = t.split("\t")
        t = splitted[0]
        repr = " ".join(splitted[1:])

        split = t.split()
        label = split[0]

        spans = [[int(span.split()[0]), int(span.split()[1])]
                 for span in u" ".join(split[1:]).split(";")]

        targets[key] = Annotation(key, repr, spans, [label])

    return targets


def _find_t(e, annotations):
    """
    Given an "E" annotation from an .ann file, find the "T" annotation.

    Because "E" annotations can be nested, the search should be done on deeper
    levels.

    :param e: (string) the "E" annotation we want to find the target of.
    :param annotations: (dict) the dict of annotations.
    :return: the keys of "T" annotations this e annotation points to.
    """
    e = e.split()
    keys = []

    if len(e) > 1:

        targetkeys = [y for y in [x.split(":")[1] for x in e[1:]]]

        for key in targetkeys:
            if key[0] == "E":
                keys.append(annotations['E'][key[1:]].split()[0].split(":")[1])

            if key[0] == "T":
                keys.append(key)

    return keys


def _evaluate_annotations(annotations):
    """
    Evaluate all annotations for an .ann file.

    Each category of annotations (i.e. "T","E","A","R","N") are treated
    separately. First, all "T" annotations are rewritten to Annotation objects,
    as these are the ultimate targets of all expressions.

    Then the "A" annotations, which contain valencies for expressions
    and targets are evaluated. Third, "E" annotations, which are event
    expressions (which can get a valency from "A") are evaluated.

    Finally, "R" and "N" annotations, which are separate from the others,
    are evaluated.

    :param annotations: (dict of dict) a dictionary of dictionaries,
    the first dictionary has a key for each annotation category
    (i.e. "T","E","A","R","N"). The second contains a second number to
    differentiate annotations. This is all based on the .ann file.
    All keys, even number keys, are strings, to guarantee compatibility with
    other versions.

    Example: in the ann file we have an annotation "T14". This is added to
    the dictionary "T" as key "14".

    :return: a dictionary of Annotation objects.
    """

    # Create the annotation objects
    annotationobjects = _createannotationobjects(annotations["T"])

    # "A" annotations
    for a in annotations["A"].values():
        try:
            # Triple format (e.g. Sentiment T14 Positive)
            label, key, valency = a.split()
        except ValueError:
            # Only a label, no valency (e.g. Target T14)
            label, key = a.split()
            valency = ""

        # Type of target (e.g. "T")
        type = key[0]
        id = key[1:]

        if type == "E":

            tempe = annotations["E"][id]
            key2 = tempe.split()[0].split(":")[1][1:]
            annotationobjects[key2].labels[label].append(valency)

        elif type == "T":

            annotationobjects[id].labels[label].append(valency)

    # "E" annotations
    for e in annotations["E"].values():

        # function returns the id of T.
        targetkeys = _find_t(e, annotations)
        origintype, originkey = e.split()[0].split(":")
        originkey = originkey[1:]

        targets = [x[1:] for x in targetkeys]

        for x in targets:
            t = annotationobjects[originkey]
            annotationobjects[x].links[origintype].append(t)

    # "R" annotations
    for r in annotations["R"].values():

        r = r.split()

        if len(r) > 1:

            origintype = r[0]
            originkey = r[1].split(":")[1][1:]
            targets = [y for y in [x.split(":")[1][1:] for x in r[2:]]]

            for x in targets:
                t = annotationobjects[originkey]
                annotationobjects[x].links[origintype].append(t)

    return annotationobjects


def readannfile(filename):
    """
    Read an .ann file and returns a dictionary containing dictionaries.

    :param filename: (string) the filename of the .ann file.
    :return: (dict of dict) a dictionary of dictionaries representing the
    annotations.
    """
    anndict = defaultdict(dict)
    with open(filename, encoding='utf-8') as f:
        for index, line in enumerate(f):

            begin = line.rstrip().split("\t")[0]
            rest = line.rstrip().split("\t")[1:]

            try:
                anndict[begin[0]][begin[1:]] = u"\t".join(rest)
            except IndexError:
                continue

    return _evaluate_annotations(anndict)
