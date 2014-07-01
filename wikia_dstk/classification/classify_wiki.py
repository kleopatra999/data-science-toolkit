import sys
import time
import numpy as np
from . import logger, Classifiers
from collections import OrderedDict, defaultdict
from sklearn.feature_extraction.text import TfidfVectorizer
from argparse import ArgumentParser, FileType


def get_args():
    ap = ArgumentParser()
    ap.add_argument(u'--num-processes', dest=u'num_processes', default=8)
    ap.add_argument(u'--classifiers', dest=u'classifiers', default=[], action=u"append")
    ap.add_argument(u'--infile', dest=u'infile', type=FileType(u'r'), default=sys.stdin)
    ap.add_argument(u'--class-file', dest=u'class_file', type=FileType(u'r'))
    ap.add_argument(u'--num-topicss', dest=u'num_topics', default=999)
    ap.add_argument(u'--outfile', dest=u'outfile', type=FileType(u'w'), default=sys.stdout)
    return ap.parse_args()


def main():
    start = time.time()
    args = get_args()

    if args.class_file:
        wid_to_class = OrderedDict()
        groups = OrderedDict()
        for line in args.class_file:
            splt = line.strip().split(',')
            groups[splt[1]] = groups.get(splt[1], []) + [int(splt[0])]
            wid_to_class[int(splt[0])] = splt[1]
        classes = groups.keys()

    logger.info(u"Loading CSV...")
    lines = [line.decode(u'utf8').strip() for line in args.infile if line.strip()]
    wid_to_features = OrderedDict([(int(splt[0]), u" ".join(splt[1:])) for splt in
                                   [line.split(u',') for line in lines]
                                   if int(splt[0]) in wid_to_class
                                   ])

    unknowns = OrderedDict([(int(splt[0]), u" ".join(splt[1:])) for splt in
                            [line.split(u',') for line in lines]
                            if int(splt[0]) not in wid_to_class
                            ])

    logger.info(u"Vectorizing...")
    vectorizer = TfidfVectorizer()
    feature_keys, feature_rows = zip(*[(classes.index(wid_to_class[int(key)]), features)
                                       for key, features in wid_to_features.items()
                                       if int(key) in wid_to_class])

    vectorizer.fit_transform(feature_rows)
    logger.info(u"Vectorized feature rows")
    training_vectors = vectorizer.transform(feature_rows).toarray()
    logger.info(u"Vectorized training features")

    logger.info(u"Training %d classifiers" % len(args.classifiers))

    classifiers = dict()
    for classifier_string in args.classifiers:
        clf = Classifiers.get(classifier_string)
        classifier_name = Classifiers.classifier_keys_to_names[classifier_string]

        logger.info(u"Training a %s classifier on %d instances..." % (classifier_name, len(training_vectors)))
        clf.fit(training_vectors, feature_keys)
        classifiers[classifier_string] = clf
        logger.info(u"Trained.")

    for counter, (wid, unknown) in enumerate(unknowns.items()):
        prediction_matrix = [classifier.predict_proba(vectorizer.transform([unknown]).toarray())
                             for classifier in classifiers.values()]
        print prediction_matrix
        summed_probabilities = np.sum(prediction_matrix, axis=0)[0]
        print summed_probabilities
        unknown_class = classes[list(summed_probabilities).index(max(summed_probabilities))]
        print wid, unknown_class
        args.outfile.write(u"%s,%s" % (wid, unknown_class))

    logger.info(u"Finished in %.2f seconds" % (time.time() - start))


if __name__ == u'__main__':
    main()