import copy
import openpyxl
from nltk.stem.porter import *
import time


# Evaluating concept expression using gold standard and extracted phrases (what was matched and what not)
class TokenBasedEvaluator:

    # Pre-process input gold standard and extracted phrases
    def __init__(self, expression_gold_standard, expression_extracted):
        self.Expression_gold_standard = expression_gold_standard
        self.Expression_extracted = expression_extracted
        self.Expression_gold_standard = self.Expression_gold_standard.lower()
        self.Expression_extracted = self.Expression_extracted.lower()
        self.Expression_gold_standard = re.sub(r"[,.;@#?!&$]+\ *", " ", self.Expression_gold_standard)
        self.Expression_extracted = re.sub(r"[,.;@#?!&$]+\ *", " ", self.Expression_extracted)

    # Check if extracted phrases and gold standard phrases is a substring of each other

        self.DifferenceInTokens = abs(len(self.Expression_extracted.split())-len(self.Expression_gold_standard.split()))

        # Variable for features as set
        # Variable indicating if extracted or golden features is a subset of each other - necessary condition.
        self.feature_subset_of_each_other = 0
        # print("Number of elements of feature expressions: ", set(self.Expression_extracted.split()).__len__(), set(self.Expression_gold_standard.split()).__len__())
        self.feature_extracted_set = set()
        self.feature_gold_set = set()

        # Variable for features as sequence
        self.feautre_extracted_sequence = list()
        self.feature_gold_sequence = list()

    # Check how many words have gold standard and extracted expressions in common
    # Use Porter Stemmer to normalize words of each expression to a common root word
    # Must be always run before evaluate_mach or evaluate_partial_match
    def check_matched_word_number(self):

        stemmer = PorterStemmer()


    # Condition for token-based subset matching: Check if extracted and golden features are subset each other
        for i in self.Expression_gold_standard.split():
            self.feature_gold_set.add(stemmer.stem(i))

        for i in self.Expression_extracted.split():
            self.feature_extracted_set.add(stemmer.stem(i))

        if self.feature_gold_set.issubset(self.feature_extracted_set) or self.feature_extracted_set.issubset(self.feature_gold_set):
            self.feature_subset_of_each_other = True
        else:
            self.feature_subset_of_each_other = False

    # Normalizing terms of extracted and golden feature as approache may return their normalized form
    # Punishing the performance of the approach because of that may be not fair

        for i in self.Expression_gold_standard.split():
            self.feature_gold_sequence.append(stemmer.stem(i))

        for i in self.Expression_extracted.split():
            self.feautre_extracted_sequence.append(stemmer.stem(i))

    # Print features that are compared
    def print_compared_phrases(self):
        print("Gold Standard Expression: " + self.Expression_gold_standard)
        print("Extracted Expression: " + self.Expression_extracted)

        # Probably remove
        # print("Matched words: ", self.NoMatchedWord)
        # print("Differences in token: ", self.DifferenceInTokens)

        print("Annotated feature set: ", self.feature_gold_set)
        print("Extracted feature set: ", self.feature_extracted_set)

        print("Annotated feature sequence: ", self.feature_gold_sequence)
        print("Extracted feature sequence: ", self.feautre_extracted_sequence)

    def new_evaluate_partial_match_feature_set(self, word_number_threshold):
        if self.feature_subset_of_each_other and (abs(self.feature_extracted_set.__len__() - self.feature_gold_set.__len__()) <= word_number_threshold):
            # print("New Partial Match Successful for feature as Set. The threshold set for: ", word_number_threshold)
            return True
        else:
            # print("Unsuccessful New Partial Match for feature as Set. The threshold set for: ", word_number_threshold)
            return False

    # Corrected exact match for evaluating feature when it is defined as a set of terms
    def new_evaluate_exact_match_feature_set(self):
        if (self.feature_subset_of_each_other and abs(self.feature_extracted_set.__len__() - self.feature_gold_set.__len__()) == 0):
            # print("Successful New Exact Match for feature as Set.")
            return True
        else:
            # print("Unsuccessful New Exact Match for feature as Set.")
            return False


    # New implementaiton for evaluating match when feature is defined as sequence
    def new_evaluate_partial_match_feature_sequence(self, word_number_threshold):

        m = len(self.feautre_extracted_sequence)
        n = len(self.feature_gold_sequence)

        # Function implementing dynaming programmin solution to find the largest common substring, here largest common sequence of terms
        LCSubTerm = LCSubStr(self.feautre_extracted_sequence, self.feature_gold_sequence, m, n)

        # Parameter to define what match we want to check
        k = (m - LCSubTerm) + (n - LCSubTerm)

        if k <= word_number_threshold:
            # print("Successful New Partial Match for Feature as Sequence. The threshold set for:" , word_number_threshold)
            return True
        else:
            # print("Unsuccessful New Partial Match for Feature as Sequence. The threshold set for:" , word_number_threshold)
            return False

    def new_evaluate_exact_match_feature_sequence(self):

        m = len(self.feautre_extracted_sequence)
        n = len(self.feature_gold_sequence)

        # Function implementing dynaming programmin solution to find the largest common substring, here largest common sequence of terms
        LCSubTerm = LCSubStr(self.feautre_extracted_sequence, self.feature_gold_sequence, m, n)

        # Parameter to define what match we want to check
        k = (m - LCSubTerm) + (n - LCSubTerm)

        if k == 0:
            # print("Successful New Exact Match for Feature as Sequence.")
            return True
        else:
            # print("Unsuccessful New Exact Match for Feature as Sequence.")
            return False


