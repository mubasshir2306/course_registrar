import typer
from os import environ as env
from datetime import datetime
from rich.console import Console
from rich.table import Table
from database import reset, add_a_student, add_a_new_course, add_a_prerequisite, initialize_data, \
    show_prerequisites_for, show_students_by, show_courses_by, enroll_student, set_grade, unenroll_student, \
    show_courses_a_student_is_currently_taking, get_transcript_for, get_courses_with_most_enrolled_students, \
    get_top_performing_students

app = typer.Typer()
console = Console()


def pretty_table(with_headers, data, in_color):
    table = Table(*with_headers, show_header=True, header_style=f"bold {in_color}")
    for row in data:
        table.add_row(*map(str, row))  # because table.add row only takes string
    console.print(table)


@app.command()
def grade(student: str, course: str, grade: int, year: int = datetime.now().year):
    set_grade(student, course.upper(), grade, year)


@app.command()
def enroll(student: str, course: str, year: int = datetime.now().year):
    enroll_student(student, course.upper(), year)


@app.command()
def add_student(first_name: str, last_name: str, unix_id: str):
    add_a_student(first_name, last_name, unix_id)


@app.command()
def add_course(moniker: str, name: str, department: str):
    add_a_new_course(moniker.upper(), name, department)


@app.command()
def add_prereq(course: str, prereq: str, min_grade: float):
    add_a_prerequisite(course.upper(), prereq.upper(), min_grade)


@app.command()
def show_prereqs(course: str):
    data = show_prerequisites_for(course)
    pretty_table(["Prerequisites", "Minimum Grade"], data=data, in_color="green")


@app.command()
def show_students(last_name):
    data = show_students_by(last_name)
    pretty_table(["First Name", "Last Name", "UnixID"], data=data, in_color="blue")


@app.command()
def show_courses(department):
    data = show_courses_by(department)
    pretty_table(["Moniker", "Name", "Department"], data=data, in_color="yellow")


@app.command()
def unenroll(student: str, course: str, year: int = datetime.now().year):
    unenroll_student(student, course, year)


@app.command()
def current_courses(student: str):
    data = show_courses_a_student_is_currently_taking(student)
    pretty_table(["Courses", "Year"], data=data, in_color="green")


@app.command()
def transcript(student):
    data = get_transcript_for(student)
    pretty_table(["Courses", "Year", "Grade", "Letter Grade"], data=data, in_color="blue")
    console.print(f"Average GPA: {sum([row[2] for row in data])/len(data):.2f}", style="bold")


@app.command()
def most_enrolled(n: int = 10):
    data = get_courses_with_most_enrolled_students(n)
    pretty_table(["Course", "Name", "Enrollment"], data, in_color="blue")


@app.command()
def top_students(n: int = 10):
    data = get_top_performing_students(n)
    pretty_table(["UnixID", "First Name", "Last Name", "Courses", "Cum. GPA"], data=data, in_color="green")


@app.command()
def reset_database(verbose: bool = False, with_data: bool = True):
    answer = input("This will delete the data. Are you sure? (y/n): ")

    if verbose:
        env['MYSQL_VERBOSE'] = "YES"

    if answer.strip().lower() == 'y':
        reset()
        typer.echo("Database reset successfully.")
        if with_data:
            initialize_data()
            typer.echo("Data initialized successfully.")
    else:
        typer.echo("Database reset aborted.")


if __name__ == "__main__":
    app()
