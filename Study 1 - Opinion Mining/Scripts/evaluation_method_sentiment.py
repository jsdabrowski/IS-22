"""
The program evaluates the sentiment from outputed by a given approach
and compare against annotated one. It calucaltes Precision, Recall, F1
And plot confusion matrices.

The programs requires xls file with annotated review sentences

"""

import copy
import openpyxl
import time
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix
from sklearn.utils.multiclass import unique_labels
from sklearn.metrics import precision_recall_fscore_support
from sklearn.metrics import accuracy_score

class PhraseExtractor:

    def __init__(self, fullpath):
        self.FullPath = fullpath

        # Open workbook following a given path
        self.workbook = openpyxl.load_workbook(self.FullPath)

    # Read phrases with feature expressions for a cell and transform to list
    def read_phrase_from_cell(self, sheetname, in_column, in_row):

        # Open a worksheet with list of review sentence to be analyzed by different tools
        sheet = self.workbook.get_sheet_by_name(sheetname)

        # Reading a given review sentence from active worksheet and return as List
        cell_read = in_column + str(in_row)

        return sheet[cell_read].value.split(";") if isinstance(sheet[cell_read].value, str) else ""

    def write_phrase_to_cell(self, sheetname, in_column, in_row, value):

        # Open a worksheet with list of review sentence to be analyzed by different tools
        sheet = self.workbook.get_sheet_by_name(sheetname)
        specific_cell = str(in_column) + str(in_row)
        sheet[specific_cell] = value

    def save_workbook(self):

        # Save extraction results to workbook
        self.workbook.save(FilePath + FileName)


# Convert to Sentiment Output such as positive (0), neutral (1), negative (2) to calculate P/R
def convert_sentiment_label(senetiment):
    switcher = {
        0: 1,
        1: 0,
        -1: 2,
    }
    return switcher.get(senetiment, "nothing")


# Map column indices into sentiment polarity positive (1), neutral (0), negative (-1)
def column_index_to_sentiment(sentiment):
    switch_sentiment = {
        0: 1,
        1: 0,
        2: -1,
    }
    return switch_sentiment.get(sentiment, "nothing")