# Extracting concept expression from a cell
class PhraseExtractor:

    FullPath = None

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
        # self.workbook.save(self.FilePath + self.FileName)
        self.workbook.save(self.FullPath)



def compare_extracted_concepts_improved(labeled_concepts, extracted_concepts, option):
    extracted = copy.deepcopy(extracted_concepts)
    labeled = copy.deepcopy(labeled_concepts)

    # True positive indexes
    extracted_matched_indexes = list()
    # False positive
    extracted_unmatched_indexes = list()
    extracted_unmatched_concepts = list()
    # False negative indexes
    labeled_unmatched_indexes = list()
    labeled_unmatched_concepts = list()
    # Matched relationship
    labeled_matched_indexes = list()

    # List of matched indexes between extracted and labelled concepts (extracted, labelled)
    matched_relationship_concepts = list()
    matched_relationship_indexes = list()

    # JUST ADDED BELOW, matched true positives
    extracted_matched_concepts = list()
    labeled_matched_concepts = list()


    # Variable for storing information if concepts matched
    token_evaluator = None

    # Find matched extracted and labeled concepts
    for index in range(0, len(extracted)):
        for index_lab in range(0, len(labeled)):

            TokenEvaluator = TokenBasedEvaluator(labeled[index_lab], extracted[index])
            TokenEvaluator.check_matched_word_number()

            # Selecting option for evaluating matching extracted and labeled concepts
            # Select if compare as sequence or set
            if option == 0:
                token_evaluator = TokenEvaluator.new_evaluate_exact_match_feature_set()
            if option == 1:
                token_evaluator = TokenEvaluator.new_evaluate_partial_match_feature_set(1)
            if option == 2:
                token_evaluator = TokenEvaluator.new_evaluate_partial_match_feature_set(2)

            if token_evaluator and index_lab not in labeled_matched_indexes and index not in extracted_matched_indexes:
                matched_relationship_indexes.append([index, index_lab])

                matched_relationship_concepts.append(str(labeled[index_lab]) + ' == ' + str(extracted[index]))

                # To compare GuMa and ReUS
                # matched_relationship_concepts.append(str(labeled[index_lab]) + ' == ' + str(labeled[index_lab]))

                # JUST ADDED BELOW, line to output extracted matched concept
                extracted_matched_concepts.append(str(extracted[index]))
                labeled_matched_concepts.append(str(labeled[index_lab]))

                extracted_matched_indexes.append(index)
                labeled_matched_indexes.append(index_lab)

    # Find unmatched extracted concepts
    for index in range(0, len(extracted)):
        if index not in extracted_matched_indexes:
            extracted_unmatched_indexes.append(index)
            extracted_unmatched_concepts.append(extracted[index])

    # Find unmatched labeled concepts
    for index in range(0, len(labeled)):
        if index not in labeled_matched_indexes:
            labeled_unmatched_indexes.append(index)
            labeled_unmatched_concepts.append(labeled[index])

    # print('Matched relationship concepts: ', matched_relationship_concepts)
    # print('Extracted unmatched concepts: ', extracted_unmatched_concepts)
    # print('Labeled unmatched concepts: ', labeled_unmatched_concepts)

    matched_relationship = copy.deepcopy(matched_relationship_concepts)
    no_matched_labeled_concepts = copy.deepcopy(labeled_unmatched_concepts)
    no_matched_extracted_concepts = copy.deepcopy(extracted_unmatched_concepts)

    # JUST ADDED BELOW, true positives - extracted expressions
    matched_extracted_concepts = copy.deepcopy(extracted_matched_concepts)
    matched_labeled_concepts = copy.deepcopy(labeled_matched_concepts)

    return matched_relationship, no_matched_labeled_concepts, no_matched_extracted_concepts, matched_extracted_concepts, labeled_matched_concepts


