from django.shortcuts import render, HttpResponse, redirect

from .models import Text
from .nlp import text_summarizer_1
from django.contrib import messages


def handle_upload(request):
    if request.method == 'POST':
        if request.FILES:
            uploaded_file = request.FILES['file']
            input_text = uploaded_file.read().decode('utf-8')

            summary_output = text_summarizer_1(input_text, 40)
            input_len = len(input_text)
            summary_len = len(summary_output)
            reduce = int(((input_len - summary_len) / input_len) * 100)

            text = Text(input_text=input_text, summary_output=summary_output)
            text.save()
            messages.success(request, "Your text has been successfully save in database")

            params = {'input_text': input_text,
                      'summary_output': summary_output,
                      'input_len': input_len,
                      'summary_len': summary_len,
                      'reduce': reduce,
                      }
            # return render(request, 'summarizer/upload.html', params)
            return render(request, 'summarizer/after_summarize.html', params)
        else:
            messages.error(request, "Please Give input file to Summarizer")

            return render(request, 'summarizer/file_input.html')


def handle_text(request):
    if request.method == "POST":
        input_text = request.POST['input_text']
        if len(input_text) > 2:

            summary_output = text_summarizer_1(input_text, 30)
            input_len = len(input_text)
            summary_len = len(summary_output)
            reduce = int(((input_len - summary_len) / input_len) * 100)

            text = Text(input_text=input_text, summary_output=summary_output)
            text.save()
            messages.success(request, "Your text has been successfully save in database")

            params = {'input_text': input_text,
                      'summary_output': summary_output,
                      'input_len': input_len,
                      'summary_len': summary_len,
                      'reduce': reduce,

                      }

            return render(request, 'summarizer/after_summarize.html', params)
        else:
            messages.error(request, "Please Give sufficient input text to Summarizer")

            return render(request, 'summarizer/text_input.html')
