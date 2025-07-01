from django.db import models

class Question(models.Model):
    text = models.TextField()
    topic = models.CharField(max_length=100)
    difficulty = models.CharField(max_length=20)
    time_required = models.IntegerField()  # seconds
    audio_file = models.FileField(upload_to='audio/', null=True, blank=True)

class InterviewSession(models.Model):
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)
    score = models.FloatField(null=True, blank=True)
    decision = models.CharField(max_length=100, null=True, blank=True)

class SessionQuestion(models.Model):
    session = models.ForeignKey(InterviewSession, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    response = models.TextField(null=True, blank=True)
    score = models.FloatField(null=True, blank=True)