# That functions was taken from sci-kit learn to plot confusion matrix
def plot_confusion_matrix(y_true, y_pred, classes, normalize=False, title=None, cmap=plt.cm.Blues):
    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    """
    if not title:
        if normalize:
            title = 'Normalized confusion matrix'
        else:
            title = 'Confusion matrix, without normalization'

    # Compute confusion matrix
    cm = confusion_matrix(y_true, y_pred)
    # Only use the labels that appear in the data
    classes = classes[unique_labels(y_true, y_pred)]

    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        print("Normalized confusion matrix")
    else:
        print('Confusion matrix, without normalization')

    fig, ax = plt.subplots()
    im = ax.imshow(cm, interpolation='nearest', cmap=cmap)
    ax.figure.colorbar(im, ax=ax)
    # We want to show all ticks...
    ax.set(xticks=np.arange(cm.shape[1]),
           yticks=np.arange(cm.shape[0]),
           # ... and label them with the respective list entries
           xticklabels=classes, yticklabels=classes,
           title=title,
           ylabel='True label',
           xlabel='Predicted label')

    # Rotate the tick labels and set their alignment.
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
             rotation_mode="anchor")

    # Loop over data dimensions and create text annotations.
    fmt = '.2f' if normalize else 'd'
    thresh = cm.max() / 2.
    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            ax.text(j, i, format(cm[i, j], fmt),
                    ha="center", va="center",
                    color="white" if cm[i, j] > thresh else "black")
    fig.tight_layout()
    return ax


if __name__ == "__main__":

    # Information for Read and Write Xls File
    FilePath = "./"
    FileName = "Experiment_template.xlsx"
    FullPath = FilePath + FileName
    SheetName = 'Sentiment Evaluation'

    # Column index with extracted and labelled expression
    MatchedFeaturesColumn = 'I'

    LeftSentimentPositiveColumn = 'E'
    LeftSentimentNeutralColumn = 'F'
    LeftSentimentNegativeColumn = 'G'

    RightSentimentPositiveColumn = 'K'
    RightSentimentNeutralColumn = 'L'
    RightSentimentNegativeColumn = 'M'

    AnnotatedSentimentColumn = 'P'
    PredictedSentimentColumn = 'Q'

    TotalAnnotatedSentimentColumn = 'W'
    TotalAnnotatedSentimentRow = 2
    TotalLabeledSentimentColumn = 'X'
    TotalLabeledSentimentRow = 2

    AnnotatedSentimentTotalList = list()
    PredictedSentimentTotalList = list()

    RowStart = 2
    RowStop = 248

    # Open xls file
    PhraseReader = PhraseExtractor(FullPath)

    for Row in range(RowStart, RowStop + 1):

        MatchedFeaturesPair = PhraseReader.read_phrase_from_cell(SheetName, MatchedFeaturesColumn, Row)

        LeftPositiveFeature = PhraseReader.read_phrase_from_cell(SheetName, LeftSentimentPositiveColumn, Row)
        LeftNeutralFeature = PhraseReader.read_phrase_from_cell(SheetName, LeftSentimentNeutralColumn, Row)
        LeftNegativeFeature = PhraseReader.read_phrase_from_cell(SheetName, LeftSentimentNegativeColumn, Row)
        LeftSentimentAggregated = [LeftPositiveFeature, LeftNeutralFeature, LeftNegativeFeature]

        RightPositiveFeature = PhraseReader.read_phrase_from_cell(SheetName, RightSentimentPositiveColumn, Row)
        RightNeutralFeature = PhraseReader.read_phrase_from_cell(SheetName, RightSentimentNeutralColumn, Row)
        RightNegativeFeature = PhraseReader.read_phrase_from_cell(SheetName, RightSentimentNegativeColumn, Row)
        RightSentimentAggregated = [RightPositiveFeature, RightNeutralFeature, RightNegativeFeature]

        MatchedFeaturesLeftSide = list()
        MatchedFeaturesRightSide = list()

        # Left side
        AnnotatedSentiment = list()
        # Right side
        PredictedSentiment = list()

        # Pairs of features separated into lef and right side
        for pair in MatchedFeaturesPair:
            MatchedFeaturesLeftSide.append(pair.split(' == ')[0])
            MatchedFeaturesRightSide.append(pair.split(' == ')[1])

        # Check sentiment of the same features on the left and right side
        for i in range(0, len(MatchedFeaturesPair)):

            # We check if left feature has assigned sentiment, and then right feature has assigned sentiment
            for LeftFeatures in LeftSentimentAggregated:
                if MatchedFeaturesLeftSide[i] in LeftFeatures:
                    for RightFeatures in RightSentimentAggregated:
                        if MatchedFeaturesRightSide[i] in RightFeatures:
                            AnnotatedSentiment.append(column_index_to_sentiment(LeftSentimentAggregated.index(LeftFeatures)))
                            PredictedSentiment.append(column_index_to_sentiment(RightSentimentAggregated.index(RightFeatures)))

        # if there is at least one matched relationship
        if MatchedFeaturesPair:

            # if feature on the left and right side are assigned with sentiment polarity
            if AnnotatedSentiment and PredictedSentiment:

                # Write annotated sentiment
                PhraseReader.write_phrase_to_cell(SheetName, AnnotatedSentimentColumn, Row, str(AnnotatedSentiment))
                AnnotatedSentimentTotalList = AnnotatedSentimentTotalList + AnnotatedSentiment

                # Write predicted sentiment
                PhraseReader.write_phrase_to_cell(SheetName, PredictedSentimentColumn, Row, str(PredictedSentiment))
                PredictedSentimentTotalList = PredictedSentimentTotalList + PredictedSentiment

    # Write the aggregated sentiment of all the each row in a cell
    PhraseReader.write_phrase_to_cell(SheetName, TotalAnnotatedSentimentColumn, TotalAnnotatedSentimentRow, str(AnnotatedSentimentTotalList))
    PhraseReader.write_phrase_to_cell(SheetName, TotalLabeledSentimentColumn, TotalLabeledSentimentRow, str(PredictedSentimentTotalList))

    # Save workbook with changes
    PhraseReader.save_workbook()

    # Here code for computing P/R/F1, and plotting confusion matrices begin

    # Give predicted and annotated sentiment values
    SentimentLabeled = AnnotatedSentimentTotalList
    SentimentPredicted = PredictedSentimentTotalList

    # Convert sentiment values to ones that can be interpreted by sci-kit learn library
    ConvertedSentimentPredicted = []
    for element in SentimentPredicted:
        ConvertedSentimentPredicted.append(convert_sentiment_label(element))
    SentimentPredicted = ConvertedSentimentPredicted

    ConvertedSentimentLabeled = []
    for element in SentimentLabeled:
        ConvertedSentimentLabeled.append(convert_sentiment_label(element))
    SentimentLabeled = ConvertedSentimentLabeled

    # Compute and plot confusion matrix
    class_names = np.array(['positive', 'neutral', 'negative'])

    # Convert sentiment to numpy format acceptable by sci-kit learn
    y_true = np.array(SentimentLabeled)
    y_pred = np.array(SentimentPredicted)

    np.set_printoptions(precision=2)

    # Plot non-normalized confusion matrix
    plot_confusion_matrix(y_true, y_pred, classes=class_names, title=' ')


    # Plot normalized confusion matrix
    plot_confusion_matrix(y_true, y_pred, classes=class_names, normalize=True, title='Normalized confusion matrix')

    # Compute precision and recall
    print("Number of features: ", len(SentimentLabeled))

    # First array presents precision(positive, neutral, negative), second presents recall(positive, neutral, negative)

    # print("### Listen! First array presents precision(positive, neutral, negative), second presents recall(positive, neutral, negative), then f-1..: ")
    # print("Per class metrics:", precision_recall_fscore_support(y_true, y_pred, average=None))

    print("Precision and Recall per Classes: ")
    print("Per class metrics: Positive (P = {:.2f}, R = {:.2f})".format(precision_recall_fscore_support(y_true, y_pred, average=None)[0][0], precision_recall_fscore_support(y_true, y_pred, average=None)[1][0]))
    print("Per class metrics: Neutral (P = {:.2f}, R = {:.2f})".format(precision_recall_fscore_support(y_true, y_pred, average=None)[0][1], precision_recall_fscore_support(y_true, y_pred, average=None)[1][1]))
    print("Per class metrics: Negative (P = {:.2f}, R = {:.2f})".format(precision_recall_fscore_support(y_true, y_pred, average=None)[0][2], precision_recall_fscore_support(y_true, y_pred, average=None)[1][2]))

    # First element precision, second recall, third f-measure
    # print("### Listen! First element precision, second recall, third f-measure: ")
    # print("Micro metric: Precision = {:.2f}, Recall ={:.2f} ".format(precision_recall_fscore_support(y_true, y_pred, average='micro')[0], precision_recall_fscore_support(y_true, y_pred, average='micro')[1]))

    # Macro does not take imbalance classes into account
    # print("Macro metrics: ", precision_recall_fscore_support(y_true, y_pred, average='macro'))
    print("Weighted metrics: Precision = {:.2f}, Recall = {:.2f} ".format(precision_recall_fscore_support(y_true, y_pred, average='weighted')[0], precision_recall_fscore_support(y_true, y_pred, average='weighted')[1]))

    print("Accuracy: {:.3f}".format(accuracy_score(y_true, y_pred)))
    print("Check number of sentiments polarities labeled and predicted:", len(y_true), " == ", len(y_pred))

    # positive (0), neutral (1), negative (2)
    print("Positive number: ", list(y_true).count(0))
    print("Neutral number: ", list(y_true).count(1))
    print("Negative number: ", list(y_true).count(2))

    # Display plot
    plt.show()


