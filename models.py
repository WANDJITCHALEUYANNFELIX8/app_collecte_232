class Student:
    def __init__(self, age, sexe, etude, sommeil, distraction, env, assiduite, ponctualite, discipline,tache, niveau, moyenne):

        self.age = age
        self.sexe = sexe
        self.etude = etude
        self.sommeil = sommeil
        self.distraction = distraction

        self.env = env
        self.assiduite = assiduite
        self.ponctualite = ponctualite
        self.discipline = discipline

        self.tache = tache
        self.niveau = niveau
        self.moyenne = moyenne


    def to_tuple(self):
        return (
            self.age,
            self.sexe,
            self.etude,
            self.sommeil,
            self.distraction,
            self.env,
            self.assiduite,
            self.ponctualite,
            self.discipline,
            self.tache,
            self.niveau,
            self.moyenne
        )
