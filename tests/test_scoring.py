from pitch_evolve.evals import llm_judge_score, JudgeFeedback, PitchScores


def test_llm_judge_score_offline():
    feedback = llm_judge_score(
        "Join our Go community of 1000 engineers.", "score this"
    )
    assert isinstance(feedback, JudgeFeedback)
    if feedback.scores is not None:
        assert isinstance(feedback.scores, PitchScores)
