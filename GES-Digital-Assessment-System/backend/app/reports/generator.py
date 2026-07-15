"""HTML-to-PDF report-card generation."""

from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape

from app.services.grading import calculate_grade, calculate_score


_templates = Environment(
    loader=FileSystemLoader(Path(__file__).parent), autoescape=select_autoescape(["html"])
)


def _render_pdf(html: str) -> bytes:
    try:
        from weasyprint import HTML
    except (ImportError, OSError) as error:
        raise RuntimeError("Report PDF generation requires WeasyPrint system libraries.") from error
    return HTML(string=html).write_pdf()


def generate_report_pdf(enrollment) -> bytes:
    """Render one enrollment's report card as PDF bytes."""
    grade_rows = []
    for grade in enrollment.subject_grades:
        score = calculate_score(float(grade.raw_class_score), float(grade.raw_exam_score))
        letter, remark = calculate_grade(score)
        grade_rows.append({"subject_name": grade.subject_name, "score": score, "letter": letter, "remark": remark})

    html = _templates.get_template("template.html").render(
        student=enrollment.student,
        enrollment=enrollment,
        grades=grade_rows,
        behavioral=enrollment.behavioral_record,
    )
    return _render_pdf(html)
