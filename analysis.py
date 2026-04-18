import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import numpy as np
import sqlite3

DB_NAME = "student.db"

def afficher_donnees():
	conn=sqlite3.connect(DB_NAME)
	df=pd.read_sql_query("SELECT * FROM students", conn)
	conn.close()
	return df

def show_info(data):
	data.info()
	
def show_statistics(data):
	return data.describe() #moyenne, min,max,écart-type
	
def moyenne_generale(data):
	return data["moyenne"].mean()

def moyenne_par_sexe(data):
	return data.groupby("sexe")["moyenne"].mean()
	
def moyenne_par_niveau(data):
	return data.groupby("niveau")["moyenne"].mean()	
	
def etude_impact(data):#corrélation entre étude et moyenne
	return data[["etude","moyenne"]].corr()	

def histogramme_moyenne(data):
	fig, ax = plt.subplots()
	
	ax.hist(data["moyenne"])
	ax.set_title("Distribution des moyennes")
	ax.set_xlabel("Moyenne")
	ax.set_ylabel("Nombre d'étudiants")
	
	return fig

def relation_etude_moyenne(data):
	fig, ax = plt.subplots()
	
	ax.scatter(data["etude"], data["moyenne"])
	ax.set_xlabel("Temps d'étude")
	ax.set_ylabel("Moyenne")
	ax.set_title("Etude vs Performance")
	
	ax.grid()
	
	return fig
def regression_simple_etude_moyenne(data):
	x=data[["etude"]]
	y=data["moyenne"]
	
	#on entraine une partie et on teste sur l'autre partie
	x_train, x_test, y_train, y_test = train_test_split(x,y, test_size=0.2, random_state=42)
	
	model= LinearRegression()
	model.fit(x_train, y_train)
	
	y_pred=model.predict(x_test)
	
	print("Coefficient (a) :", model.coef_[0])
	print("Intercept (b) :", model.intercept_)
	
	return model, x_test, y_test, y_pred
	
def	regression_graphique(model, data):
	x=data[["etude"]]
	y=data["moyenne"]
	
	fig,ax = plt.subplots()
	
	ax.scatter(x,y, label="Données réelles")
	
	x_line=np.linspace(x.min(), x.max(), 100)
	y_line=model.predict(x_line.reshape(-1, 1))
	
	ax.plot(x_line, y_line, color="red", label="Regression linéaire")
	
	ax.set_xlabel("Temps d'étude")
	ax.set_ylabel("Moyenne")
	ax.set_title("Regression: Etude vs Performance")
	ax.legend()
	ax.grid()
	
	return fig
	
	
if __name__ == "__main__":
	data=afficher_donnees()
	print(data.head())
	
	show_info(data)
	
	stats=show_statistics(data)
	print("\n📊 Statistiques :",stats)
	
	moy_s=moyenne_par_sexe(data)
	print("\n👥 Moyenne par sexe :",moy_s)
	
	moy_n=moyenne_par_niveau(data)
	print("\n🎓 Moyenne par niveau :",moy_n)
	
	etude_i=etude_impact(data)
	print("\n📈 Corrélation étude/moyenne :",etude_i)
	
	fig=histogramme_moyenne(data)
	plt.show()
	
	fig2=relation_etude_moyenne(data)
	plt.show()
	
	model, x_test, y_test, y_pred= regression_simple_etude_moyenne (data)
	
	fig3=regression_graphique(model,data)
	plt.show()
	
	
	
	
	
	
	
	
	
	
	
	
	




