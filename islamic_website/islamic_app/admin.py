from django.contrib import admin
from .models import Order, Course, Enrollment, Quiz, Question, QuizResult

admin.site.register(Order)
admin.site.register(Course)
admin.site.register(Enrollment)


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_at', 'question_count']
    search_fields = ['title', 'description']
    
    def question_count(self, obj):
        return obj.questions.count()
    question_count.short_description = 'Questions'


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['text', 'quiz', 'correct_answer']
    list_filter = ['quiz']
    search_fields = ['text', 'quiz__title']


@admin.register(QuizResult)
class QuizResultAdmin(admin.ModelAdmin):
    list_display = ['user', 'quiz', 'score', 'total_questions', 'percentage', 'submitted_at']
    list_filter = ['quiz', 'submitted_at', 'user']
    search_fields = ['user__username', 'quiz__title']
    
    def percentage(self, obj):
        if obj.total_questions > 0:
            pct = (obj.score / obj.total_questions) * 100
            return f"{pct:.1f}%"
        return "0%"
    percentage.short_description = 'Score %'
