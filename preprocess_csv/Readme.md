## Preprocess Text in CSV 

Pre-process text data for some text as data kinds of analyses. 

The script takes a csv with raw text and outputs a csv with pre-processed text. Depending on what the user wants, the script removes stop words, stems, normalizes (takes out special characters, extra whitespace etc.), etc. and dumps clean text into a new csv along with all the other columns.  

You can also just output a random sample of the file. See this [Stackflow](http://stackoverflow.com/questions/692312/randomly-pick-lines-from-a-file-without-slurping-it-with-unix) documentation for how random sampling is implemented.

Downloads nltk_data to ./nltk_data directory if no such directory exists  

To run the script, on the shell, type:
```
python preprocessData.py [options] <CSV input file>
```

Script options and default value of the options:  
```  
Options:
  -h, --help            show this help message and exit
  -b BEGIN, --begin=BEGIN
                            Begin row number (default: 1)
  -e END, --end=END     End row number (default: 0)
  -r RANDOM, --random=RANDOM
                            Percent random sampling (default: 100)
  -c COLUMN, --column=COLUMN
                            Data column to be cleaned (default: 'Body')
  -k, --keep            Keep original data column (default: No)
  -o OUTFILE, --outfile=OUTFILE
                            Clean output CSV filename (default: 'cleaned.csv')
  --append              Append if output CSV exists (default: No)
  --keep-accented       Keep accented (default: No)
  --keep-punct          Keep punctuation (default: No)
  --keep-stopwords      Keep stopwords (default: No)
  --keep-numbers        Keep numbers and words that begin with numbers
                            (default: No)
  --keep-stems          Do not stem (default: No)
```

### Example

To clean column name `speaking` in [sample_in.csv](sample_in.csv) and save output as [sample_out.csv](sample-out.csv)

```
python preprocessData.py -c speaking sample_in.csv -o sample-out.csv
```