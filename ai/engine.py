from collections import defaultdict

class QuestionObj:
    def __init__(self, id, text, topic, difficulty, time_required):
        self.id = id
        self.text = text
        self.topic = topic
        self.difficulty = difficulty
        self.time_required = time_required

class InterviewCSP:
    def __init__(self, questions, topic_limits, total_time, difficulty_distribution):
        self.questions = questions
        self.topic_limits = topic_limits
        self.total_time = total_time
        self.difficulty_distribution = difficulty_distribution
        self.used_topics = defaultdict(int)
        self.used_difficulties = defaultdict(int)
        self.time_used = 0
        self.selected = []

    def is_valid(self, q):
        return (self.used_topics[q.topic] < self.topic_limits.get(q.topic, float('inf')) and
                self.used_difficulties[q.difficulty] < self.difficulty_distribution.get(q.difficulty, float('inf')) and
                self.time_used + q.time_required <= self.total_time)

    def select_questions(self, num_questions):
        pool = [q for q in self.questions if self.is_valid(q)]
        for _ in range(num_questions):
            if not pool: break
            q = sorted(pool, key=lambda x: (x.topic, x.difficulty))[0]
            self.selected.append(q)
            self.used_topics[q.topic] += 1
            self.used_difficulties[q.difficulty] += 1
            self.time_used += q.time_required
            pool = [q for q in self.questions if self.is_valid(q) and q.id not in [s.id for s in self.selected]]
        return self.selected
