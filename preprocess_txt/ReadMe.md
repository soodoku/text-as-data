## Preprocess Text in Directory of Text Files

Takes a directory of text files and outputs processed text files in the same directory structure.

By default, the script converts text to lower case, removes special characters (!"#$%&\'()*+-/:;<=>@[\\]^_`{|}~), removes diacritics, and removes extra space. 

To run the script, type the following in shell:
```
python preprocess.py [options] <directory of text files>
```

The script takes the following command line options: 

```
Options:
  -h, --help            show this help message and exit
  -o OUTFILE, --out=OUTFILE
                        Output file in CSV (default: program.data.csv)
  -d OUTDIR, --dir=OUTDIR
                        Output directory for normalize file (default: txt)
  --overwritten         Overwritten even if output file exists (default: No)
  --remove-stopwords=REMOVE_STOPWORDS
                        Remove stopwords 'common25' or 'common100' or'nltk'
                        (default: None)
  --remove-punctuation  Remove punctuation (default: No)
  --stemmed=STEMMED     Select stemmer 'porter' or 'snowball' (default:
                        None)
  --include-text        Also Output cleaned text as column in program data
                        file (default: No)
```

### Example

To clean files in directory `sample_in` and save output in `sample_out`

```
python preprocess_txt/preprocess.py preprocess_text/sample_in/ -o preprocess_txt/sample-out/
```