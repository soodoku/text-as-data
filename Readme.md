## Text as Data

[![MIT](https://img.shields.io/github/license/mashape/apistatus.svg)](https://opensource.org/licenses/MIT)
[![Build Status](https://travis-ci.org/soodoku/text-as-data.svg?branch=master)](https://travis-ci.org/soodoku/text-as-data)

1. [Get Text](https://github.com/soodoku/text-as-data#get-text-data)
2. [Preprocess Text](https://github.com/soodoku/text-as-data#preprocess-text)
3. [Subset, Take a Random Sample, Summarize](https://github.com/soodoku/text-as-data#get-summary-of-data-subset-data)
4. [Create tdm/tf-idf](https://github.com/soodoku/text-as-data#get-tdm)
5. Analyze the data
	* [Analyze Text in R](https://github.com/soodoku/text-as-data#analyze-text-in-r)
	* [Sentiment Analysis in Python](https://github.com/soodoku/text-as-data#sentiment-analysis-in-python)

### Get Text

You can get text data from scraping, APIs, searchable pdfs, images of paper, etc. Some examples:
* Get text from searchable pdfs. e.g. [Get data from Wisconsin Ads storyboards using Python](https://gist.github.com/soodoku/62a3172eb1b4a55dee1a)
* [Get text from images of text using Tesseract from Python](https://github.com/soodoku/image-to-text)
* [Get text from images of text using Abbyy FineReader Cloud OCR from R](https://github.com/soodoku/abbyyR)
* [Get text from images of text using Captricity OCR from R](https://github.com/soodoku/captr)
* [Get Congressional Speech Data](https://gist.github.com/soodoku/85d79275c5880f67b4cf) using Capitol Words API from the Sunlight Foundation

### Preprocess Text

Preprocess text for text-as-data analysis. 

Depending on the need, remove stop words, punctuation, capitalization, special characters, and stem.

* [preprocess_txt](preprocess_txt/) takes a directory of 'raw' text files and outputs processed text files in the same directory structure. 
* [preprocess_csv](preprocess_csv/) takes a csv with 'raw' text and outputs a csv with processed text.

### Get Summary of the Data, Subset Data

Output a simple or stratified random sample of a csv, and only the columns you need. Get summary of crucial aspects of the data. Takes a csv. 

* [Summarize and Subset](subset/).

### Get TDM

Create a term-document-matrix and get some information about the matrix including frequent and infrequent terms. Options available for removing sparse terms etc. 

* [Get TDM, TF-IDF, Summary](tdm/).

### Sentiment Analysis in Python

* [Basic sentiment analysis](https://gist.github.com/soodoku/22e4cff2eb6a05be3c0d) using AFINN

### Analyze Text in R

* Classify text in R using SVM or Lasso. See [Basic Text Classifier](https://gist.github.com/soodoku/e34dbe0219b0f00a74d5)
* Worked out example of how to model words as a function of ideology using Congressional Speech. See [Speech Learn](https://github.com/soodoku/speech-learn)

### License

Scripts are released under the [MIT License](https://opensource.org/licenses/MIT).		
