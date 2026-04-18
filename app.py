from flask import Flask, request, render_template
from controller import process_student
from database import create_table()

app=Flask(__name__)

@app.route('/')
def home():
	return render_template("index.html")	

@app.route('/submit', methods=['POST'])
def submit():
	form_data={
		"age"=request.form["age"]
		"sexe"=request.form["sexe"],
		"etude"=request.form["etude"],
		"sommeil"=request.form["sommeil"],
		"distraction"=request.form["distraction"],
		"env"=request.form["env"],
		"assiduite"=request.form["assiduite"],
		"ponctualite"=request.form["ponctualite"],
		"discipline"=request.form["discipline"],
		"taches"=request.form["tache"],
		"niveau"=request.form["niveau"],
		"moyenne"=request.form["moyenne"]
	}	
	
	process_student(form_data)
	
	return "Données enregistrées avec succès"

	
if __name__ == "__main__":
	create_table()
	app.run(debug=True)
	
