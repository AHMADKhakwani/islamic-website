# islamic_app/views.py  ← 100% WORKING VERSION (copy-paste this)

import stripe
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from django.core.mail import send_mail
from .models import Course, Enrollment, Order, Quiz, Question, QuizResult
from .forms import CustomUserCreationForm
from django.contrib.auth import authenticate, login, logout

stripe.api_key = settings.STRIPE_SECRET_KEY


# ==================== PUBLIC PAGES ====================
def index(request):
    return render(request, 'islamic_app/index.html')

def courses(request):
    all_courses = Course.objects.all()
    return render(request, 'islamic_app/courses.html', {'courses': all_courses})

def about(request):
    return render(request, 'islamic_app/about.html')

def tutor(request):
    return render(request, 'islamic_app/tutor.html')

def contact(request):
    success = False
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        subject = request.POST.get("subject")
        message = request.POST.get("message")

        send_mail(
            subject=f"{subject} - Message from {name}",
            message=f"From: {name} <{email}>\n\n{message}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=["itsmez.ab02@gmail.com"],
        )
        success = True
    return render(request, "islamic_app/contact.html", {"success": success})


# ==================== AUTH ====================
def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Signup successful! Please log in.")
            return redirect('islamic_app:login')
    else:
        form = CustomUserCreationForm()
    return render(request, "islamic_app/signup.html", {"form": form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect('islamic_app:index')
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, "islamic_app/login.html")

def logout_view(request):
    logout(request)
    return redirect('islamic_app:index')


# ==================== COURSE + PAYMENT FLOW ====================
@login_required
def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    is_enrolled = Enrollment.objects.filter(user=request.user, course=course).exists()

    context = {
        'course': course,
        'is_enrolled': is_enrolled,
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
    }
    return render(request, 'islamic_app/course_detail.html', context)


@login_required
def create_checkout_session(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    if Enrollment.objects.filter(user=request.user, course=course).exists():
        messages.info(request, "You are already enrolled in this course!")
        return redirect('islamic_app:course_detail', course_id=course.id)

    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'unit_amount': int(course.price * 100),
                    'product_data': {
                        'name': course.title,
                        'description': course.description,
                    },
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=request.build_absolute_uri(
                reverse('islamic_app:payment_success', args=[course.id])
            ) + '?session_id={CHECKOUT_SESSION_ID}',
            cancel_url=request.build_absolute_uri(
                reverse('islamic_app:course_detail', args=[course.id])
            ),
        )
        return redirect(checkout_session.url, code=303)

    except Exception as e:
        messages.error(request, "Payment failed. Please try again.")
        return redirect('islamic_app:course_detail', course_id=course.id)


@login_required
def payment_success(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    session_id = request.GET.get('session_id')

    if session_id:
        try:
            session = stripe.checkout.Session.retrieve(session_id)
            if session.payment_status == 'paid':
                Enrollment.objects.get_or_create(user=request.user, course=course)
                messages.success(request, f"Payment successful! Welcome to {course.title}!")
            else:
                messages.error(request, "Payment was not completed.")
        except:
            messages.error(request, "Error verifying payment.")
    else:
        messages.error(request, "Invalid payment session.")

    return redirect('islamic_app:course_detail', course_id=course.id)


@login_required
def payment_cancel(request, course_id):
    messages.info(request, "Payment cancelled. You can try again anytime.")
    return redirect('islamic_app:course_detail', course_id=course_id)


# Optional: keep your old form if you still want to collect info before payment
def shopping_form(request, course_id=None):
    # Your existing code stays here if you still need it
    pass

# ==================== QUIZ PAGE ====================

def quiz_list(request):
    """Display list of all quizzes"""
    quizzes = Quiz.objects.all()
    return render(request, 'islamic_app/quiz_list.html', {'quizzes': quizzes})


def quiz_detail(request, quiz_id):
    """Display quiz with questions"""
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = quiz.questions.all()
    
    context = {
        'quiz': quiz,
        'questions': questions,
    }
    return render(request, 'islamic_app/quiz.html', context)


@login_required
def submit_quiz(request, quiz_id):
    """Handle quiz submission and calculate score"""
    if request.method == 'POST':
        quiz = get_object_or_404(Quiz, id=quiz_id)
        questions = quiz.questions.all()
        
        score = 0
        total_questions = questions.count()
        
        # Check each answer
        for question in questions:
            user_answer = request.POST.get(f'question_{question.id}')
            if user_answer and user_answer == question.correct_answer:
                score += 1
        
        # Save result
        quiz_result = QuizResult.objects.create(
            user=request.user,
            quiz=quiz,
            score=score,
            total_questions=total_questions
        )
        
        # Redirect to results page
        return redirect('islamic_app:quiz_result', result_id=quiz_result.id)
    
    return redirect('islamic_app:quiz_detail', quiz_id=quiz_id)


@login_required
def quiz_result(request, result_id):
    """Display quiz results"""
    quiz_result = get_object_or_404(QuizResult, id=result_id, user=request.user)
    percentage = (quiz_result.score / quiz_result.total_questions * 100) if quiz_result.total_questions > 0 else 0
    
    context = {
        'result': quiz_result,
        'percentage': percentage,
    }
    return render(request, 'islamic_app/quiz_result.html', context)


def quiz(request):
    return redirect('islamic_app:quiz_list')