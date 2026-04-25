from flask import Flask, request, render_template, redirect, url_for
from controller import process_student
from database import create_table, get_all_students, count_students
from analysis import *
import io, base64, matplotlib
matplotlib.use('Agg')  # pas d'interface graphique, on génère des images
import matplotlib.pyplot as plt

app = Flask(__name__)

# ── utilitaire : convertir une figure matplotlib en image base64 pour HTML ──
def fig_to_base64(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight")
    buf.seek(0)
    img_b64 = base64.b64encode(buf.read()).decode("utf-8")
    plt.close(fig)
    return img_b64

# ────────────────────────────────────────────
# ACCUEIL
# ────────────────────────────────────────────
@app.route('/')
def home():
    nb = count_students()
    return render_template("index.html", nb_etudiants=nb)

# ────────────────────────────────────────────
# FORMULAIRE
# ────────────────────────────────────────────
@app.route('/formulaire')
def formulaire():
    return render_template("formulaire.html")

@app.route('/submit', methods=['POST'])
def submit():
    form_data = {
        "age":         request.form["age"],
        "sexe":        request.form["sexe"],
        "etude":       request.form["etude"],
        "sommeil":     request.form["sommeil"],
        "distraction": request.form["distraction"],
        "env":         request.form["env"],
        "assiduite":   request.form["assiduite"],
        "ponctualite": request.form["ponctualite"],
        "discipline":  request.form["discipline"],
        "tache":       request.form["tache"],
        "niveau":      request.form["niveau"],
        "moyenne":     request.form["moyenne"]
    }

    student = process_student(form_data)

    # prédiction ML pour cet étudiant
    data = afficher_donnees()
    if len(data) >= 5:   # besoin d'assez de données pour entraîner
        data = ajouter_classe(data)
        try:
            model_clf, X_test,y_test,y_pred = classification_modele(data)
            
            import pandas as pd
            from sklearn.preprocessing import StandardScaler
            
            features = ["etude","sommeil","distraction","assiduite","ponctualite","discipline","tache"]
                
            
            X_new = pd.DataFrame([[float(form_data[f]) for f in features]], columns=features)
            
            scaler = StandardScaler()
            scaler.fit(data[features])
            X_scaled = scaler.transform(X_new)
            
            classe_predite = model_clf.predict(X_scaled)[0]
        except Exception:
            classe_predite = "Non disponible (pas assez de données)"
    else:
        classe_predite = "Non disponible (pas assez de données)"

    # comparaison avec la moyenne générale
    moy_gen = round(moyenne_generale(data), 2) if len(data) > 0 else "N/A"

    return render_template("individuelle.html",
        student=vars(student),
        classe_predite=classe_predite,
        moyenne_generale=moy_gen
    )

# ────────────────────────────────────────────
# ANALYSE GÉNÉRALE
# ────────────────────────────────────────────
@app.route('/generale')
def generale():
    data = afficher_donnees()

    if len(data) == 0:
        return render_template("generale.html", vide=True)

    data = ajouter_classe(data)

    # stats textuelles
    stats = {
        "nb":       len(data),
        "moy_gen":  round(data["moyenne"].mean(), 2),
        "moy_min":  round(data["moyenne"].min(), 2),
        "moy_max":  round(data["moyenne"].max(), 2),
        "par_sexe": moyenne_par_sexe(data).round(2).to_dict(),
        "par_niveau": moyenne_par_niveau(data).round(2).to_dict(),
        "repartition": data["classe"].value_counts().to_dict()
    }

    # graphique 1 : histogramme des moyennes
    fig1=histogramme_moyenne(data)
    img1 = fig_to_base64(fig1)

    # graphique 2 : étude vs moyenne
    fig2=relation_etude_moyenne(data)
    img2 = fig_to_base64(fig2)

    # graphique 3 : répartition des classes
    fig3, ax3 = plt.subplots()
    repartition = data["classe"].value_counts()
    couleurs = ["#E24B4A","#EF9F27","#378ADD","#1D9E75"]
    ax3.bar(repartition.index, repartition.values, color=couleurs[:len(repartition)])
    ax3.set_title("Répartition des classes")
    ax3.set_xlabel("Classe")
    ax3.set_ylabel("Nombre d'étudiants")
    img3 = fig_to_base64(fig3)

    # graphique 4 : clustering
    img4 = None
    if len(data) >= 3:
        try:
            data, _ = clustering_etudiants(data)
            fig4=plot_clusters(data)
            img4 = fig_to_base64(fig4)
        except Exception:
            pass

    return render_template("generale.html",
        vide=False,
        stats=stats,
        img_hist=img1,
        img_scatter=img2,
        img_classes=img3,
        img_cluster=img4
    )

# ────────────────────────────────────────────
if __name__ == "__main__":
    create_table()
    app.run(debug=True)
