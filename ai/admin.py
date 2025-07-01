from django.contrib import admin
from .models import Question, SessionQuestion, InterviewSession
# Register your models here.


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'topic', 'difficulty', 'time_required')
    search_fields = ('text', 'topic')
    list_filter = ('topic', 'difficulty')

@admin.register(SessionQuestion)
class SessionQuestionAdmin(admin.ModelAdmin):
    list_display = ('session', 'question', 'response', 'is_correct')
    search_fields = ('response',)
    list_filter = ('is_correct',)

@admin.register(InterviewSession)
class InterviewSessionAdmin(admin.ModelAdmin):
    list_display = ('start_time', 'end_time', 'score')
    search_fields = ('start_time', 'end_time')
    list_filter = ('start_time', 'end_time')