#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import csv
csv.field_size_limit(sys.maxint)
import optparse

import random
import pandas as pd

__version__ = 'r3 (2014/12/25)'


def parse_command_line(argv):
    """Command line options parser for the script
    """
    usage = "Usage: %prog [options] <CSV input file>"

    parser = optparse.OptionParser(usage=usage)

    parser.add_option("-c", "--column", action="store",
                      type="string", dest="column", default="Online Section",
                      help="Label column name (default: 'Online Section')")
    parser.add_option("-d", "--delimiter", action="store",
                      type="string", dest="delimiter", default=";",
                      help="Delimiter used to split label if multiple labels (default: ';')")

    parser.add_option("-o", "--outfile", action="store",
                      type="string", dest="outfile", default="subset.csv",
                      help="Subseting output CSV filename (default: 'subset.csv')")

    parser.add_option("-r", "--remove", action="store",
                      type="string", dest="remove", default="NA",
                      help="Labels name to be removed (default: 'NA')")
    parser.add_option("-b", "--begin", action="store",
                      type="int", dest="begin", default=1,
                      help="Begin row number (default: 1)")
    parser.add_option("-e", "--end", action="store",
                      type="int", dest="end", default=0,
                      help="End row number (default: 0)")

    parser.add_option("--selected-cols", action="store",
                      type="string", dest="selected_cols", default=None,
                      help="Selected columns name (default: 'All')")

    parser.add_option("-s", "--size", action="store",
                      type="int", dest="size", default=0,
                      help="Random size (default: 0)")

    parser.add_option("-n", "--n-per-label", action="store",
                      type="int", dest="nperlabel", default=0,
                      help="N per label (stratified) (default: 0)")

    parser.add_option("--no-report", action="store_true",
                      dest="noreport", default=False,
                      help="Don't report data statistics (default: False)")

    return parser.parse_args(argv)


class LabelsStat(object):
    """ Label statistics data
    """
    def __init__(self):
        self._count = 0
        self._labels = dict()

    @property
    def count(self):
        return self._count

    @count.setter
    def count(self, value):
        self._count = value

    @property
    def labels(self):
        return self._labels

    @labels.setter
    def labels(self, value):
        self._labels = value


def DataReport(filename, labelColumn, options):
    """DataReport(labelColumn)
           Report certain features of the data
            - Takes the argument (labelColumn)
            - Total number of rows
            - Reports total # of unique labels
            - Reports total number of rows per unique label
            - Runs automatically when script is called
    """
    with open(filename) as f:
        reader = csv.DictReader(f)
        if labelColumn not in reader.fieldnames:
            print("ERROR: Specified label column not found ('%s')" % labelColumn)
            print("There are following columns in '%s' :-" % filename)
            for c in reader.fieldnames:
                print "- %s" % (c)
            return
        count = 0
        all_labels = dict()
        nlabels = dict()
        for i, r in enumerate(reader):
            if i % 10000 == 0:
                if i < options.begin - 1:
                    print("Skipped: #%d" % i)
                else:
                    print("Processed: %d" % i)
            if i < options.begin - 1:
                continue
            if options.end != 0 and i >= options.end:
                break
            data = r[labelColumn]
            if data is None:
                continue
            # Process here
            labels = [l.strip() for l in data.split(options.delimiter)
                      if l.strip() != '']
            n = len(labels)
            if n not in nlabels:
                nlabels[n] = LabelsStat()
            nlabels[n].count += 1
            for l in labels:
                if l not in nlabels[n].labels:
                    nlabels[n].labels[l] = 0
                nlabels[n].labels[l] += 1
            if n >= 1:
                l = '|'.join(sorted(labels))
                if l not in all_labels:
                    all_labels[l] = 0
                all_labels[l] += 1
                count += 1
        print("-"*80)
        print("================================ Data Report ================================")
        print("Label column: '%s' (delimiter: '%s')" % (labelColumn,
                                                        options.delimiter))
        print("Total Number of labeled articles: %d" % (count))
        print("Number of distinct labels: %d" % (len(all_labels)))
        n = 0
        for l in sorted(all_labels, key=all_labels.get, reverse=True):
            n += all_labels[l]
            print("%-70s %6d" % (l, all_labels[l]))
        print("============================== Label Statistics ==============================")
        print("Maximum number of multiple labels: %d" %
              sorted(nlabels.keys())[-1])
        for n in nlabels:
            print '-'*80
            print("N = %d (%d articles)" % (n, nlabels[n].count))
            for l in sorted(nlabels[n].labels, key=nlabels[n].labels.get,
                            reverse=True):
                print("%-70s %6d" % (l, nlabels[n].labels[l]))
        print("-"*80)


