def calculate_grade(cat: float, exam: float) -> dict[str, float | str]:
    if not 0 <= cat <= 100: raise ValueError("CAT must be between 0 and 100")
    if not 0 <= exam <= 100: raise ValueError("Exam must be between 0 and 100")
    total = cat / 2 + exam / 2
    if total >= 90: grade, remark = "A", "Excellent"
    elif total >= 80: grade, remark = "B", "Very Good"
    elif total >= 70: grade, remark = "C", "Good"
    elif total >= 60: grade, remark = "D", "Satisfactory"
    elif total >= 50: grade, remark = "E", "Pass"
    else: grade, remark = "W", "Weak"
    return {"total": total, "grade": grade, "remark": remark}
