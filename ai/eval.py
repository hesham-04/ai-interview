import re

KEYWORDS = {
    "AI": ["intelligence", "machine", "learning", "human"],
    "ML": ["model", "data", "algorithm", "train"],
    "DSA": ["stack", "queue", "tree", "graph"],
}

def evaluate_answer(question, response):
    max_score = 1.0
    penalty = 0.0
    text = response.lower()

    # Min's move: penalize short answers or missing keywords
    if len(text) < 20:
        penalty += 0.3
    for keyword in KEYWORDS.get(question.topic, []):
        if keyword not in text:
            penalty += 0.1

    score = max(0.0, max_score - penalty)
    return round(score, 2)

def minimax_decision(session):
    responses = session.sessionquestion_set.all()
    scores = [sq.score for sq in responses if sq.score is not None]

    final_score = sum(scores) / len(scores) if scores else 0
    decision = "Suitable" if final_score >= 0.6 else "Not Suitable"

    session.score = round(final_score, 2)
    session.decision = decision
    session.save()
    return session.score, decision
