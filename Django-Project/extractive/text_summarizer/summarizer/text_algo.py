from django.shortcuts import render, HttpResponse

from django.contrib import messages

from io import StringIO
import string
from nltk import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
import nltk
from nltk.stem.porter import PorterStemmer
from heapq import nlargest

ps = PorterStemmer()


def handle_input(request):
    input_text = request.GET.get('input_text', 'default')
    lower_text = input_text.lower()
    token_text = nltk.word_tokenize(lower_text)
    y = []
    for i in token_text:
        if i.isalnum():  # eliminating character other than alpha nmeric
            y.append(i)

    text = y[:]
    y.clear()

    for i in text:
        if i not in stopwords.words('english') and i not in string.punctuation:
            y.append(i)

    text = y[:]
    y.clear()

    for i in text:
        y.append(ps.stem(i))  # steaming of text

    transform_text = " ".join(y)  # return token word as a text
    word_tokens = word_tokenize(transform_text)
    stop_words = stopwords.words('english')

    word_token_frequencies = {}
    for word in word_tokens:
        if word not in word_token_frequencies.keys():
            word_token_frequencies[word] = 1
        else:
            word_token_frequencies[word] += 1

    max_frequency = max(word_token_frequencies.values())
    for word in word_token_frequencies.keys():
        word_token_frequencies[word] = word_token_frequencies[word] / max_frequency

    sent_token = sent_tokenize(input_text)

    for sent in sent_token:
        sentence = sent.split(" ")

    sentence_scores = {}
    for sent in sent_token:
        sentence = sent.split(" ")
        for word in sentence:
            if word.lower() in word_token_frequencies.keys():
                if sent not in sentence_scores.keys():
                    sentence_scores[sent] = word_token_frequencies[word.lower()]
                else:
                    sentence_scores[sent] += word_token_frequencies[word.lower()]

    select_length = int(len(sent_token) * 0.3)
    summary_list = nlargest(select_length, sentence_scores, key=sentence_scores.get)
    final_summary = [word for word in summary_list]
    summary_output = ' '.join(final_summary)

    params = {'input_text': input_text,
              'lower_text': lower_text,
              'token_text': token_text,
              'transform_text': transform_text,
              'word_tokens': word_tokens,
              'final_summary': final_summary,

              'summary_output': summary_output

              }
    return render(request, 'summarizer/upload.html', params)