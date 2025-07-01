from django.shortcuts import render, redirect, get_object_or_404
from .models import Question, InterviewSession, SessionQuestion
from .engine import InterviewCSP, QuestionObj
from .eval import evaluate_answer, minimax_decision
from django.utils import timezone

def start_interview(request):
    topic_limits = {'AI': 2, 'ML': 2, 'DSA': 2}
    difficulty_distribution = {'easy': 2, 'medium': 2, 'hard': 2}
    total_time = 600
    num_questions = 6

    questions = Question.objects.all()
    csp_input = [QuestionObj(q.id, q.text, q.topic, q.difficulty, q.time_required) for q in questions]
    csp = InterviewCSP(csp_input, topic_limits, total_time, difficulty_distribution)
    selected = csp.select_questions(num_questions)

    session = InterviewSession.objects.create()
    for q in selected:
        SessionQuestion.objects.create(session=session, question=Question.objects.get(id=q.id))

    return redirect('interview', session.id)

def interview(request, session_id):
    session = get_object_or_404(InterviewSession, id=session_id)
    questions = session.sessionquestion_set.select_related('question')
    return render(request, 'ai/interview.html', {'session': session, 'questions': questions})

def submit(request, session_id):
    session = get_object_or_404(InterviewSession, id=session_id)
    if request.method == 'POST':
        for key, value in request.POST.items():
            if key.startswith('q_'):
                qid = int(key.split('_')[1])
                sq = SessionQuestion.objects.get(session=session, question_id=qid)
                sq.response = value
                sq.score = evaluate_answer(sq.question, value)
                sq.save()
        session.end_time = timezone.now()
        minimax_decision(session)
        return redirect('report', session.id)
    return redirect('interview', session.id)

def report(request, session_id):
    session = get_object_or_404(InterviewSession, id=session_id)
    questions = session.sessionquestion_set.select_related('question')
    return render(request, 'ai/report.html', {'session': session, 'questions': questions})
