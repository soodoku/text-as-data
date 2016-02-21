#!/usr/bin/env python
# -*- coding: utf-8 -*-

__version__ = 'r1 (2014/08/16)'

import os
import sys
import csv
csv.field_size_limit(sys.maxint)
import optparse
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer


def TDMReport(vec, X, opts):
    """
    # TDMReport(tdm)
           - Report most frequent, sparse
    """
    freq_df = pd.DataFrame({'term': vec.get_feature_names(),
                           'sum': np.asarray(X.sum(axis=0)).ravel().tolist()})
    freq_df['ratio'] = freq_df['sum']/np.sum(freq_df['sum'])

    print("Total terms: {0:d}".format(len(vec.vocabulary_)))
    print("Most frequent {0:d} terms: ".format(opts.n_freq))
    print freq_df.sort('sum', ascending=False).head(opts.n_freq)
    print("Most sparse {0:d} terms: ".format(opts.n_sparse))
    print freq_df.sort('sum', ascending=True).head(opts.n_sparse)

    return freq_df


def CreateTDM(df, opts):
    """
    # Document Term Matrix
    # CreateTDM(Traindata, labelColumn(s), textColumn, unigrams/bigrams/other?)
           - outputs a tdm
           - calls TDMReport(tdm)
    """
    vec = CountVectorizer(ngram_range=(opts.min_ngram, opts.max_ngram),
                          max_features=opts.max_features,
                          stop_words=opts.remove_terms)

    X = vec.fit_transform(df[opts.textColumn])

    return vec, X


def TFIDFReport(vec, X, opts):
    freq_df = pd.DataFrame({'term': vec.get_feature_names(),
                           'sum': np.asarray(X.sum(axis=0)).ravel().tolist()})
    freq_df['ratio'] = freq_df['sum']/np.sum(freq_df['sum'])

    print("Total terms: {0:d}".format(len(vec.vocabulary_)))
    print("Most frequent {0:d} terms: ".format(opts.n_freq))
    print freq_df.sort('sum', ascending=False).head(opts.n_freq)
    print("Most sparse {0:d} terms: ".format(opts.n_sparse))
    print freq_df.sort('sum', ascending=True).head(opts.n_sparse)

    return freq_df


def CreateTFIDF(X, opts):
    """
    # CreateTFIDF(Traindata, labelColumn, textColumns)
           - outputs a tf-idf
           - calls tdidfReport(tfidf)
    """
    tfidf = TfidfTransformer(norm="l2")

    X = tfidf.fit_transform(X)

    return X


def RemoveSparse(freq, opts):
    """
    # RemoveSparse(tdm, Y)
           # Remove sparse terms (terms which are very rare etc.)
           - Y is a way to subset tdm
           - automatically implement the default Y that is suggested
    """
    if opts.remove_n_sparse:
        head = freq.sort('sum', ascending=True).head(opts.remove_n_sparse)
        n_sparses = head['term'].tolist()
    else:
        n_sparses = []
    return n_sparses


def RemoveFrequent(freq, opts):
    """
    # RemoveFrequent(tdm, X)
           - Removes frequent terms
           - X is a way to subset tdm
           - automatically implement the default X that is suggested
    """
    if opts.remove_n_freq:
        head = freq.sort('sum', ascending=False).head(opts.remove_n_freq)
        n_frequents = head['term'].tolist()
    else:
        n_frequents = []

    return n_frequents


