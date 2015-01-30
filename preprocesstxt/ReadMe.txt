Usage: process_cc_clean.py [options] <directory of text files>

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

  NOTE: 
  By default the program applies the following functions :-
  - to_lower_case
  - remove_special_characters (!"#$%&\'()*+-/:;<=>@[\\]^_`{|}~)
  - remove_diacritics
  - remove_extra_space