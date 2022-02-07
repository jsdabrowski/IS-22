from xls_manipulation import PhraseExtractor
from text_processing import TextProcessing
from algorithm_collocation import CollocationAlgorithm
from collocations_builder import CollocationBuilder
import time


def significance_level_to_ciritical_value(level):
    thisdict = {

        0.1: 2.706,
        0.05: 3.841,
        0.01: 6.635,
        0.005: 7.879,
        0.001: 10.828
    }

    return thisdict[level]


class CollocationFindingProgram:

    time_start = time.time()

    collocation_list = list()

    collocations_list_0_1 = list()
    collocations_list_0_01 = list()
    collocations_list_0_05 = list()
    collocations_list_0_005 = list()
    collocations_list_0_001 = list()

    collocation_builder = None

    xls_manipulator = None

    # Build lexicon with collocations
    def __init__(self, FullPathCollocationLexicon, RowStart, RowStop):

        # List of potential features extracted using collocation algorithm
        self.collocation_builder = CollocationBuilder(FullPathCollocationLexicon, RowStart, RowStop)

    # Retrieve collocation from lexicon for a given critical value
    def get_collocations_for_given_critical_value(self, critical_value):

        self.collocation_builder.get_collocation_given_critical_value(critical_value)

        self.collocation_list = self.collocation_builder.get_features()

        print("Collocation Building Time: ", time.time() - self.time_start)

    def set_collocations_list_for_critical_value_predefined_range(self):

        self.collocation_builder.get_collocation_given_critical_value(2.706)
        self.collocations_list_0_1 = self.collocation_builder.get_features()

        self.collocation_builder.get_collocation_given_critical_value(3.841)
        self.collocations_list_0_05 = self.collocation_builder.get_features()

        self.collocation_builder.get_collocation_given_critical_value(6.635)
        self.collocations_list_0_01 = self.collocation_builder.get_features()

        self.collocation_builder.get_collocation_given_critical_value(7.879)
        self.collocations_list_0_005 = self.collocation_builder.get_features()

        self.collocation_builder.get_collocation_given_critical_value(10.828)
        self.collocations_list_0_001 = self.collocation_builder.get_features()

    def get_collocations_for_given_critical_value_predefined_list(self, critical_value):

        if critical_value == 2.706:

            self.collocation_list = self.collocations_list_0_1

        elif critical_value == 3.841:

            self.collocation_list = self.collocations_list_0_05

        elif critical_value == 6.635:

            self.collocation_list = self.collocations_list_0_01

        elif critical_value == 7.879:

            self.collocation_list = self.collocations_list_0_005

        elif critical_value == 10.828:

            self.collocation_list = self.collocations_list_0_001


    def read_file(self, FullPath):

        # Open input text
        self.xls_manipulator = PhraseExtractor(FullPath)

    def save_file(self):

        self.xls_manipulator.save_workbook()
        print("Collocation Program Execution Time: ", time.time() - self.time_start)

    # Run collocation-based extraction algorithm for given rows range
    def run_collocation(self, RowStart, RowStop):

        SheetName = 'Apps'

        # Column index with review content
        SentenceContentLabel = 'D'
        ExtractedFeatureLabel = 'J'

        # Text processing
        text_processor = TextProcessing()

        # List with elements that each one corresponds to processed review
        processed_sentence = list()

        # Read input text
        for row in range(RowStart, RowStop + 1):

            time_start = time.time()

            identified_features = list()

            review_sentence = self.xls_manipulator.read_phrase_from_cell(SheetName, SentenceContentLabel, row)
            text_processor.text_processing(review_sentence[0])
            processed_sentence = set(text_processor.get_processed_text())

            for collocation in self.collocation_list:
                if collocation.issubset(processed_sentence):
                    identified_features.append(collocation)

            feature_string = ""

            for feature in identified_features:

                if len(feature_string):
                    feature_string += ";" + str(feature).replace("', '", " ").replace("{'", "").replace("'}", "")

                else:
                    feature_string = str(feature).replace("', '", " ").replace("{'", "").replace("'}", "")

            if feature_string:
                self.xls_manipulator.write_phrase_to_cell(SheetName, ExtractedFeatureLabel, row, feature_string)

            print("Collocation Program Execution Time: ", time.time() - time_start)


if __name__ == '__main__':

    # Path to file with reviews in which features are identified for evaluation
    FilePath = "./supporting_files/"
    FileName = "Experiment_template.xlsx"
    FullPathCollocationExtraction = FilePath + FileName
    StartRowReview = 2
    StopRowReview = 155
    rowsWithReviews = list(range(StartRowReview, StopRowReview + 1))

    # Path with file from which collocation lexicon is built
    FilePath = "./supporting_files/"
    FileName = "com.zentertain.photoeditor_lexicon.xlsx"
    FullPathCollocationLexicon = FilePath + FileName
    StartRowLexicon = 2
    StopRowLexicon = 3754

    # Retrieve collocations for a given significance level
    sign_level = significance_level_to_ciritical_value(0.005)

    program_collocation_finding = CollocationFindingProgram(FullPathCollocationLexicon, StartRowLexicon, StopRowLexicon)
    program_collocation_finding.get_collocations_for_given_critical_value(sign_level)

    program_collocation_finding.read_file(FullPathCollocationExtraction)


    # for i in [49, 104, 134, 87, 82, 85, 59, 108, 26, 30, 79, 38, 3, 37, 101, 115, 50, 74, 114, 68, 131, 72, 98, 54, 150, 4, 91, 138, 31, 52, 128]:
    #     program_collocation_finding.run_collocation(i, i)

    for i in rowsWithReviews:
        program_collocation_finding.run_collocation(i, i)

    program_collocation_finding.save_file()




