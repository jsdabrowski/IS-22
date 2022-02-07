from nltk.corpus import webtext
from nltk.collocations import BigramCollocationFinder
from nltk.metrics import BigramAssocMeasures
from nltk.corpus import stopwords
from nltk import word_tokenize


class CollocationAlgorithm:

    # List with tokenized corpus stop words
    text_corpus = None

    # TODO wywalic prawdopodobnie
    stopset = None

    # Collocation Finder
    tcf = None

    # All the collocations
    bigram_freq = None

    # Collocation with frequency above N
    bigram_freq_above = None

    # Top-N collocations with highest frequency
    bigram_freq_top = None

    # Top-N collocations with highest likelihood ratio
    bigram_likelihood_top = None

    # All collocations with likelihood ratio
    bigram_likelihood_all = None

    def __init__(self, text_corpus):
        """ Given a text corpus it finds bi-gram collocations

        :param text_corpus: list with tokenized text
        :return : Nothing
        """

        self.text_corpus = text_corpus
        words = [w.lower() for w in self.text_corpus]

        ''' 
        Finding bi-gram collocation with window size 3 (2-word distance)
        Given word w_i, w_j, and their positions i, j in sentence s, distance (offset) is 
        defined d = j-i. Windows is defined as w = d+1
        '''

        self.tcf = BigramCollocationFinder.from_words(words, window_size=3)

        # TODO Can be probably removed as I already implemented: Filtering stop words
        # self.stopwords = (stopwords.words('english'))
        # filter_stops = lambda w: len(w) < 3 or w in self.stopwords
        # self.tcf.apply_word_filter(filter_stops)

        # All the collocations
        self.bigram_freq = list(self.tcf.ngram_fd.keys())

        # Collocation with frequency above N
        self.bigram_freq_above = [item[0] for item in self.tcf.ngram_fd.items() if item[1] > 13]

        # Top-N collocations with highest frequency
        self.bigram_freq_top = self.tcf.nbest(BigramAssocMeasures.raw_freq, 5)

        # Top-N collocations with highest likelihood ratio
        self.bigram_likelihood_top = self.tcf.nbest(BigramAssocMeasures.likelihood_ratio, 10)

        # All the collocations with likelihood ratio
        self.bigram_likelihood_all = self.tcf.score_ngrams(BigramAssocMeasures.likelihood_ratio)

    def get_bigram_freq(self):

        return self.bigram_freq

    def get_bigram_freq_above(self):

        return self.bigram_freq_above

    def get_bigram_freq_top(self):

        return self.bigram_freq_top

    def get_bigram_likelihood_top(self):

        return self.bigram_likelihood_top

    def get_bigram_likelihood_ranked(self, critical_value=None):

        """
                Return ranked list of collocations with given confidence level specified by
                critical value as input
                :param critical_value: critical value
                :return : Lists with collocations
        """

        # If critical_value level for given confidence level (significance level), df1 = 1
        # 3.841 -> 0.95 (alpha = 0.05);  6.635 -> 0.99 (alpha = 0.01);
        # 7.879 -> 0.995 (alpha = 0.005 ; 10.828-> 0.999 (alpha = 0.001)

        if critical_value:
            return [bigram[0] for bigram in self.bigram_likelihood_all if bigram[1] > critical_value]

        # If no significance level given
        else:
            return [bigram[0] for bigram in self.bigram_likelihood_all]


if __name__ == '__main__':

    # Input text corpus to be search for collocation
    text_corpus = webtext.words('singles.txt')

    # text_corpus = word_tokenize("I prefer not to say tomorrow and other day")
    # print(text_corpus)

    ca = CollocationAlgorithm(text_corpus)

    print(ca.get_bigram_likelihood_ranked(7.879))
    print(ca.get_bigram_freq())










