from django.shortcuts import render_to_response, render, RequestContext, HttpResponseRedirect, HttpResponse
from django.conf.urls import patterns, url
from rest_framework.decorators import api_view
from rest_framework.response import Response
import requests
import json
from django.contrib import messages
from django.utils.crypto import get_random_string
from datetime import datetime
from django.utils.timezone import utc
from sample.models import Test, Question, Options, Admin, Answers, UserAnswers, Scores, User, Store
from django.core.context_processors import csrf
from django.contrib.auth import login, authenticate, logout
from django.core import serializers
import _mysql
import MySQLdb


def plot(request):
    return render(request, "plot.html")


def analysis(request):
    store_details = Store.objects.all()
    test_list = [int(store_detail.test) for store_detail in store_details]
    cutoff_list = [int(store_detail.cutoff_count) for store_detail in store_details]
    percentage_list = [float(store_detail.overall_percentage) for store_detail in store_details]
    return render_to_response('analysis.html',
                              {'test_list': test_list, 'cutoff_list': cutoff_list, 'percentage_list': percentage_list},
                              RequestContext(request))


def signup(request):
    return render(request, "signup.html")


def home(request):
    return render(request, "home.html")


def instructor(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        Username = 'peri'
        Password = '12345'
        if username != Username:
            error = "Wrong credentials"
            return render_to_response("home.html", {'error': error}, RequestContext(request))
    return render_to_response("entryform.htm", RequestContext(request))


def fbLogin(request):
    return render(request, 'index.html')


def err(request):
    return render(request, 'loggedin.html')


def testpage(request):
    tests = Test.objects.all()
    return render_to_response('taketest.html', {'tests': tests}, RequestContext(request))


def Questions_display(request, testid):
    c = {}
    c.update(csrf(request))
    try:
        question_no = 0
        questions = Question.objects.filter(test_id=testid)[question_no]
        options = Options.objects.filter(question=questions.pk)
        a = []
        for i in options:
            a.append(i.value)
        username = User.objects.all()
        testdetails = Test.objects.all()
        current_user_name = request.user.name
        testId = testid
        return render_to_response('starttest.html', {'testID': testId, 'questions': questions, 'quesno': question_no,
                                                     'optionset': options, 'a1': a[0], 'a2': a[1], 'a3': a[2],
                                                     'a4': a[3],
                                                     'username': username,
                                                     'testdetails': testdetails,
                                                     'current_user_name': current_user_name}, RequestContext(request))

    except IndexError:

        return HttpResponseRedirect('/result/')


def result(request):
    value = 1
    testid = Test.objects.get(id=value)
    return render(request, 'testresult.html', {'testid': testid})


def testPages(request):
    test_table = Test.objects.all()
    if test_table:
        return render_to_response('createtest.html', {'test_table': test_table}, RequestContext(request))


@api_view(['POST'])
def apifblogin(request):
    details = json.loads(
        requests.get("https://graph.facebook.com/me?access_token=" + request.DATA['accesstoken']).content)
    if "error" not in details:
        name = details['name']
        mailid = details['email']
        password = get_random_string()
        try:
            User.objects.get(username=mailid)
        except User.DoesNotExist:
            user = User(username=mailid, name=name)
            user.set_password(password)
            user.save()
            authenticated_user = authenticate(username=mailid, password=password)
            login(request, authenticated_user)
            return Response({'name': name}, 200)
        return Response({'error': "You are already registered"}, 400)
    return Response({'error': "Not a valid user"}, 400)


def createtest(request):
    c = {}
    c.update(csrf(request))
    if request.method == 'POST':
        testname = request.POST['testname']
        testdescription = request.POST['testdescription']
        testduration = request.POST['testduration']

        testtable = Test(testName=testname, description=testdescription, duration=testduration,
                         startDate=datetime.now(), endDate=datetime.now())
        testtable.save()
        test_table = Test.objects.all()
        return render_to_response('createtest.html', {'test_table': test_table}, RequestContext(request))


@api_view(['POST'])
def questionpost(request):
    if request.method == 'POST':
        testid = request.POST.get('testid')
        question = request.POST.get('question')
        option1 = request.POST.get('option1')
        option2 = request.POST.get('option2')
        option3 = request.POST.get('option3')
        option4 = request.POST.get('option4')
        answerIndex = request.POST.get('answerindex')
        optionslist = [option1, option2, option3, option4]
        questionSave = Question(value=question, test=Test.objects.get(id=testid))
        questionSave.save()
        saveOptions = Options(question=questionSave, optionType='MCQ', value=option1)
        saveOptions.save()
        saveOptions = Options(question=questionSave, optionType='MCQ', value=option2)
        saveOptions.save()
        saveOptions = Options(question=questionSave, optionType='MCQ', value=option3)
        saveOptions.save()
        saveOptions = Options(question=questionSave, optionType='MCQ', value=option4)
        saveOptions.save()

        if int(answerIndex) <= 3:
            saveanswer = Answers(question=Question.objects.get(value=question),
                                 option=Options.objects.get(value=optionslist[int(answerIndex)]))
            saveanswer.save()
            name = "fgxg"
        return Response({'name': name}, 200)


def savedtest(request):
    return render(request, 'savedtest.html')


def addquestions(request):
    return render(request, 'createtest.html')


def show_test(request):
    if request.method == 'GET':
        testid = request.GET.get('search')
        test = Test.objects.get(id=testid)
        testDetails = Question.objects.filter(test=test)
        return render_to_response('savedtest.html', {'testDetails': testDetails}, RequestContext(request))


@api_view(['POST'])
def useranswers(request):
    try:
        if request.method == 'POST':
            questionid = request.POST['questionid']
            useranswer = request.POST['radio']
            testId = request.POST['testid']
            current_user = request.user
            ques = Question.objects.get(id=questionid)
            selected_option = Options.objects.filter(value=useranswer, question=ques)
            answer = Answers.objects.get(question=questionid)
            option_list = []
            for i in selected_option:
                option_list.append(i.id)
            if option_list[0] == answer.option_id:
                useranswers = UserAnswers(user=User.objects.get(username=current_user),
                                          question=Question.objects.get(id=questionid),
                                          option=Options.objects.get(id=option_list[0]),
                                          test=Test.objects.get(id=testId), isCorrect=True)
                useranswers.save()
            else:
                useranswers = UserAnswers(user=User.objects.get(username=current_user),
                                          question=Question.objects.get(id=questionid),
                                          option=Options.objects.get(id=option_list[0]),
                                          test=Test.objects.get(id=testId), isCorrect=False)
                useranswers.save()
            question_no = int(request.POST['questionno']) + 1
            questions = Question.objects.filter(test=testId)[question_no]
            selected_option = Options.objects.filter(question=questions.pk)
            optionslist = []
            for i in selected_option:
                optionslist.append(i.value)

            return Response({'questions': questions.pk, 'quesno': question_no, 'questionvalue': questions.value,
                             'option1': optionslist[0], 'option2': optionslist[1], 'option3': optionslist[2],
                             'option4': optionslist[3],
                             'test': testId})
    except IndexError:

        return Response({'error': "Not a valid user"}, 400)


def logoutNow(request):
    if request.user.is_authenticated():
        logout(request)
    return HttpResponseRedirect('/home/')


@api_view(['POST'])
def checkresult(request):
    if request.method == 'POST':
        test_id = request.POST.get('testid')
        current_user = request.user
        answer_count = UserAnswers.objects.filter(isCorrect=True, test=test_id, user=current_user).count()
        question_count = UserAnswers.objects.filter(test=test_id, user=current_user).count()
        total_marks = question_count * 5
        score = answer_count * 5
        save_score = Scores(user=User.objects.get(username=current_user), score=score,
                            test=Test.objects.get(id=test_id))
        save_score.save()
    return Response({'score': score, 'totalmarks': total_marks})


def store_save(request):
    test_value = 1
    filterd_test = Scores.objects.filter(test=test_value)
    sum_of_score = []
    for i in filterd_test:
        sum_of_score.append(i.score)
    total_sum_of_score = sum(sum_of_score)
    no_of_students = Scores.objects.filter(test=test_value).count()
    question_count = UserAnswers.objects.filter(test=test_value).count()
    total_marks = question_count * 5
    overall_percentage = (float(total_sum_of_score) / float(total_marks)) * 100

    # ---------------  difficulty level-------------------#
    test_id = 1
    current_user = request.user
    questions_count = UserAnswers.objects.filter(test=test_id, user=current_user).count()
    max_score = (questions_count * 5) - 3
    total_no_of_students = Scores.objects.filter(test=test_id).count()
    who_got_gr_max = Scores.objects.filter(score__gte=max_score).count()
    if who_got_gr_max > (total_no_of_students / 2):
        diff_level = "LOW"
    else:
        diff_level = "HIGH"
        #--------------------------------Saving into store-----------------#
    save_last_test = Store(test=test_id, overall_percentage=overall_percentage, cutoff_count=who_got_gr_max)
    save_last_test.save()
    return render_to_response('entryform.htm', {'sum_of_score': total_sum_of_score, 'no_of_students': no_of_students,
                                                'total_marks': total_marks, 'percentage': overall_percentage,
                                                'max_score': max_score, 'total_no_of_students': total_no_of_students,
                                                'who_gor_gr_max': who_got_gr_max, 'diff_level': diff_level},
                              RequestContext(request))

