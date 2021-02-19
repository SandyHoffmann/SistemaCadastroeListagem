from config import *

class EspacoCafe(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    nome_espaco = db.Column(db.String(40), nullable = False)
    def __str__(self):
        return str(self.id)+", "+ str(self.nome_espaco)
    
    def json(self):
        return {
            "id": self.id,
            "nome_espaco": self.nome_espaco
        }

class Sala(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    nome_sala = db.Column(db.String(40), nullable = False)
    lotacao = db.Column(db.Integer, nullable = True, default=0)
    def __str__(self):
        return str(self.id)+", "+ str(self.nome_sala)+", "+str(self.lotacao)
    
    def json(self):
        return {
            "id": self.id,
            "nome_sala": self.nome_sala,
            "lotacao": self.lotacao
        }

class Pessoa(db.Model):
    cpf = db.Column(db.String(10),primary_key=True)
    nome_pessoa = db.Column(db.String(40), nullable = False)
    sobrenome = db.Column(db.String(40), nullable = False)
    sala_um_id = db.Column(db.Integer,db.ForeignKey(Sala.id),nullable=False)
    sala_um = db.relationship("Sala",foreign_keys=[sala_um_id])
    sala_dois_id = db.Column(db.Integer,db.ForeignKey(Sala.id),nullable=False)
    sala_dois = db.relationship("Sala",foreign_keys=[sala_dois_id])
    espacocafe_um_id = db.Column(db.Integer,db.ForeignKey(EspacoCafe.id),nullable=False)
    espacocafe_um = db.relationship("EspacoCafe",foreign_keys=[espacocafe_um_id])
    espacocafe_dois_id = db.Column(db.Integer,db.ForeignKey(EspacoCafe.id),nullable=False)
    espacocafe_dois = db.relationship("EspacoCafe",foreign_keys=[espacocafe_dois_id])

    def __str__(self):
        return self.cpf+", "+ self.nome_pessoa+", "+self.sobrenome
    
    def json(self):
        return {
            "id": self.id,
            "nome_pessoa": self.nome_pessoa,
            "sobrenome": self.sobrenome,
            "sala_um_id": self.sala_um_id,
            "sala_um":self.sala_um.json(),
            "sala_dois_id": self.sala_dois_id,
            "sala_dois":self.sala_dois.json(),
            "espacocafe_um_id": self.espacocafe_um_id,
            "espacocafe_um":self.espacocafe_um.json(),
            "espacocafe_dois_id": self.espacocafe_dois_id,
            "espacocafe_dois":self.espacocafe_dois.json()
        }

if __name__ == "__main__":



"""    
    db.create_all()
    
    espaco1 = EspacoCafe(nome_espaco="cafe com leite")
    espaco2 = EspacoCafe(nome_espaco="cafe preto")
    espaco3 = EspacoCafe(nome_espaco="suco de laranja")
    espaco4 = EspacoCafe(nome_espaco="suco de uva")
    db.session.add(espaco1)
    db.session.add(espaco2)
    db.session.add(espaco3)
    db.session.add(espaco4)
    db.session.commit()
    print(EspacoCafe.query.get(3))

    sala1 = Sala(nome_sala="Sala 1")
    sala2 = Sala(nome_sala="Sala 2")
    sala3 = Sala(nome_sala="Sala 3")
    sala4 = Sala(nome_sala="Sala 4")
    db.session.add(sala1)
    db.session.add(sala2)
    db.session.add(sala3)
    db.session.add(sala4)
    db.session.commit()

    print(Sala.query.get(4))

"""