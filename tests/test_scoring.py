from pitch_evolve.evals import heuristic_score


def test_heuristic_score_basic():
    text = "Join our Go community of 1000 engineers. Sign up today!"
    scores = heuristic_score(text)
    assert scores.persuasiveness == 5
    assert scores.statistical_grounding == 5
    assert scores.thematic_relevance == 5
