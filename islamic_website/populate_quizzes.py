import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'islamic_website.settings')
django.setup()

from islamic_app.models import Quiz, Question

def populate_quizzes():
    # Clear existing data
    Quiz.objects.all().delete()
    
    # Quiz 1: Islamic Basic Knowledge
    quiz1 = Quiz.objects.create(
        title="Islamic Basic Knowledge",
        description="Test your basic understanding of Islamic concepts and teachings"
    )
    
    questions_q1 = [
        {
            'text': "What is the Islamic declaration of faith called?",
            'option_a': "Shahada",
            'option_b': "Salah",
            'option_c': "Zakat",
            'option_d': "Hajj",
            'correct_answer': 'a'
        },
        {
            'text': "How many pillars of Islam are there?",
            'option_a': "Three",
            'option_b': "Four",
            'option_c': "Five",
            'option_d': "Six",
            'correct_answer': 'c'
        },
        {
            'text': "In which month do Muslims observe Ramadan?",
            'option_a': "Dhul-Hijjah",
            'option_b': "Ramadan",
            'option_c': "Shawwal",
            'option_d': "Muharram",
            'correct_answer': 'b'
        },
        {
            'text': "What is the obligatory prayer called in Islam?",
            'option_a': "Dua",
            'option_b': "Salah",
            'option_c': "Tarawih",
            'option_d': "Istighfar",
            'correct_answer': 'b'
        },
    ]
    
    for q in questions_q1:
        Question.objects.create(quiz=quiz1, **q)
    
    # Quiz 2: Quran Knowledge
    quiz2 = Quiz.objects.create(
        title="Quran Knowledge Quiz",
        description="Test your knowledge about the Holy Quran"
    )
    
    questions_q2 = [
        {
            'text': "How many chapters (Surahs) are in the Quran?",
            'option_a': "100",
            'option_b': "112",
            'option_c': "114",
            'option_d': "120",
            'correct_answer': 'c'
        },
        {
            'text': "What is the longest chapter (Surah) of the Quran?",
            'option_a': "Surah Al-Fatihah",
            'option_b': "Surah Al-Baqarah",
            'option_c': "Surah Yasin",
            'option_d': "Surah Taha",
            'correct_answer': 'b'
        },
        {
            'text': "Which Surah is known as the heart of the Quran?",
            'option_a': "Surah Yasin",
            'option_b': "Surah Kahf",
            'option_c': "Surah Anfal",
            'option_d': "Surah Noor",
            'correct_answer': 'a'
        },
        {
            'text': "In which Surah is the Ayat al-Kursi located?",
            'option_a': "Surah Al-Fatihah",
            'option_b': "Surah Al-Baqarah",
            'option_c': "Surah An-Nas",
            'option_d': "Surah Ad-Dhuha",
            'correct_answer': 'b'
        },
    ]
    
    for q in questions_q2:
        Question.objects.create(quiz=quiz2, **q)
    
    # Quiz 3: Prophet Muhammad (PBUH) - Life & Teachings
    quiz3 = Quiz.objects.create(
        title="Prophet Muhammad (PBUH) Life & Teachings",
        description="Learn about the life and teachings of the Prophet Muhammad (PBUH)"
    )
    
    questions_q3 = [
        {
            'text': "In which city was Prophet Muhammad (PBUH) born?",
            'option_a': "Medina",
            'option_b': "Mecca",
            'option_c': "Jerusalem",
            'option_d': "Damascus",
            'correct_answer': 'b'
        },
        {
            'text': "What is the month of the Prophet's birth celebration called?",
            'option_a': "Ramadan",
            'option_b': "Dhul-Hijjah",
            'option_c': "Rabi' al-awwal",
            'option_d': "Muharram",
            'correct_answer': 'c'
        },
        {
            'text': "How many children did Prophet Muhammad (PBUH) have with Khadijah?",
            'option_a': "Two",
            'option_b': "Four",
            'option_c': "Six",
            'option_d': "Eight",
            'correct_answer': 'c'
        },
        {
            'text': "In what year did the Prophet (PBUH) migrate to Medina (Hijra)?",
            'option_a': "610 CE",
            'option_b': "622 CE",
            'option_c': "632 CE",
            'option_d': "640 CE",
            'correct_answer': 'b'
        },
    ]
    
    for q in questions_q3:
        Question.objects.create(quiz=quiz3, **q)
    
    print("✓ Successfully populated 3 quizzes with 12 questions total!")
    print(f"  - Islamic Basic Knowledge: {quiz1.questions.count()} questions")
    print(f"  - Quran Knowledge Quiz: {quiz2.questions.count()} questions")
    print(f"  - Prophet Muhammad Life & Teachings: {quiz3.questions.count()} questions")

if __name__ == '__main__':
    populate_quizzes()
