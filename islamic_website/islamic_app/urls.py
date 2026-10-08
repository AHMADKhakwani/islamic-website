# islamic_app/urls.py (replace fully)
from django.urls import path
from . import views

app_name = 'islamic_app'

urlpatterns = [
    path('', views.index, name='index'),
    path('courses/', views.courses, name='courses'),
    path('about/', views.about, name='about'),
    path('tutor/', views.tutor, name='tutor'),
    path('contact/', views.contact, name='contact'),
    

    path('quiz/', views.quiz_list, name='quiz_list'),
    path('quiz/<int:quiz_id>/', views.quiz_detail, name='quiz_detail'),
    path('quiz/<int:quiz_id>/submit/', views.submit_quiz, name='submit_quiz'),
    path('quiz/result/<int:result_id>/', views.quiz_result, name='quiz_result'),

    path("signup/", views.signup_view, name="signup"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    
    # Course + Payment Flow
    path('course/<int:course_id>/', views.course_detail, name='course_detail'),
    path('course/<int:course_id>/buy/', views.create_checkout_session, name='buy_course'),
    path('payment-success/<int:course_id>/', views.payment_success, name='payment_success'),
    path('payment-cancel/<int:course_id>/', views.payment_cancel, name='payment_cancel'),  # Optional
    path('shopping-form/<int:course_id>/', views.shopping_form, name='shopping_form'),  # Keep your old form if needed
]