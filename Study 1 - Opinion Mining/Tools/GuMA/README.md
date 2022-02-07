## GuMA Tool
We here provide our re-implementation of GuMA tool. We implemented feature extraction and feature-specific sentiment analysis as separate programs. You can find the program is the following directories:

- ``` GuMA-FE/ ``` : files for running feature extraction
- ``` GuMA-SA/ ``` : files for running feature-specific sentiment analysis


## GuMA Tool - Feature Extraction

### How to Install GuMA tool for Feature Extraction
Download GuMA-FE directory and place in a folder preferable in your home folder.

Make sure your GuMA-FE folder contains this structure:
```
GuMA-FE
├── algorithm_collocation.py
├── collocations_builder.py
├── main.py
├── supporting_files
│   ├── Experiment_template.xlsx
│   └── com.zentertain.photoeditor_lexicon.xlsx
├── text_processing.py
└── xls_manipulation.py
```

### How to Configure GuMA tool for Feature Extraction
Open ```main.py``` to configure the tool. Find the snippet:

```
    # Path to file with reviews in which features are identified for evaluation
    FilePath = "./supporting_files/"
    FileName = "Experiment_template.xlsx"
    FullPathCollocationExtraction = FilePath + FileName
    StartRowReview = 2
    StopRowReview = 155
    rowsWithReviews = list(range(StartRowReview, StopRowReview + 1))
```
Set up ```FilePath``` and  ```FileName``` to indicate path and the name of *.xls file with app reviews from which app features are identified for the evaluation; ```StartRowReview``` and ``` StopRowReview``` to indicate app reviews that need to be analysed.

### How to Run GuMA tool for Feature Extraction
Run ```main.py``` to use the tool for feature extraction.


## GuMA Tool - Feature-Specific Sentiment Analysis

### How to Install GuMA tool for Feature-Specific Sentiment Analysis
Download GuMA-SA directory and place in a folder preferable in your home folder.

Make sure your GuMA-SA folder contains this structure:
```
GuMA-SA
├── main_program.py
└── supporting_files
    ├── Experiment_template.xlsx
    └── SentiStrength
        ├── SentiStrength.jar
        └── SentiStrength_Data
            ├── BoosterWordList.txt
            ├── Dictionary.txt
            ├── EmoticonLookupTable.txt
            ├── FilmAddition.txt
            ├── IdiomLookupTable.txt
            ├── IronyTerms.txt
            ├── MobilePhoneAddition.txt
            ├── MusicAddition.txt
            ├── NegatingWordList.txt
            ├── PoliticsAddition.txt
            ├── QuestionWords.txt
            ├── RiotsAddition.txt
            ├── SentimentLookupTable.txt
            └── SlangLookupTable.txt

```

### How to Configure GuMA tool for Feature-Specific Sentiment Analysis
Open ```main_program.py``` to configure the tool. Find the snippet:

```
    # Information for r/w from/to xls file
    FilePath = "./supporting_files/"
    FileName = "Experiment_template.xlsx"
    FullPath = FilePath + FileName
    SheetName = 'Apps'

    # Range of rows from xls for which the analysis will be conducted
    RowStart = 2
    RowStop = 155

```
Set up ```FilePath``` and  ```FileName``` to indicate path and the name of *.xls file with app reviews from which app feature-specific sentiment is identified for the evaluation; ```RowStart ``` and ``` RowStop ``` to indicate app reviews that need to be analysed.

### How to Run GuMA tool for Feature-Specific Sentiment Analysis
Run ```main_program.py``` to use the tool for feature-specific sentiment analysis.
