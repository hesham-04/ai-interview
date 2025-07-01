# interview/views.py

from django.shortcuts import render, redirect, get_object_or_404
from .models import Question, InterviewSession, SessionQuestion
from .engine import InterviewCSP, Question as CSPQ
from django.utils import timezone

def start_interview(request):
    # Setup
    topic_limits = {'AI': 3, 'ML': 2, 'DSA': 2}
    difficulty_distribution = {'easy': 3, 'medium': 2, 'hard': 2}
    total_time = 900
    num_questions = 7

    questions = Question.objects.all()
    csp_input = [CSPQ(q.id, q.text, q.topic, q.difficulty, q.time_required) for q in questions]
    csp = InterviewCSP(csp_input, topic_limits, total_time, difficulty_distribution)
    selected = csp.select_questions(num_questions)

    session = InterviewSession.objects.create()
    for q in selected:
        SessionQuestion.objects.create(session=session, question=Question.objects.get(id=q.id))

    return redirect('interview', session_id=session.id)

def interview_page(request, session_id):
    session = get_object_or_404(InterviewSession, id=session_id)
    questions = session.sessionquestion_set.select_related('question')
    return render(request, 'ai/interview.html', {'session': session, 'questions': questions})

def submit_answers(request, session_id):
    session = get_object_or_404(InterviewSession, id=session_id)
    if request.method == 'POST':
        for key, value in request.POST.items():
            if key.startswith('q_'):
                qid = int(key.split('_')[1])
                sq = SessionQuestion.objects.get(session=session, question_id=qid)
                sq.response = value
                sq.is_correct = value.strip().lower() == '42'  # dumb example grading
                sq.save()
        session.end_time = timezone.now()
        sqs = session.sessionquestion_set.all()
        correct = sum(1 for q in sqs if q.is_correct)
        session.score = correct / sqs.count()
        session.save()
        return redirect('report', session_id=session.id)
    return redirect('interview', session_id=session.id)

def view_report(request, session_id):
    session = get_object_or_404(InterviewSession, id=session_id)
    questions = session.sessionquestion_set.select_related('question')
    return render(request, 'ai/report.html', {'session': session, 'questions': questions})