# Dynamic Programming implementation of LCS problem
def LCSubStr(X, Y, m, n):

    # Create a table to store lengths of
    # longest common suffixes of substrings.
    # Note that LCSuff[i][j] contains the
    # length of longest common suffix of
    # X[0...i-1] and Y[0...j-1]. The first
    # row and first column entries have no
    # logical meaning, they are used only
    # for simplicity of the program.

    # LCSuff is the table with zero
    # value initially in each cell
    LCSuff = [[0 for k in range(n + 1)] for l in range(m + 1)]

    # To store the length of
    # longest common substring
    result = 0

    # Following steps to build
    # LCSuff[m+1][n+1] in bottom up fashion
    for i in range(m + 1):
        for j in range(n + 1):
            if (i == 0 or j == 0):
                LCSuff[i][j] = 0
            elif (X[i - 1] == Y[j - 1]):
                LCSuff[i][j] = LCSuff[i - 1][j - 1] + 1
                result = max(result, LCSuff[i][j])
            else:
                LCSuff[i][j] = 0
    return result


class EvaluationMethods:
    """
    Class to evalaute the results for feature extraction techniques

    """

    def __init__(self, FullPathEvaluation, RowStart=None, RowStop=None, GivenList = None):

        # Code start time
        start_time = time.time()

        SheetName = 'Apps'

        # Column index with extracted and labelled expression H/J
        ColumnLabeledRead = 'H'
        ColumnExtractedRead = 'J'


        # Open xls file
        PhraseReader = PhraseExtractor(FullPathEvaluation)

        ListIteration = list()

        if GivenList != None and RowStart == None and RowStop == None:

            ListIteration = GivenList

        elif GivenList == None and RowStart != None and RowStop != None:

            ListIteration = range(RowStart, RowStop + 1)

        else:

            raise ValueError('A very specific bad thing happened.')

        # Read concept expression from a cell and represent as list
        # for Row in range(RowStart, RowStop + 1):
        for Row in ListIteration:

            LabeledConcepts = PhraseReader.read_phrase_from_cell(SheetName, ColumnLabeledRead, Row)
            ExtractedConcepts = PhraseReader.read_phrase_from_cell(SheetName, ColumnExtractedRead, Row)

            LabeledConcepts_0 = copy.deepcopy(LabeledConcepts)
            ExtractedConcepts_0 = copy.deepcopy(ExtractedConcepts)
            LabeledConcepts_1 = copy.deepcopy(LabeledConcepts)
            ExtractedConcepts_1 = copy.deepcopy(ExtractedConcepts)
            LabeledConcepts_2 = copy.deepcopy(LabeledConcepts)
            ExtractedConcepts_2 = copy.deepcopy(ExtractedConcepts)

            # Compare extracted expression for a given sentence using exact match
            MatchedRelationship, NotMatchedLabeledConcepts, NotMatchedExtractedConcepts, MatchedExtractedConcepts, MatchedLabeledConcepts = compare_extracted_concepts_improved(
                LabeledConcepts_0, ExtractedConcepts_0, 0)

            # True positive relationship
            ExactMatchedColumn = 'N'
            # True positive
            ExactMatchedExtractedColumn = 'O'
            ExactMatchedLabeledColumn = 'AB'
            # False positive
            NotExactMatchedExtractedColumn = 'P'
            # False negative
            NotExactMatchedLabeledColumn = 'Q'

            # Write concept expression to a cell representing matched and unmatched concepts
            PhraseReader.write_phrase_to_cell(SheetName, ExactMatchedColumn, Row,
                                              str(MatchedRelationship).replace('"', "'").replace("['", "").replace("']",
                                                                                                                   "").replace(
                                                  "', '", ";").replace("[]", ""))
            PhraseReader.write_phrase_to_cell(SheetName, NotExactMatchedLabeledColumn, Row,
                                              str(NotMatchedLabeledConcepts).replace('"', "'").replace("['",
                                                                                                       "").replace("']",
                                                                                                                   "").replace(
                                                  "', '", ";").replace("[]", ""))
            PhraseReader.write_phrase_to_cell(SheetName, NotExactMatchedExtractedColumn, Row,
                                              str(NotMatchedExtractedConcepts).replace('"', "'").replace("['",
                                                                                                         "").replace(
                                                  "']", "").replace("', '", ";").replace("[]", ""))
            PhraseReader.write_phrase_to_cell(SheetName, ExactMatchedExtractedColumn, Row,
                                              str(MatchedExtractedConcepts).replace('"', "'").replace("['", "").replace(
                                                  "']", "").replace("', '", ";").replace("[]", ""))

            PhraseReader.write_phrase_to_cell(SheetName, ExactMatchedLabeledColumn, Row,
                                              str(MatchedLabeledConcepts).replace('"', "'").replace("['", "").replace(
                                                  "']", "").replace("', '", ";").replace("[]", ""))



            # Compare extracted expression for a given sentence using partial match (1)
            MatchedRelationship, NotMatchedLabeledConcepts, NotMatchedExtractedConcepts, MatchedExtractedConcepts, MatchedLabeledConcepts = compare_extracted_concepts_improved(
                LabeledConcepts_1, ExtractedConcepts_1, 1)

            # True positive relationship
            PartialMatched_1_Column = 'R'
            # True positive
            PartialMatched_1_Extracted_Column = 'S'
            PartialMatched_1_Labeled_Column = 'AC'
            # False positive
            NotPartialMatched_1_Extracted_Column = 'T'
            # False negative
            NotPartialMatched_1_Labeled_Column = 'U'

            # Write concept expression to a cell representing matched and unmatched concepts
            PhraseReader.write_phrase_to_cell(SheetName, PartialMatched_1_Column, Row,
                                              str(MatchedRelationship).replace('"', "'").replace("['", "").replace("']",
                                                                                                                   "").replace(
                                                  "', '", ";").replace("[]", ""))
            PhraseReader.write_phrase_to_cell(SheetName, NotPartialMatched_1_Labeled_Column, Row,
                                              str(NotMatchedLabeledConcepts).replace('"', "'").replace("['",
                                                                                                       "").replace("']",
                                                                                                                   "").replace(
                                                  "', '", ";").replace("[]", ""))
            PhraseReader.write_phrase_to_cell(SheetName, NotPartialMatched_1_Extracted_Column, Row,
                                              str(NotMatchedExtractedConcepts).replace('"', "'").replace("['",
                                                                                                         "").replace(
                                                  "']", "").replace("', '", ";").replace("[]", ""))
            PhraseReader.write_phrase_to_cell(SheetName, PartialMatched_1_Extracted_Column, Row,
                                              str(MatchedExtractedConcepts).replace('"', "'").replace("['", "").replace(
                                                  "']", "").replace("', '", ";").replace("[]", ""))

            PhraseReader.write_phrase_to_cell(SheetName, PartialMatched_1_Labeled_Column, Row,
                                              str(MatchedLabeledConcepts).replace('"', "'").replace("['", "").replace(
                                                  "']", "").replace("', '", ";").replace("[]", ""))

            # Compare extracted expression for a given sentence using exact match
            MatchedRelationship, NotMatchedLabeledConcepts, NotMatchedExtractedConcepts, MatchedExtractedConcepts, MatchedLabeledConcepts = compare_extracted_concepts_improved(
                LabeledConcepts_2, ExtractedConcepts_2, 2)

            # True positive relationship
            PartialMatched_2_Column = 'V'
            # True positive
            PartialMatched_2_Extracted_Column = 'W'
            PartialMatched_2_Labeled_Column = 'AD'
            # False positive
            NotPartialMatched_2_Extracted_Column = 'X'
            # False negative
            NotPartialMatched_2_Labeled_Column = 'Y'

            # Write concept expression to a cell representing matched and unmatched concepts
            PhraseReader.write_phrase_to_cell(SheetName, PartialMatched_2_Column, Row,
                                              str(MatchedRelationship).replace('"', "'").replace("['", "").replace("']",
                                                                                                                   "").replace(
                                                  "', '", ";").replace("[]", ""))
            PhraseReader.write_phrase_to_cell(SheetName, NotPartialMatched_2_Labeled_Column, Row,
                                              str(NotMatchedLabeledConcepts).replace('"', "'").replace("['",
                                                                                                       "").replace("']",
                                                                                                                   "").replace(
                                                  "', '", ";").replace("[]", ""))
            PhraseReader.write_phrase_to_cell(SheetName, NotPartialMatched_2_Extracted_Column, Row,
                                              str(NotMatchedExtractedConcepts).replace('"', "'").replace("['",
                                                                                                         "").replace(
                                                  "']", "").replace("', '", ";").replace("[]", ""))
            PhraseReader.write_phrase_to_cell(SheetName, PartialMatched_2_Extracted_Column, Row,
                                              str(MatchedExtractedConcepts).replace('"', "'").replace("['", "").replace(
                                                  "']", "").replace("', '", ";").replace("[]", ""))

            PhraseReader.write_phrase_to_cell(SheetName, PartialMatched_2_Labeled_Column, Row,
                                              str(MatchedLabeledConcepts).replace('"', "'").replace("['", "").replace(
                                                  "']", "").replace("', '", ";").replace("[]", ""))

        # Save xls file
        PhraseReader.save_workbook()

        # Time to execute the program
        stop_time = time.time()
        print('Program end after secs: ', stop_time - start_time)


if __name__ == "__main__":

    # Path with file for which the evaluation of feature expression extraction is done
    FilePath = "./"
    FileName = "Experiment_template.xlsx"
    FullPathEvaluation = FilePath + FileName
    RowStartEvaluation = 2
    RowStopEvaluation = 155

    evaluation_program = EvaluationMethods(FullPathEvaluation, RowStart=RowStartEvaluation, RowStop=RowStopEvaluation)
