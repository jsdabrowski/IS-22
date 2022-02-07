"""
Text-processing class
"""

import re
from nltk import word_tokenize, pos_tag, WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.corpus import wordnet


def get_wordnet_pos(word):
    """ Function return PoS tagg acceptable for WordNet Lemmatization"""

    tag_dict = {
        "J": wordnet.ADJ,
        "N": wordnet.NOUN,
        "V": wordnet.VERB
    }

    return tag_dict.get(word)


class TextProcessing:

    input_sentence = ""
    processed_sentence = ""

    # Lemmatization
    lemmatizer = 0

    # PoS Tagging to be left after filtering sentence
    pos_pattern = ['N', 'J', 'V']

    # PoS Taggin without adjective (different than original implementation BUT CHECK IT)
    # pos_pattern = ['N', 'V']

    # Stopwords
    stop_words = set(stopwords.words('english'))
    stop_words.add("app")
    stop_words.add("fix")
    stop_words.add("please")

    def __init__(self):

        self.lemmatizer = WordNetLemmatizer()

    def text_processing(self, text_corpus):

        self.input_sentence = text_corpus

        # Lowercase, Tokenize, Numerical and Non-english word removal
        sentence_lower_case = self.input_sentence.lower()
        sentence_without_numerical = ''.join([i for i in sentence_lower_case if not i.isdigit()])
        sentence_without_non_english = re.sub(r'[^a-zA-Z]+', ' ', sentence_without_numerical)
        sentence_tokenized = word_tokenize(sentence_without_non_english)

        # Remove probbly
        # sentence_filtered_stop_words = [w for w in sentence_tokenized if not w in stop_words]

        # PoS Tagging, PoS Filtering and Lemmatisation
        sentence_pos = pos_tag(sentence_tokenized)
        sentence_filtered_lemmatized = [self.lemmatizer.lemmatize(i[0], pos=get_wordnet_pos(i[1][0])) for i in sentence_pos
                                        if i[1][0] in self.pos_pattern]

        # Stop word removal
        self.processed_sentence = [w for w in sentence_filtered_lemmatized if not w in self.stop_words]

    def print_result(self):

        print(self.input_sentence)
        print(self.processed_sentence)

    def get_original_text(self):

        return self.input_sentence

    def get_processed_text(self):

        return self.processed_sentence


if __name__ == '__main__':

    example_sentence = "Netflix is a great way to watch series and some movies you missed or forgotten about."

    textprocessor = TextProcessing()
    textprocessor.text_processing(example_sentence)

    textprocessor.print_result()


