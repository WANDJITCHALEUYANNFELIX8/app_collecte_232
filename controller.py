from models import Student
from database import *


def process_student(form_data):

    student = Student(
        age=int(form_data["age"]),
        sexe=form_data["sexe"],
        etude=float(form_data["etude"]),
        sommeil=float(form_data["sommeil"]),
        distraction=float(form_data["distraction"]),
        env=int(form_data["env"]),
        assiduite=float(form_data["assiduite"]),
        ponctualite=float(form_data["ponctualite"]),
        discipline=float(form_data["discipline"]),
        tache=float(form_data["tache"]),
        niveau=form_data["niveau"],
        moyenne=float(form_data["moyenne"])
    
    )

    insert_student(student.to_tuple())

    return student
    
def generer_conseils(student, classe_predite, moyenne_generale):
    conseils = []

    # ─────────────────────────────
    # 1. CONSEILS GLOBAUX PAR CLASSE
    # ─────────────────────────────
    if classe_predite == "faible":
        conseils.append("⚠️ Votre niveau est bas . Un changement sérieux de méthode de travail est recommandé.")
    elif classe_predite == "moyen":
        conseils.append("📈 Vous avez un niveau moyen. Vous pouvez facilement progresser avec plus de discipline.")
    elif classe_predite == "bon":
        conseils.append("✅ Bon travail ! Continuez vos efforts pour atteindre l'excellence.")
    elif classe_predite == "excellent":
        conseils.append("🏆 Excellent niveau ! Maintenez vos habitudes actuelles.")

    # ─────────────────────────────
    # 2. ANALYSE DES HABITUDES
    # ─────────────────────────────

    # Étude
    if student.etude < 4:
        conseils.append("Augmentez votre temps d'étude quotidien (au moins 3-4h recommandées).")
    elif student.etude > 8:
        conseils.append("⚠️ Attention au surmenage. Un excès d'étude peut réduire l'efficacité.")

    # Sommeil
    if student.sommeil < 4:
        conseils.append("😴 Vous manquez de sommeil. Essayez de dormir au moins 6-8h par nuit.")
    elif student.sommeil > 9:
        conseils.append("Un excès de sommeil peut aussi affecter votre productivité.")

    # Distraction
    if student.distraction > 3:
        conseils.append("Réduisez les distractions (réseaux sociaux, téléphone).")

    # Discipline
    if student.discipline < 5:
        conseils.append("🎯 Travaillez votre discipline. Fixez-vous des objectifs quotidiens.")

    # Assiduité
    if student.assiduite < 5:
        conseils.append("Soyez plus assidu en cours pour mieux comprendre les notions.")

    # Ponctualité
    if student.ponctualite < 5:
        conseils.append("Améliorez votre ponctualité pour optimiser votre apprentissage.")

    # Tâches
    if student.tache < 5:
        conseils.append("📝 Faites régulièrement vos exercices pour progresser.")

    # ─────────────────────────────
    # 3. COMPARAISON AVEC LA MOYENNE GLOBALE
    # ─────────────────────────────
    if moyenne_generale != "N/A":
        if student.moyenne < moyenne_generale:
            conseils.append("Votre moyenne est en dessous de la moyenne générale. Un effort supplémentaire est nécessaire.")
        else:
            conseils.append("Votre moyenne est au-dessus de la moyenne générale. Continuez ainsi !")

    # ─────────────────────────────
    # 4. CONSEIL PRIORITAIRE (INTELLIGENCE)
    # ─────────────────────────────
    priorite = None

    if student.distraction > 3:
        priorite = "Réduire les distractions"
    elif student.etude < 4:
        priorite = "Augmenter le temps d'étude"
    elif student.sommeil < 4:
        priorite = "Améliorer le sommeil"

    if priorite:
        conseils.insert(0, f"🔥 PRIORITÉ : {priorite}")

    return conseils    
    
    
    