def SelectRows(data, options):
    """SelectRows(labelColumn, removeLabels)
           Selecting a subset of the data
            - Takes the arguments: labelColumn, removeLabels
            - Takes the following arguments: column name of labels,
              a list of labels that are not needed and returns dataset
              without rows which have labels that are not needed.
    """
    removeLabels = [l.strip() for l in options.remove.split(options.delimiter)]
    print("Seclecting rows...")
    takeout_fn = (lambda a: '|'.join(sorted([x.strip() for x in
                  str(a).split(options.delimiter) if x.strip() not in
                  removeLabels])))
    data['label'] = data['label'].apply(takeout_fn)

    data = data[data['label'] != '']

    return data[data['label'] != 'nan']


def RandomSample(data, size):
    """Returns random sample of given size
    """
    return data.ix[random.sample(data.index, size)]


def StratifiedSample(data, nperlabel):
    """Returns stratified data with N per label
    """
    sample = pd.DataFrame()
    datagrp = data.groupby('label')
    sortedgrp = datagrp.size().order(ascending=False)
    for i, l in enumerate(sortedgrp.index):
        if sortedgrp[l] > nperlabel:
            print("==> %-50s %6d" % (l, sortedgrp[l]))
            sample = sample.append(RandomSample(data[data['label'] == l],
                                   nperlabel))
        else:
            break
    print("There are %d labels have more than %d articles" % (i, nperlabel))
    print("Sample size: %s articles" % (len(sample)))
    return sample


if __name__ == "__main__":
    print("%s - %s\n" % (os.path.basename(sys.argv[0]), __version__))
    (options, args) = parse_command_line(sys.argv)
    if len(args) < 2:
        print("Usage: %s [options] <CSV input file>" %
              os.path.basename(sys.argv[0]))
        sys.exit(-1)

    print(options)

    if not options.noreport:
        print("Data analysis in progress...")
        DataReport(args[1], options.column, options)

    print("Reading CSV file...(%s)" % args[1])
    data = pd.read_csv(args[1], usecols=[options.column])
    data.columns = ['label']
    # Subsetting data by --begin and --end option
    if options.end == 0:
        options.end = len(data)
    data = data[options.begin - 1:options.end]
    data = SelectRows(data, options)
    if options.size != 0:
        print("Random sampling...(N = %d)" % options.size)
        data = RandomSample(data, options.size)
    if options.nperlabel != 0:
        print("Stratified sampling...(N per label = %d)" % options.nperlabel)
        data = StratifiedSample(data, options.nperlabel)

    print("Writing output CSV file...(%s)" % options.outfile)
    if options.selected_cols: 
        columns = [c.strip() for c in
                   options.selected_cols.split(options.delimiter)
                   if c.strip() != '']
        try:
            outdata = pd.read_csv(args[1], usecols=columns)
        except Exception as e:
            print("ERROR: Cannot read CSV file (%s)" % e.message)
            sys.exit(-1)
    else:
        outdata = pd.read_csv(args[1])
    outdata = outdata.iloc[data.index]
    outdata.to_csv(options.outfile, index_label='index')
    print("Done!!!")
