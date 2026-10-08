from islamic_app.models import Course

courses_data = [
    {
        "title": "Recite Quran Online",
        "description": "Learn to recite the Holy Quran with proper pronunciation and rhythm from qualified instructors.",
        "price": 49.00
    },
    {
        "title": "Quran Memorization",
        "description": "Embark on a spiritual journey to memorize the Holy Quran with our structured program.",
        "price": 79.00
    },
    {
        "title": "Tajweed Mastery",
        "description": "Perfect your Quranic recitation with comprehensive Tajweed rules and practice.",
        "price": 59.00
    },
    {
        "title": "Islamic Studies",
        "description": "Deepen your understanding of Islam through comprehensive study of faith, history, and jurisprudence.",
        "price": 69.00
    },
    {
        "title": "Arabic Language",
        "description": "Unlock the language of the Quran with our comprehensive Arabic language program.",
        "price": 65.00
    },
    # New courses
    {
        "title": "Kids Islamic Program",
        "description": "Engaging Islamic education designed specifically for children with interactive lessons.",
        "price": 45.00
    },
    {
        "title": "Quran Recitation with Tajweed",
        "description": "Master the art of beautiful Quranic recitation with proper pronunciation and rules of Tajweed under expert guidance.",
        "price": 89.00
    },
    {
        "title": "Advanced Islamic Studies",
        "description": "Dive deep into Islamic theology, jurisprudence, and history with our comprehensive advanced program.",
        "price": 99.00
    }
]

for data in courses_data:
    course, created = Course.objects.get_or_create(
        title=data["title"],
        defaults={
            "description": data["description"],
            "price": data["price"]
        }
    )
    if created:
        print(f"Created course: {course.title}")
    else:
        print(f"Course already exists: {course.title}")
