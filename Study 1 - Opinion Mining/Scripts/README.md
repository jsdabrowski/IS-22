## Scripts

You can find here the following files:

- ``` evaluation_method_features.py``` : script implementing the evaluation method for feature extraction
- ``` evaluation_method_features.py``` : script implementing the evaluation method for feature-specific sentiment analysis
- ``` Experiment_template.xls ``` : File to which a tool outputs results and where a part of the ground truth should be copied; and to compare the tool output to the ground truth.

# How to Evaluate Future Extraction

Copy ```evaluation_method_features.py``` to your desired directory.

Open ```evaluation_method_features.py``` to configure the tool. Find the snippet:

```
FilePath = "./"
FileName = "Experiment_template.xlsx"
FullPathEvaluation = FilePath + FileName
RowStartEvaluation = 2
RowStopEvaluation = 155

```

Set up ```FilePath``` and  ```FileName``` to indicate path and the name of *.xls file with manually annotated features and features outputted from a tool; ```RowStartEvaluation ``` and ``` RowStopEvaluation ``` to indicate features  that will be compared.

Run ```evaluation_method_features.py```.

Make sure that values from ```N:Y``` cells in ```Apps``` tab, in ```Experiment_tample.xls``` file, are copied to the respective columns in ```Exact Match```, ```Partial Match (1)``` and ```Partial Match (2)``` tabs.

# How to Evaluate Feature-Specific Sentiment Analysis

Copy ```evaluation_method_sentiment.py ``` to your desired directory.

Open ```evaluation_method_sentiment.py``` to configure the tool. Find the snippet:

```
# Information for Read and Write Xls File
FilePath = "./"
FileName = "Experiment_template.xlsx"
FullPath = FilePath + FileName
SheetName = 'Sentiment Evaluation'

RowStart = 2
RowStop = 248
```

Set up ```FilePath``` and  ```FileName``` to indicate path and the name of *.xls file with manually annotated sentiment and sentiment outputted from a tool; ```RowStart``` and ```RowStop``` to indicate sentiment  that will be compared.

Run ```evaluation_method_sentiment.py```.

Make sure that values from ```E:G``` and ```K:M``` cells in ```Apps``` tab, in ```Experiment_tample.xls``` file, are copied to the respective columns in ```Sentiment Evaluation``` tab.
