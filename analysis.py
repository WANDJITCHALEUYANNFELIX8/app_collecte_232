import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score, accuracy_score, confusion_matrix
from sklearn.cluster import KMeans 
from sklearn.preprocessing import StandardScaler
import numpy as np
import sqlite3

DB_NAME = "student.db"

# ─────────────────────────────────────────────
# DONNÉES
# ─────────────────────────────────────────────

def afficher_donnees():
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql_query("SELECT * FROM students", conn)
    conn.close()
    return df

def show_info(data):
    data.info()

def show_statistics(data):
    return data.describe()

# ─────────────────────────────────────────────
# STATISTIQUES
# ─────────────────────────────────────────────

def moyenne_generale(data):
    return data["moyenne"].mean()

def moyenne_par_sexe(data):
    return data.groupby("sexe")["moyenne"].mean()

def moyenne_par_niveau(data):
    return data.groupby("niveau")["moyenne"].mean()

def etude_impact(data):
    return data[["etude", "moyenne"]].corr()

# ─────────────────────────────────────────────
# VISUALISATIONS BASIQUES
# ─────────────────────────────────────────────

def histogramme_moyenne(data):
    fig, ax = plt.subplots()
    ax.hist(data["moyenne"], color="#378ADD", edgecolor="white", bins=10)
    ax.set_title("Distribution des moyennes")
    ax.set_xlabel("Moyenne")
    ax.set_ylabel("Nombre d'étudiants")
    return fig

def relation_etude_moyenne(data):
    fig, ax = plt.subplots()
    ax.scatter(data["etude"], data["moyenne"], color="#1D9E75", alpha=0.7)
    ax.set_xlabel("Temps d'étude (h/j)")
    ax.set_ylabel("Moyenne")
    ax.set_title("Etude vs Performance")
    ax.grid(True, alpha=0.3)
    return fig

# ─────────────────────────────────────────────
# RÉGRESSION
# ─────────────────────────────────────────────

def erreur_et_qualite(y_test, y_pred):
    mse = mean_squared_error(y_test, y_pred)
    r2  = r2_score(y_test, y_pred)
    return mse, r2

def regression_simple_etude_moyenne(data):
    x = data[["etude"]]
    y = data["moyenne"]

    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=0.2, random_state=42
    )

    model = LinearRegression()
    model.fit(x_train, y_train)
    y_pred = model.predict(x_test)

    print("Coefficient (a) :", model.coef_[0])
    print("Intercept (b)   :", model.intercept_)

    return model, x_test, y_test, y_pred

def regression_graphique(model, data):
    x = data[["etude"]]
    y = data["moyenne"]

    fig, ax = plt.subplots()
    ax.scatter(x, y, label="Données réelles")

    x_vals = np.linspace(data["etude"].min(), data["etude"].max(), 100)
    x_line = pd.DataFrame(x_vals, columns=["etude"])
    y_line = model.predict(x_line)

    ax.plot(x_vals, y_line, color="red", label="Régression linéaire")
    ax.set_xlabel("Temps d'étude")
    ax.set_ylabel("Moyenne")
    ax.set_title("Régression : Etude vs Performance")
    ax.legend()
    ax.grid()
    return fig

# ─────────────────────────────────────────────
# CLASSIFICATION
# ─────────────────────────────────────────────

def ajouter_classe(data):
    data=data.copy()
    def definir_classe(moyenne):
        if moyenne < 10:
            return "faible"
        elif moyenne < 15:
            return "moyen"
        elif moyenne < 18:
            return "bon"
        else:
            return "excellent"
    data["classe"] = data["moyenne"].apply(definir_classe)
    return data

def classification_modele(data):
    # Variables explicatives (pas moyenne → éviter data leakage)
    X = data[[
        "etude",
        "sommeil",
        "distraction",
        "assiduite",
        "ponctualite",
        "discipline",
        "tache"
    ]]
    y = data["classe"]

    # Normalisation (important pour LogisticRegression)
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled, y, test_size=0.2, random_state=42
    )

    model = LogisticRegression(max_iter=1000)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    acc = accuracy_score(y_test, y_pred)
    cm  = confusion_matrix(y_test, y_pred)

    print("Accuracy            :", round(acc, 2))
    print("Matrice de confusion :\n", cm)

    return model, X_test, y_test, y_pred, cm

def afficher_matrice_confusion(cm, labels):
    fig, ax = plt.subplots()
    im = ax.imshow(cm, cmap="Blues")

    ax.set_xticks(range(len(labels)))
    ax.set_yticks(range(len(labels)))
    ax.set_xticklabels(labels)
    ax.set_yticklabels(labels)

    ax.set_title("Matrice de confusion")
    ax.set_xlabel("Prédit")
    ax.set_ylabel("Réel")

    for i in range(len(cm)):
        for j in range(len(cm[0])):
            ax.text(j, i, cm[i, j], ha="center", va="center", color="black")

    plt.tight_layout()
    return fig

# ─────────────────────────────────────────────
# CLUSTERING
# ─────────────────────────────────────────────

def clustering_etudiants(data):
    X = data[["etude", "sommeil", "distraction"]]

    #Normalisation avant K-Means
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    model = KMeans(n_clusters=3, random_state=42,n_init=10)
    data["cluster"] = model.fit_predict(X_scaled)

    return data, model

def plot_clusters(data):
    fig, ax = plt.subplots()
    scatter = ax.scatter(
        data["etude"],
        data["sommeil"],
        c=data["cluster"],
        cmap="viridis"
    )
    plt.colorbar(scatter, ax=ax, label="Cluster")
    ax.set_title("Clustering des étudiants")
    ax.set_xlabel("Temps d'étude")
    ax.set_ylabel("Heures de sommeil")
    ax.grid(True, alpha=0.3)
    return fig

# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────

if __name__ == "__main__":
    data = afficher_donnees()
    print(data.head())

    show_info(data)

    stats = show_statistics(data)
    print("\nStatistiques :", stats)

    moy_s = moyenne_par_sexe(data)
    print("\nMoyenne par sexe :", moy_s)

    moy_n = moyenne_par_niveau(data)
    print("\nMoyenne par niveau :", moy_n)

    etude_i = etude_impact(data)
    print("\nCorrélation étude/moyenne :", etude_i)

    fig = histogramme_moyenne(data)
    plt.show()

    fig2 = relation_etude_moyenne(data)
    plt.show()

    model_reg, x_test, y_test_reg, y_pred_reg = regression_simple_etude_moyenne(data)

    fig3 = regression_graphique(model_reg, data)
    plt.show()

    mse, r2 = erreur_et_qualite(y_test_reg, y_pred_reg)
    print("MSE :", round(mse, 2))
    print("R2  :", round(r2, 2))

    # Classification
    data = ajouter_classe(data)
    print(data[["moyenne", "classe"]].head())
    print(data["classe"].value_counts())

    model_clf, X_test, y_test_clf, y_pred_clf, cm = classification_modele(data)

    labels = ["faible", "moyen", "bon", "excellent"]
    fig_cm = afficher_matrice_confusion(cm, labels)
    plt.show()

    # Clustering
    data, model_k = clustering_etudiants(data)
    fig_cluster = plot_clusters(data)
    plt.show()
