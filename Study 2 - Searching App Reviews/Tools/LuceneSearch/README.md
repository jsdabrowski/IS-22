## LuceneSearch Tool
We here provide our implementation of Lucene-based tool.

### How to Install LuceneSearch tool
Download LuceneSearch directory and place in a folder preferable in your home folder.

Make sure your LuceneSearch folder contains this structure:

```
LuceneSearch/
└── com.vogella.maven.eclipse
    ├── pom.xml
    ├── src
    │   ├── main
    │   │   └── java
    │   │       └── com
    │   │           └── vogella
    │   │               └── com
    │   │                   └── vogella
    │   │                       └── maven
    │   │                           └── eclipse
    │   │                               ├── InMemoryLuceneIndex.java
    │   │                               ├── Review.java
    │   │                               └── XlsManipulation.java
    │   └── test
    │       └── java
    │           └── com
    │               └── vogella
    │                   └── com
    │                       └── vogella
    │                           └── maven
    │                               └── eclipse
    │                                   ├── DataManipulationTestCases.java
    │                                   ├── LuceneTestCases.java
    │                                   └── TotalExperimentTestCases.java
    └── target
        ├── classes
        │   └── com
        │       └── vogella
        │           └── com
        │               └── vogella
        │                   └── maven
        │                       └── eclipse
        │                           ├── InMemoryLuceneIndex.class
        │                           ├── Review.class
        │                           ├── XlsManipulation.class
        │                           ├── hitDocumentsContainer.class
        │                           └── sortByReviewNo.class
        └── test-classes
            └── com
                └── vogella
                    └── com
                        └── vogella
                            └── maven
                                └── eclipse
                                    ├── DataManipulationTestCases.class
                                    ├── LuceneTestCases.class
                                    └── TotalExperimentTestCases.class
```

### How to Configure LuceneSearch tool
Open ```TotalExperimentTestCases.java``` to configure the tool. Find the snippet:

```
// Location of a xls file with app reviews
private String inputPathname = "/Users/jacekdabrowski/Desktop/Collected reviews/";
private String inputFilename = "Evernote_1250_review_level.xlsx";
int numberReviews = 1250;
	
private String outputPathname = "/Users/jacekdabrowski/Desktop/";
private String outputFilename = "results_lucene_search_";
	
// Input queries 
private List<String> orginalQueries = Arrays.asList("Create shortcuts", "Write notes");
```

Set up ```inputPathname``` and  ```inputFilename``` to indicate path and the name of *.xls file with app reviews in which the tool searches for feature-specific app reviews; ```numberReviews``` to indicate the number of app reviews that need to be analysed; ```outputPathname``` and  ```outputFilename``` to indicate the path of the tool's output file; and ```orginalQueries``` to indicate a list of queried features. 

### How to Run LuceneSearch tool
Run ```TotalExperimentTestCases.java``` to use the tool for finding feature-specific app reviews.