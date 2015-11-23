## Subset, Simple Random or Stratified Random Sample

Takes a csv, column containing labels (y), and options such as size of random sample, n per label if you want a stratified random sample, column names of columns you want to keep (default is to keep all), etc. see more below. The script produces a csv that includes an index column that tracks the row index of the input data. The script also prints out the following features of the data:
- Total number of rows
- Total # of unique labels
- Total number of rows per unique label

### Usage

To run the script,
```
python SubsetData.py [options] <CSV input file>
```

The script supports the following command line options: 

```    
    
    Options:
      -h, --help            show this help message and exit
      -c COLUMN, --column=COLUMN
                            Label column name (default: 'Online Section')
      -d DELIMITER, --delimiter=DELIMITER
                            Delimeter use to split label if multiple labels
                            (default: ';')
      -r REMOVE, --remove=REMOVE
                            Labels name to be removed (default: 'NA')
      -o OUTFILE, --outfile=OUTFILE
                            Subseting output CSV filename (default: 'subset.csv')
      -b BEGIN, --begin=BEGIN
                            Begin row number (default: 1)
      -e END, --end=END     End row number (default: 0)
      --selected-cols=SELECTED_COLS
                            Selected columns name (default: 'All')
      -s SIZE, --size=SIZE  Random sample size (default: 0)
      -n NPERLABEL, --n-per-label=NPERLABEL
                            N per label (stratified) (default: 0)
      --no-report           Don't report data statistics (default: False)
```

### Example

```
python SubsetData.py -s 1000 --selected-cols "labels;text" --no-report -o input-subset.csv input.csv
```

Randomly samples 1000 row from `input.csv` and saves as `input-subset.csv` with only columns named `labels` and `text`

An `index` column is added to output CSV file as a unique ID (row index of the input CSV file)
