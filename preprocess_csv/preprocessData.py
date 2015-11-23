#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import csv
csv.field_size_limit(sys.maxint)

import re
import string
import nltk
import unicodedata
import optparse

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem.porter import PorterStemmer

from random import randint

__version__ = 'r7 (2014/09/25)'


def parse_command_line(argv):
    """Command line options parser for the script
    """
    usage = "Usage: %prog [options] <CSV input file>"

    parser = optparse.OptionParser(usage=usage)
    parser.add_option("-b", "--begin", action="store",
                      type="int", dest="begin", default=1,
                      help="Begin row number (default: 1)")
    parser.add_option("-e", "--end", action="store",
                      type="int", dest="end", default=0,
                      help="End row number (default: 0)")
    parser.add_option("-r", "--random", action="store",
                      type="int", dest="random", default=100,
                      help="Percent random sampling (default: 100)")
    parser.add_option("-c", "--column", action="store",
                      type="string", dest="column", default="Body",
                      help="Data column to be cleaned (default: 'Body')")
    parser.add_option("-k", "--keep", action="store_true",
                      dest="keep", default=False,
                      help="Keep original data column (default: No)")
    parser.add_option("-o", "--outfile", action="store",
                      type="string", dest="outfile", default="cleaned.csv",
                      help="Clean output CSV filename"
                           " (default: 'cleaned.csv')")
    parser.add_option("--append", action="store_true",
                      dest="append", default=False,
                      help="Append if output CSV exists (default: No)")
    parser.add_option("--keep-accented", action="store_true",
                      dest="keep_accented", default=False,
                      help="Keep accented (default: No)")
    parser.add_option("--keep-punct", action="store_true",
                      dest="keep_punct", default=False,
                      help="Keep punctuation (default: No)")
    parser.add_option("--keep-stopwords", action="store_true",
                      dest="keep_stopwords", default=False,
                      help="Keep stopwords (default: No)")
    parser.add_option("--keep-numbers", action="store_true",
                      dest="keep_numbers", default=False,
                      help="Keep numbers and words that begin with numbers"
                           " (default: No)")
    parser.add_option("--keep-stems", action="store_true",
                      dest="keep_stems", default=False,
                      help="Keep Stems (default: No)")

    return parser.parse_args(argv)


def to_unicode(s):
    """Returns unicode string
    """

    if not isinstance(s, unicode):
        try:
            s = unicode(s, errors='ignore')
        except:
            s = u""
    return s


def remove_accented(s):
    """Removes accented chars and lower case
    """

    s = ''.join(c for c in unicodedata.normalize('NFD', s.lower())
                if unicodedata.category(c) != 'Mn')
    return s


def regexp_word_tokenize(s):
    """Simple word tokenizer using Regular Expression
    """
    return re.compile(r"\b\w\w+\b", re.U).findall(s)


def stemmed(words):
    """Returns stemmed words
    """
    st = PorterStemmer()
    stemmed_words = []
    for w in words:
        try:
            stemmed_words.append(st.stem(w))
        except:
            print("WARN: cannot stem '%s'" % (w))
    return stemmed_words


def remove_stopwords(words, swords=None):
    """Remove stopwords
    """
    if swords is None:
        nltk.data.path.append("./nltk_data")
        try:
            swords = stopwords.words('english')
        except:
            nltk.download('stopwords', './nltk_data')
            swords = stopwords.words('english')
    words = [w for w in words if w not in swords]
    return words


def remove_punctuation(words):
    """Remove punctuation
    """

    punct_regex = re.compile('[%s]' % re.escape(string.punctuation))
    nopunct_words = []
    for w in words:
        nw = punct_regex.sub(u'', w)
        if nw != u'':
            nopunct_words.append(nw)
    return nopunct_words


def remove_numbers(words):
    """Remove numbers and words that start with numbers
    """

    new_words = []
    for w in words:
        if not re.match(r"\d+.*", w):
            new_words.append(w)
    return new_words


if __name__ == "__main__":
    print("%s - %s\n" % (os.path.basename(sys.argv[0]), __version__))
    (options, args) = parse_command_line(sys.argv)
    if len(args) < 2:
        print("Usage: %s [options] <CSV input file>" %
              os.path.basename(sys.argv[0]))
        sys.exit(-1)

    print(options)

    if not os.path.isfile(options.outfile):
        o = open(options.outfile, 'wb')
    else:
        if options.append:
            o = open(options.outfile, 'ab' if options.append else 'wb')
        else:
            overwrite = raw_input("File '%s' exists, overwrite? (Y/n): " %
                                  options.outfile).lower() != 'n'
            if overwrite:
                o = open(options.outfile, 'wb')
            else:
                sys.exit(-2)

    f = open(args[1])
    reader = csv.DictReader(f)
    if options.column not in reader.fieldnames:
        print("ERROR: Specified text column not found ('%s')" % options.column)
        print("There are following columns in '%s' :-" % args[1])
        for c in reader.fieldnames:
            print "- %s" % (c)
        sys.exit()

    ncols = len(reader.fieldnames)
    if options.keep:
        cols = reader.fieldnames + ['<cleaned>%s' % options.column]
    else:
        cols = reader.fieldnames
    writer = csv.DictWriter(o, cols)
    if not options.append:
        writer.writeheader()
    i = 0
    count = 0
    for r in reader:
        if i % 100 == 0:
            if i < options.begin - 1:
                print("Skipped row: %d" % i)
            else:
                print("Cleaning row: %d" % i)
        i += 1
        if i < options.begin:
            continue
        if options.end != 0 and i > options.end:
            break
        if len(r) != ncols:
            print("WARN: row #%d is corrupted" % i)
            continue
        if randint(0, 100) > options.random:
            continue
        body = r[options.column]
        s = to_unicode(body)
        if not options.keep_accented:
            # convert to lowercase and remove accentuated
            s = remove_accented(s)
        # Word with punctuation tokenizer
        words = word_tokenize(s)
        #words = regexp_word_tokenize(body)
        if not options.keep_punct:
            # Remove punctuation
            words = remove_punctuation(words)
        if not options.keep_stopwords:
            # Remove stopwords
            words = remove_stopwords(words)
        if not options.keep_numbers:
            # Remove numbers and words start with numbers
            words = remove_numbers(words)
        if not options.keep_stems:
            # Stemmed
            words = stemmed(words)
        if options.keep:
            r['<cleaned>%s' % options.column] = ' '.join(words)
        else:
            r[options.column] = ' '.join(words)
        writer.writerow(r)
        count += 1
    print("Complete total: %d rows" % count)
    f.close()
    o.close()
