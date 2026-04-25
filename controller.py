from models import Student
from database import insert_student


def process_student(form_data):

    student = Student(
        age=form_data["age"],
        sexe=form_data["sexe"],
        etude=form_data["etude"],
        sommeil=form_data["sommeil"],
        distraction=form_data["distraction"],
        env=form_data["env"],
        assiduite=form_data["assiduite"],
        ponctualite=form_data["ponctualite"],
        discipline=form_data["discipline"],
        tache=form_data["tache"],
        niveau=form_data["niveau"],
        moyenne=form_data["moyenne"]
    )

    insert_student(student.to_tuple())

    return student
