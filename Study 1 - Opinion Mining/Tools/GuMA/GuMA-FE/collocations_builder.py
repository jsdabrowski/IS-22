"""
The actual program that reads reviews and provide potential features list via collocation algorithm
"""

# TODO check the accuracy if we take review sentence instead review to create collocations

from xls_manipulation import PhraseExtractor
from text_processing import TextProcessing
from algorithm_collocation import CollocationAlgorithm
import time


class CollocationBuilder:

    time_start = time.time()

    SheetName = 'Lexicon' #'Apps'

    # Column index with review content
    ReviewContent = 'A'

    # Rows with reviews from which collocation will be extracted
    RowStart = None
    RowStop = None

    # List of collocations for given critical value
    filtered_collocation_list = list()

    # This probably can be removed
    # filtered_collocation_list_0_01 = list()
    # filtered_collocation_list_0_05 = list()
    # filtered_collocation_list_0_1 = list()

    collocation_algorithm = None
    processed_list_reviews = list()

    def __init__(self, FullPathCollocationLexicon, RowStart, RowStop):

        self.RowStart = RowStart
        self.RowStop = RowStop

        # Text corpus with all the reviews
        text_corpus = list()

        # Open input text
        xls_manipulator = PhraseExtractor(FullPathCollocationLexicon)

        # Text processing
        text_processor = TextProcessing()

        # List with elements that each one corresponds to processed review
        self.processed_list_reviews = list()

        # Read input text
        for row in range(self.RowStart, self.RowStop + 1):
            review_content = xls_manipulator.read_phrase_from_cell(self.SheetName, self.ReviewContent, row)
            text_processor.text_processing(review_content[0])
            processed_review = text_processor.get_processed_text()
            text_corpus += processed_review
            self.processed_list_reviews.append(processed_review)

        # Retrieve all the collocation from text corpus
        self.collocation_algorithm = CollocationAlgorithm(text_corpus)

        print("Builder collocation time 1: ", time.time() - self.time_start)

    # Get a list of collocations given critical value and input lexicon file
    def get_collocation_given_critical_value(self, critical_value = 7.879):

        # collocation_list_with_list = collocation_algorithm.get_bigram_freq()

        # Given Critical_value level for specific confidence level (significance level), df1 = 1
        # 3.841 -> 0.95 (alpha = 0.05);  6.635 -> 0.99 (alpha = 0.01);
        # 7.879 -> 0.995 (alpha = 0.005 ; 10.828-> 0.999 (alpha = 0.001)
        # Setting critical value for extracting collocations

        collocation_list_with_list = self.collocation_algorithm.get_bigram_likelihood_ranked(critical_value)

        collocation_list_with_set = [set(element) for element in collocation_list_with_list if len(set(element)) > 1]

        # Make a list of unique collocations where the order does not matter
        unique_collocation_list = list()

        for element in collocation_list_with_set:

            if element not in unique_collocation_list:
                unique_collocation_list.append(element)

        """List with collocations that not occur in more than 3 reviews"""
        filtered_collocation_list = list()

        # TU PROBLEM SIE ZACZYNA I MOZNA TO USPRAWNIC

        start_time = time.time()

        for collocation_pair in unique_collocation_list:

            n_occurrence = 0

            for review in self.processed_list_reviews:

                if collocation_pair.issubset(review):
                    n_occurrence += 1

            if n_occurrence >= 3:
                filtered_collocation_list.append(collocation_pair)

        self.filtered_collocation_list = filtered_collocation_list

        print("filterting: ", time.time() - start_time)

        print("Builder collocation time 2: ", time.time() - self.time_start)

    # Return the list of collocations (features)
    def get_features(self):

        return self.filtered_collocation_list


if __name__ == '__main__':

    # Path with file from which collocation lexicon is built
    FilePath = "/Users/jacekdabrowski/Desktop/"
    FileName = "Netflix_14K.xlsx"
    FullPathCollocationLexicon = FilePath + FileName
    StartRowLexicon = 2
    StopRowLexicon = 1000

    collocation_builder = CollocationBuilder(FullPathCollocationLexicon, StartRowLexicon, StopRowLexicon)
    collocation_builder.get_collocation_given_critical_value(10.828)
    print(collocation_builder.get_features())

