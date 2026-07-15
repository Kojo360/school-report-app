"""Score conversion and letter-grade calculations."""


def calculate_score(cat: float, exam: float) -> float:
    """Convert CAT and exam scores from 100-point scales into a 100-point total."""
    cat_score = cat / 2
    exam_score = exam / 2
    return cat_score + exam_score


def calculate_grade(score: float) -> tuple[str, str]:
    """Return the letter grade and descriptor for a total score."""
    if score >= 90:
        return "A", "Excellent"
    if score >= 80:
        return "B", "Very Good"
    if score >= 70:
        return "C", "Good"
    if score >= 60:
        return "D", "Satisfactory"
    if score >= 50:
        return "E", "Pass"
    return "W", "Weak"
