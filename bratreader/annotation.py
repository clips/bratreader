# -*- coding: utf-8 -*-
from collections import defaultdict


class Annotation(object):
    """This class represents an annotation."""

    def __init__(self, id, representation, spans, labels=()):
        """
        Create an annotation object.

        :param id: (string) The id of the current annotation.
        :param representation: (string) The string representation of the
        annotation. Doesn't take into account the fact that annotations may be
        discontinous.
        :param spans: (list of list of ints) A list of list of ints
        representing the starting and ending points, in characters, for any
        words in the annotation.
        :param labels: (list of strings) a list of initial labels for the
        annotation object. These never get an initial value.
        :return: None
        """
        self.id = id
        self.links = defaultdict(list)
        self.labels = defaultdict(list)
        for label in labels:
            self.labels[label] = []
        self.repr = representation
        self.spans = spans
        self.realspan = (spans[0][0], spans[-1][1])
        self.words = []

    def __repr__(self):
        """Representation of the annotation."""
        return "Annotation: {0}".format(self.repr.encode("utf-8"))
