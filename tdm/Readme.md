#### Create Term Document Matrix or TF-IDF

The script takes a csv with a (preprocessed) text column and outputs a tdm, tf-idf. It also prints out summary including  most frequent terms, most infrequent terms etc. See below for more detail.

The script depends on `sklearn` which in turn depends on `numpy` and `scipy'. To install the dependencies:
```
sudo apt-get install -qq python-numpy python-scipy
pip install -U sklearn
```

To run the script:
```
python tdm.py [options] <CSV input file>
```

Here are all the script options and default values of the options:

```
Options:
  -h, --help            show this help message and exit
  -t TEXTCOLUMN, --text=TEXTCOLUMN
                        Text column name (default: 'Body')
  -l LABELCOLUMNS, --labels=LABELCOLUMNS
                        Label column(s) name (default: 'Online Section')
  -d DELIMITER, --delimiter=DELIMITER
                        Delimeter use to split option's value if multiple
                        values (default: ';')
  --min-ngram=MIN_NGRAM
                        Minimum ngram(s) (default: 1)
  --max-ngram=MAX_NGRAM
                        Maximum ngram(s) (default: 2)
  --max-features=MAX_FEATURES
                        Maximum features (default: 2**16)
  --n-freq=N_FREQ       Report most frequent terms (default: 20)
  --n-sparse=N_SPARSE   Report most sparse terms (default: 20)
  -r REMOVE_TERMS_FILE, --remove-terms-file=REMOVE_TERMS_FILE
                        File name contains terms to be removed (default: None)
  --remove-n-freq=REMOVE_N_FREQ
                        Top most of frequent term(s) to be removed (default:
                        0)
  --remove-n-sparse=REMOVE_N_SPARSE
                        Top most of sparse term(s) to be removed (default: 0)
  --out-tdm-file=OUT_TDM_FILE
                        Save output TDM to CSV filename (default: None)
  --use-tfidf           Use TF-IDF (default: False)
  --out-tfidf-file=OUT_TFIDF_FILE
                        Save output TF-IDF to CSV filename (default: None)
```

### Example

```
python TDM.py --max-features=100 --n-freq=10 --n-sparse=20 --remove-terms-file=remove-terms.csv --remove-n-freq=10 --remove-n-sparse=40 --out-tdm-file=tdm.csv --use-tfidf --out-tfidf-file=tfidf.csv input.csv
```

Note that the TDM/TF-IDF output CSV file will be large and take a long time to save if there are a lot of terms (columns).

The `index` column also added to output CSV file as reference unique ID (row index of the input CSV file)