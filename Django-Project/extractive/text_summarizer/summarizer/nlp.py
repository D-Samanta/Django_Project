# import library

from string import punctuation
import pandas as pd
import re
import spacy
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from nltk.tokenize import word_tokenize, sent_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from textblob import TextBlob


ps = PorterStemmer()
tfidf = TfidfVectorizer()
nlp = spacy.load("en_core_web_sm")


# Function for Data Cleaning

def spell_correction(text):
    tb = TextBlob(text)
    return tb.correct().string


def remove_punc(text):
    for char in punctuation:
        text = text.replace(char, '')
    return text


def remove_stopwords(text):
    new_text = []
    for word in text.lower().split():
        if word not in stopwords.words('english'):
            new_text.append(word)
    return ' '.join(new_text)


def stem_words(text):
    new_text = []
    for word in text.split():
        new_text.append(ps.stem(word))
    return ' '.join(new_text)


# Function Feature extraction

def sent_length(text):
    token = word_tokenize(text)
    return len(token)


def noun_count(sent):
    doc = nlp(sent)
    count = 0
    for i in range(len(doc)):
        if doc[i].pos_ == 'PROPN':
            count += 1
    return count


def count_numerals(sentence):
    return len(re.findall(r'\b\d+(?:\.\d+)?\b', sentence))


# code for text summarizer_1 ( tf-idf + noun + numeric )

def text_summarizer_1(input_text, summary_size):
    # input_text = 'I am a good boy. Ram is a good boy. Everyone likes Ram.'
    sent = sent_tokenize(input_text)
    # desired_summary_size = 50
    n = int(len(sent) * (summary_size / 100))
    df = pd.DataFrame({'sent': sent})

    # Data preprocessing

    # 1.Spelling correction
    # df['correct_sent'] = df['sent'].apply(spell_correction)
    df['correct_sent'] = df['sent']

    # 2. Remove punctuation

    df['sent_punc'] = df['correct_sent'].apply(remove_punc)

    # Remove stopwords

    df['sent_sw'] = df['sent_punc'].apply(remove_stopwords)

    # Stemming

    df['stem_sent'] = df['sent_sw'].apply(stem_words)

    # Feature extraction
    # Feature: 1 - Sentence length score

    df['sent_length'] = df['stem_sent'].apply(sent_length)

    # Feature: 2 - Tf-Idf Score

    bow = tfidf.fit_transform(df['stem_sent'])
    df['tfidf_sent_score'] = bow.mean(axis=1)

    # Feature : 3 - proper noun

    df['noun_count'] = df['sent_sw'].apply(noun_count)
    df['noun_count_score'] = df['noun_count'] / df['sent_length']

    # Feature : 4 - Count numerical

    df['numeric_count'] = df['sent_sw'].apply(count_numerals)
    df['numeric_count_score'] = df['numeric_count'] / df['sent_length']

    # Final Feature

    df['grand_score'] = (df['tfidf_sent_score'] + df['noun_count_score'] + df['numeric_count_score']) / 3

    summary_index = df['grand_score'].nlargest(n).index.tolist()

    summary_df = df.loc[summary_index, :]

    summary_df.sort_index(inplace=True)

    summary_text = ' '.join(summary_df['correct_sent'].astype(str))

    return summary_text


# code for text summarizer_2




