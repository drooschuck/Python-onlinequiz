from django.shortcuts import render, redirect, reverse
from . import forms, models
from django.db.models import Sum
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.conf import settings
from datetime import date, timedelta
from quiz import models as QMODEL
from teacher import models as TMODEL


# for showing signup/login button for student
def studentclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request, 'student/studentclick.html')


def student_signup_view(request):
    userForm = forms.StudentUserForm()
    studentForm = forms.StudentForm()
    mydict = {'userForm': userForm, 'studentForm': studentForm}
    if request.method == 'POST':
        userForm = forms.StudentUserForm(request.POST)
        studentForm = forms.StudentForm(request.POST, request.FILES)
        if userForm.is_valid() and studentForm.is_valid():
            user = userForm.save()
            user.set_password(user.password)
            user.save()
            student = studentForm.save(commit=False)
            student.user = user
            student.save()
            my_student_group = Group.objects.get_or_create(name='STUDENT')
            my_student_group[0].user_set.add(user)
        return HttpResponseRedirect('studentlogin')
    return render(request, 'student/studentsignup.html', context=mydict)


def is_student(user):
    return user.groups.filter(name='STUDENT').exists()


@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def student_dashboard_view(request):
    dict = {
        'total_course': QMODEL.Course.objects.all().count(),
        'total_question': QMODEL.Question.objects.all().count(),
    }
    return render(request, 'student/student_dashboard.html', context=dict)


@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def student_exam_view(request):
    courses = QMODEL.Course.objects.all()
    return render(request, 'student/student_exam.html', {'courses': courses})


@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def take_exam_view(request, pk):
    course = QMODEL.Course.objects.get(id=pk)
    total_questions = QMODEL.Question.objects.all().filter(course=course).count()
    questions = QMODEL.Question.objects.all().filter(course=course)
    total_marks = 0
    for q in questions:
        total_marks = total_marks + q.marks

    return render(request, 'student/take_exam.html', {'course': course, 'total_questions': total_questions, 'total_marks': total_marks})


@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def start_exam_view(request, pk):
    course = QMODEL.Course.objects.get(id=pk)
    questions = QMODEL.Question.objects.all().filter(course=course)
    if request.method == 'POST':
        pass
    response = render(request, 'student/start_exam.html', {'course': course, 'questions': questions})
    response.set_cookie('course_id', course.id)
    return response


@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def calculate_marks_view(request):
    try:
        if request.COOKIES.get('course_id') is None:
            print("Error: Course ID not found in cookies")
            return HttpResponseRedirect('student-dashboard')

        course_id = request.COOKIES.get('course_id')
        try:
            course = QMODEL.Course.objects.get(id=course_id)
        except QMODEL.Course.DoesNotExist:
            print(f"Error: Course with ID {course_id} not found")
            return HttpResponseRedirect('student-dashboard')

        total_marks = 0
        questions = QMODEL.Question.objects.all().filter(course=course)
        if not questions:
            print(f"Warning: No questions found for course {course.course_name}")
            
        for i in range(len(questions)):
            selected_ans = request.POST.get(str(i + 1))
            if selected_ans is None:
                print(f"Warning: No answer received for question {i + 1}")
                continue
                
            actual_answer = questions[i].answer
            
            # Debugging information
            print(f"Question {i + 1}: Selected Answer = {selected_ans} ({type(selected_ans)}), Actual Answer = {actual_answer} ({type(actual_answer)})")
            
            # Compare answers exactly as stored in the database
            print(f"Exact comparison: '{selected_ans}' vs '{actual_answer}'")
            
            if selected_ans == actual_answer:
                print(f"Correct answer! Adding {questions[i].marks} marks")
                total_marks += questions[i].marks
            else:
                print(f"Incorrect answer. No marks added. Expected: '{actual_answer}', Got: '{selected_ans}'")

        student = models.Student.objects.get(user_id=request.user.id)
        result = QMODEL.Result()
        result.marks = total_marks
        result.exam = course
        result.student = student
        
        try:
            result.save()
            print(f"Success: Total Marks Recorded: {total_marks} for student {student.user.username}")
        except Exception as e:
            print(f"Error saving result: {str(e)}")
            return HttpResponseRedirect('student-dashboard')

        return HttpResponseRedirect('view-result')
        
    except Exception as e:
        print(f"Unexpected error in calculate_marks_view: {str(e)}")
        return HttpResponseRedirect('student-dashboard')


@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def view_result_view(request):
    courses = QMODEL.Course.objects.all()
    return render(request, 'student/view_result.html', {'courses': courses})


@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def check_marks_view(request, pk):
    course = QMODEL.Course.objects.get(id=pk)
    student = models.Student.objects.get(user_id=request.user.id)
    results = QMODEL.Result.objects.all().filter(exam=course).filter(student=student)
    return render(request, 'student/check_marks.html', {'results': results})


@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def student_marks_view(request):
    courses = QMODEL.Course.objects.all()
    return render(request, 'student/student_marks.html', {'courses': courses})
