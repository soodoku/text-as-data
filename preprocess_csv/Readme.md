## Pre-processing data for some Text as Data Analyses

### Description

Pre-process data for some text as data kinds of analyses. 

Input: csv with 'dirty text' column  
Output: csv with 'clean text' column  

The script:  
1. Depending on what the user wants, removes stop words, stems, normalizes (takes out special characters, extra whitespace etc.).  
2. And then dumps the cleaned data back into a new csv with all the other columns  
3. Downloads nltk_data to ./nltk_data directory if no such directory exists  

You can also just output a random sample of the file. See this [Stackflow](http://stackoverflow.com/questions/692312/randomly-pick-lines-from-a-file-without-slurping-it-with-unix) documentation for how random sampling is implemented.

The following show all script options and default value of the options:  

<pre><code>
    preprocessData.py - r7 (2014/09/25)

    Usage: preprocessDataForML.py [options] <CSV input file>

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
</code></pre>

### Example

To clean column name `Content` in `test.csv` and save output as `test-cleaned.csv`

<pre><code>
	python preprocessData.py -c Content test.csv -o test-cleaned.csv
</code></pre>	
