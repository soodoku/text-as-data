Subset, Simple Random or Stratified Random Sample
=================================================

Description
-----------

Input: Path name to preprocessed dataset, labelColumn
   * If SelectedCols given, keep only SelectedCols in the dataset
   * If SelectedRows given, keep only SelectedRows in the dataset
   * If RandomSampleSize given, 
     - From dataset = [SelectedCols, SelectedRows], take a random sample with size = size
  * If StratifiedRandomSample given,
     - From dataset = [SelectedCols, SelectedRows], take a stratified random sample with n per label

Functions:
1. DataReport(labelColumn)
   * Report certain features of the data
   * Takes the argument (labelColumn)
     - Total number of rows
     - Reports total # of unique labels
     - Reports total number of rows per unique label
     - Runs automatically when script is called

2. SelectCols(SelectedCols)
   * If user provides no list of columns, keep all columns
   * Otherwise keep only 'SelectedCols'

3. SelectRows(labelColumn, removeLabels)
   * Selecting a subset of the data
     - Takes the arguments: labelColumn, removeLabels 

4. RandomSample(Size, data (from SelectRows, SelectCols))
   * Random Sample

5. StratifiedSample(NperLabel, LabelColumn, OutputFromSelectRows) 
   * Stratified Random Sample
   * Randomly sample NperLabel within rows with each Label

Usage
--------------


```
    SubsetData.py - r3 (2014/12/25)
    
    Usage: SubsetData.py [options] <CSV input file>
    
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

EXAMPLE
-------

```
    python SubsetData.py -s 1000 --selected-cols "labels;text" --no-report -o input-subset.csv input.csv
```

To randomly sample 1000 row from `input.csv` and save as `input-subset.csv` with only columns named `labels` and `text`

An `index` column will be added to output CSV file as a unique ID (row index of the input CSV file)
