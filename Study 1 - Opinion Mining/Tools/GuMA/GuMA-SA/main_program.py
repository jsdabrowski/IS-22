"""
This code read xls with review sentences, conduct sentiment analysis and save it in the same file

"""

import subprocess
import shlex
import openpyxl
import time

# Wrapper for SentiStrength and function for conducting sentiment analysis
def get_sentiment(InputContent):

    #open a subprocess using shlex to get the command line string into the correct args list format
    p = subprocess.Popen(shlex.split("java -jar ./supporting_files/SentiStrength/SentiStrength.jar trinary stdin sentidata ./supporting_files/SentiStrength/SentiStrength_Data/"),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)

    #communicate via stdin the string to be rated. Note that all spaces are replaced with +
    #Can't send string in Python 3, must send bytes
    b = bytes(InputContent.replace(" ","+"), 'utf-8')
    stdout_byte, stderr_text = p.communicate(b)

    #convert from byte
    stdout_text = stdout_byte.decode("utf-8")

    #replace the tab with a space between the positive and negative ratings. e.g. 1    -5 -> 1 -5
    stdout_text = stdout_text.rstrip().replace("\t"," ")

    # Below line could be probably remove as we are interested just in final sentiment
    #return stdout_text + ";" + InputContent
    return int(str(stdout_text + ";" + InputContent).split(";")[0].split(" ")[2])


# Class to manipulate xls file: read, write from/to cell
class XlsManipulator:

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

        return sheet[cell_read].value if isinstance(sheet[cell_read].value, str) else isinstance(sheet[cell_read].value, str)

    def write_to_cell(self, sheetname, in_column, in_row, value):

        # Open a worksheet with list of review sentence to be analyzed by different tools
        sheet = self.workbook.get_sheet_by_name(sheetname)
        specific_cell = str(in_column) + str(in_row)
        sheet[specific_cell] = value

    def save_workbook(self):
        # Save extraction results to workbook
        self.workbook.save(FilePath + FileName)

    def close_workbook(self):
        self.workbook.close()


# convert sentiment polarity to respective column that contain such sentiment polarity
def convert_sentiment_to_column(sentiment_polarity, column_positive, column_nutral, column_negative):

    switch_sentiment_to_column = {
        1: column_positive,
        0: column_nutral,
        -1: column_negative,
    }

    return switch_sentiment_to_column[sentiment_polarity]


if __name__ == "__main__":

    time_start = time.time()

    # Determine Sentiment for a sentence via SentiStrength and covert to sci-kit label

    # Information for r/w from/to xls file
    FilePath = "./supporting_files/"
    FileName = "Experiment_template.xlsx"
    FullPath = FilePath + FileName
    SheetName = 'Apps'

    ColumnSentenceInput = 'D'
    ColumnFeaturesEvaluateSentiment = 'H'
    ColumnPositiveFeatures = 'K'
    ColumnNeutralFeatures = 'L'
    ColumnNegativeFeatures = 'M'

    # Range of rows from xls for which the analysis will be conducted
    RowStart = 2
    RowStop = 155

    # Object needed to manipulate xls - r/w operations
    ExcelManipulator = XlsManipulator(FullPath)

    # Read sentence, calculate their sentiment and covert to the form acceptable by sci-kit learn
    for Row in range(RowStart, RowStop+1):

        # Read sentence content
        SentenceContent = ExcelManipulator.read_phrase_from_cell(SheetName, ColumnSentenceInput, Row)
        FeatureContent = ExcelManipulator.read_phrase_from_cell(SheetName, ColumnFeaturesEvaluateSentiment, Row)

        # Check if there are some features that sentiments have to be evaluated in a given row
        if FeatureContent:

            # Predict feature sentiment based on the sentence sentiment
            SentenceSentiment = get_sentiment(SentenceContent)

            # Determine the label of the column
            ColumnLabel = convert_sentiment_to_column(SentenceSentiment, ColumnPositiveFeatures, ColumnNeutralFeatures, ColumnNegativeFeatures)

            # Write Sentence sentiment into xls file. Will be used later to conduct root-cause analysis
            ExcelManipulator.write_to_cell(SheetName, ColumnLabel, Row, FeatureContent)

    # Save and Close Workbook
    ExcelManipulator.save_workbook()
    ExcelManipulator.close_workbook()

    print("Time to execute code: ", time.time() - time_start)
