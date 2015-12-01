__author__ = 'tony'
import os
import django
from datetime import datetime

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myproject.settings")
django.setup()

from sample.models import Question, Options, Answers
from sample.models import Test



def save_tests(no_of_tests):
    for j in range(int(no_of_tests)):
        name = raw_input("ENTER TEST NAME")
        desc = raw_input("ENTER DESCRIPTION")
        duration = raw_input("ENTER TEST DURATION")

        test = Test(testName=name, description=desc, duration=duration, startDate=datetime.now(),
                    endDate=datetime.now())
        test.save()

        n = raw_input("ENTER NUMBER OF QUESTIONS")
        save_questions(test, n)


def save_questions(test, no_of_questions):
    for i in range(int(no_of_questions)):
        question = raw_input("ENTER QUESTION")

        question = Question(value=question, test=test)
        question.save()
        no_of_options = raw_input("ENTER NUMBER OF OPTIONS")
        save_options(question, no_of_options)
        save_answer(question)


def save_options(question, no_of_options):
    for i in range(int(no_of_options)):
        option = raw_input("ENTER OPTION")

        option = Options(value=option, question=question, optionType='MCQ')
        option.save()


def save_answer(question):
    options = question.options_set.all()
    i = 1
    for option in options:
        print i,':', option.value
        i+=1
    answer_index = raw_input('Enter index of correct answer:')
    answer = Answers(question=question,option=options[int(answer_index)-1])
    answer.save()




no_of_tests = raw_input("ENTER NO OF TESTS")
save_tests(no_of_tests)