def parse_command_line(argv):
    """Command line options parser for the script
    """
    usage = "Usage: %prog [options] <CSV input file>"

    parser = optparse.OptionParser(usage=usage)

    parser.add_option("-t", "--text", action="store",
                      type="string", dest="textColumn", default="Body",
                      help="Text column name (default: 'Body')")
    parser.add_option("-l", "--labels", action="store",
                      type="string", dest="labelColumns",
                      default="Online Section",
                      help="Label column(s) name (default: 'Online Section')")
    parser.add_option("-d", "--delimiter", action="store",
                      type="string", dest="delimiter", default=";",
                      help="Delimeter use to split option's value if multiple"
                           " values (default: ';')")
    parser.add_option("--min-ngram", action="store",
                      type="int", dest="min_ngram", default=1,
                      help="Minimum ngram(s) (default: 1)")
    parser.add_option("--max-ngram", action="store",
                      type="int", dest="max_ngram", default=2,
                      help="Maximum ngram(s) (default: 2)")
    parser.add_option("--max-features", action="store",
                      type="int", dest="max_features", default=2**16,
                      help="Maximum features (default: 2**16)")
    parser.add_option("--n-freq", action="store",
                      type="int", dest="n_freq", default=20,
                      help="Report most frequent terms (default: 20)")
    parser.add_option("--n-sparse", action="store",
                      type="int", dest="n_sparse", default=20,
                      help="Report most sparse terms (default: 20)")
    parser.add_option("-r", "--remove-terms-file", action="store",
                      type="string", dest="remove_terms_file", default=None,
                      help="File name contains terms to be removed"
                           " (default: None)")
    parser.add_option("--remove-n-freq", action="store",
                      type="int", dest="remove_n_freq", default=0,
                      help="Top most of frequent term(s) to be removed"
                           " (default: 0)")
    parser.add_option("--remove-n-sparse", action="store",
                      type="int", dest="remove_n_sparse", default=0,
                      help="Top most of sparse term(s) to be removed"
                           " (default: 0)")
    parser.add_option("--out-tdm-file", action="store",
                      type="string", dest="out_tdm_file", default=None,
                      help="Save output TDM to CSV filename (default: None)")
    parser.add_option("--use-tfidf", action="store_true",
                      dest="use_tfidf", default=False,
                      help="Use TF-IDF (default: False)")
    parser.add_option("--out-tfidf-file", action="store",
                      type="string", dest="out_tfidf_file", default=None,
                      help="Save output TF-IDF to CSV filename (default: None)")

    return parser.parse_args(argv)


if __name__ == "__main__":
    print("{0!s} - {1!s}\n".format(os.path.basename(sys.argv[0]), __version__))
    (opts, args) = parse_command_line(sys.argv)
    if len(args) < 2:
        print("Usage: {0!s} [options] <CSV input file>".format(
              os.path.basename(sys.argv[0])))
        sys.exit(-1)

    print("Options: {0!s}".format(opts))

    opts.remove_terms = []

    if opts.remove_terms_file:
        try:
            opts.remove_terms = pd.read_csv(opts.remove_terms_file,
                                            header=None)[0].tolist()
        except:
            print("WARN: Cannot read remove terms file ({0!s})".format(
                  opts.remove_terms_file))

    print("Reading input file...({0!s})".format(args[1]))
    cols = [opts.textColumn] + opts.labelColumns.split(opts.delimiter)
    df = pd.read_csv(args[1], usecols=cols)
    print("Creating Term Document Matrix...")
    vec, X = CreateTDM(df, opts)
    freq = TDMReport(vec, X, opts)
    n_sparses = RemoveSparse(freq, opts)
    n_frequents = RemoveFrequent(freq, opts)
    out_df = pd.DataFrame(X.toarray(), columns=vec.get_feature_names())
    cols = out_df.columns - n_sparses - n_frequents
    ext_cols = opts.labelColumns.split(opts.delimiter)
    out_df = out_df[cols].join(pd.DataFrame(df[ext_cols]))
    if opts.out_tdm_file:
        print("Saving TDM output to CSV file... ({0!s})".format(opts.out_tdm_file))
        out_df.to_csv(opts.out_tdm_file, index_label='index')
    if opts.use_tfidf:
        print("Creating TF-IDF Matrix...")
        X = CreateTFIDF(X, opts)
        freq = TFIDFReport(vec, X, opts)
        n_sparses = RemoveSparse(freq, opts)
        n_frequents = RemoveFrequent(freq, opts)
        out_df = pd.DataFrame(X.toarray(), columns=vec.get_feature_names())
        cols = out_df.columns - n_sparses - n_frequents
        out_df = out_df[cols].join(pd.DataFrame(df[ext_cols]))
        if opts.out_tfidf_file:
            print("Saving TF-IDF output to CSV file... ({0!s})".format(
                  opts.out_tfidf_file))
            out_df.to_csv(opts.out_tfidf_file, index_label='index')
    print("Done!!!")
