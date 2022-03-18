import nltk
from nltk.corpus import stopwords
import re
import string


# tokenize helper function
def text_process(raw_text):
    """
    Takes in a string of text, then performs the following:
    1. Remove all punctuation
    2. Remove all stopwords
    3. Returns a list of the cleaned text
    """
    # Check characters to see if they are in punctuation
    nopunc = [char for char in list(raw_text) if char not in string.punctuation]

    # Join the characters again to form the string.
    nopunc = ''.join(nopunc)

    # Now just remove any stopwords
    return ' '.join([word for word in nopunc.lower().split() if word.lower() not in stopwords.words('english')])


def remove_non_words(tweet):
    # import nltk
    # nltk.download('stopwords')
    # data = nltk.corpus.comtrans.aligned_sents('alignment-en-fr.txt')
    # nltk.data.path.append('gs://cloud-project-bucket-1981/stopwords')
    sw = nltk.corpus.stopwords.words("english")
    output_string = ''
    print(tweet)
    # Remove Punctuation and split 's, 't, 've with a space for filter
    tweet = re.sub(r'[' + string.punctuation.replace('@', '') + ']+', ' ', tweet)
    # Remove single space remaining at the front of the tweet.
    tweet = tweet.lstrip(' ')
    # Remove characters beyond Basic Multilingual Plane (BMP) of Unicode:
    tweet = ''.join(c for c in tweet if c <= '\uFFFF')

    for word in tweet.split(' '):
        if word[:1].isalpha():
            output_string += word + ' '
        else:
            # non_words.append(word)
            pass

    return output_string


def text_cleaning(df):
    df["words"] = df["words"].apply(lambda x: remove_non_words(x))
    df["words"] = df["words"].apply(lambda x: text_process(x))

    return df