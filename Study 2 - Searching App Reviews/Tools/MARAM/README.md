## MARAM Tool
We here provide our re-implementation of MARAM tool.

### How to Install MARAM tool
Download MARAM directory and place in a folder preferable in your home folder.

Make sure your MARAM folder contains this structure:
```
MARAM/
├── MARAM.py
└── text_processing.py
```

### How to Configure MARAM tool
Open ```MARAM.py``` to configure the tool. Find the snippet:

```
# File with INPUT Reviews and Identified Features
FilePath = "./Collected reviews/"
FileName = "Evernote_1250_review_level.xlsx"
Sheet = 'Reviews'

# File with OUTPUT Results
FilePathResults = "./Result from running tools - searching/"
FileNameResults = "results_maram_search_"
SheetResults = 'Results'

# No. Reviews to Read
numberReviews = 1025

# INPUT Queries
queriesOrginal = ["Create shortcuts", "Write notes", "Annotate documents", "Widget", "Add a passcode lock"]

```

Set up ```FilePath``` and  ```FileName``` to indicate path and the name of *.xls file with app reviews in which the tool searches for feature-specific app reviews; ```numberReviews``` to indicate the number of app reviews that need to be analysed; ```FilePathResults``` and  ```FileNameResults ``` to indicate the path of the tool's output file; and ```queriesOrginal``` to indicate a list of queried features. 

### How to Run MARAM tool
Run ```MARAM.py``` to use the tool for finding feature-specific app reviews.