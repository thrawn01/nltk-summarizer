
from nltk.tokenize import RegexpTokenizer
from nltk.probability import FreqDist
from nltk.corpus import stopwords
from collections import defaultdict
import nltk.data
import re

# Here so these get initialized at module load time ( They take a while )
sentence_tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
word_tokenizer = RegexpTokenizer('\w+')
non_nouns = stopwords.words()


def most_frequent_words(original_sentences, frequent_words, num_sentences):
    # Lower the case to make matching simple
    sentences_lowered = [sentence.lower() for sentence in original_sentences]
    # a map of sentences with the highest concentration of frequent words
    sentences = defaultdict(int)
    # For the most frequent words
    for word in frequent_words:
        # While looking through our lowercased sentences
        for i in range(0, len(sentences_lowered)):
            # If we find the word in the sentence
            if word in sentences_lowered[i]:
                # Note the count in the map
                sentences[original_sentences[i]] += 1
    # Swap the sentence with the count
    sentences = dict(zip(sentences.values(), sentences.keys()))
    # sort the keys so we get the greatest frequency of words first
    keys = sorted(sentences.keys(), reverse=True)
    # Return the top num_sentences of high frequency worded sentences
    return [sentences[keys[i]] for i in range(0, num_sentences)]


def get_context(needle, haystack, context):
    # Locate the value in the original_sentences
    for i in range(0, len(haystack)):
        if haystack[i] == needle:
            prefix = i - context
            if prefix < 0:
                prefix = 0
            # Return the number of context sentences asked for
            return haystack[prefix:i+(context+1)]


def summarize(num_sentences, context_lines, text):
    result = {}
    # Remove newlines from the text
    text = re.sub('\s*[\n|\r|\r\n]\s*', ' ', text)
    # Separate all the words
    base_words = [word.lower() for word in word_tokenizer.tokenize(text)]
    # Remove non-nouns from the words collected
    words = [word for word in base_words if word not in non_nouns]
    # Use a frequency distribution to encode how often a word occurs
    frequencies = FreqDist(words)
    # Now create a set of the most frequent words, limit top 100 words
    frequent_words = [pair[0] for pair in frequencies.items()[:100]]
    # Separate all the sentences
    original_sentences = sentence_tokenizer.tokenize(text)
    # Find the sentences with the most frequent words
    high_freq_sentences = most_frequent_words(original_sentences,
                                              frequent_words, num_sentences)
    # Create a map with the High Frequence Sentences as the key,
    # and the context as the value
    for sentence in high_freq_sentences:
        # Get context for each of the high freq sentences
        result[sentence] = get_context(sentence,
                                       original_sentences, context_lines)
    return result
