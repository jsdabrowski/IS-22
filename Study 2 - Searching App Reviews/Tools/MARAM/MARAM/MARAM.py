""" My implmentation of the MARAM tool """

import text_processing as txtProcessing
import numpy as np
import pandas as pd
import time
import copy


def jaccard_similarity(list1, list2):
    s1 = set(list1)
    s2 = set(list2)
    return float(len(s1.intersection(s2)) / len(s1.union(s2)))


if __name__ == "__main__":

    print('The experiment started.')
    start = time.time()

    # File with INPUT Reviews and Identified Features
    FilePath = "/Users/jacekdabrowski/Desktop/Collected reviews/"
    # FileName = "result_safe_transformed.xlsx"
    FileName = "Evernote_1250_review_level.xlsx"
    Sheet = 'Reviews'

    # File with OUTPUT Results
    FilePathResults = "/Users/jacekdabrowski/Desktop/"
    FileNameResults = "results_maram_search_"
    SheetResults = 'Results'

    # No. Reviews to Read
    numberReviews = 1025

    # INPUT Queries

    queriesOrginal = ["Create shortcuts", "Write notes"]

    # INPUT Reviews
    df = pd.read_excel(FilePath+FileName, sheet_name=Sheet, usecols="A:C")

    # Select number reviews to read
    df = df.head(numberReviews)

    # Convert df to list
    reviewCollection = df.values.tolist()

    # Here MARAM algorithm are performed.
    textProcessor = txtProcessing.TextProcessing()

    # Process Queries
    queriesProcessed = list()
    for query in queriesOrginal:
        textProcessor.text_processing(query)
        queriesProcessed.append(textProcessor.get_processed_text())

    # Perform experiment for each query
    for queryProcessed in queriesProcessed:

        # Process Reviews
        reviewsProcessed = list()
        reviewProcessed = list()

        for review in reviewCollection:
            reviewProcessed = copy.deepcopy(review)
            textProcessor.text_processing(review[2])
            reviewProcessed.append(textProcessor.get_processed_text())

            reviewProcessed.append(queriesOrginal[queriesProcessed.index(queryProcessed)])
            reviewProcessed.append(queryProcessed)

            # Compute Similarity
            jaccardSimilarityValue = jaccard_similarity(queryProcessed, reviewProcessed[3])
            reviewProcessed.append(jaccardSimilarityValue)

            reviewsProcessed.append(reviewProcessed)

            # Data frame with semantic search results
            df_results = pd.DataFrame

            # Save Results
            df_results = pd.DataFrame(reviewsProcessed,
                                      columns=['App id', 'Review id', 'Review content', 'Review (Preprocessed)', 'Query (Orginal)',
                                               'Query (Preprocessed)', 'Jaccard Similarity'])

            df_results.to_excel(
                FilePathResults + FileNameResults + "query_{0}_".format(queriesProcessed.index(queryProcessed) + 1) + queriesOrginal[
                    queriesProcessed.index(queryProcessed)] + ".xlsx", sheet_name=SheetResults, index=False, engine='xlsxwriter')

    # Experiment execution time
    end = time.time()
    print('Experiment took: {0}'.format(end - start))