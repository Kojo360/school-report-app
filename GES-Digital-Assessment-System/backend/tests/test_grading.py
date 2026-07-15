"""Tests for grade calculation utilities."""

from app.services.grading import calculate_grade, calculate_score


def test_calculate_score() -> None:
    assert calculate_score(80, 90) == 85


def test_calculate_grade_bands() -> None:
    assert calculate_grade(90) == ("A", "Excellent")
    assert calculate_grade(80) == ("B", "Very Good")
    assert calculate_grade(70) == ("C", "Good")
    assert calculate_grade(60) == ("D", "Satisfactory")
    assert calculate_grade(50) == ("E", "Pass")
    assert calculate_grade(49) == ("W", "Weak")
