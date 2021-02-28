from config import *
from config import db

#Classe Espaco café, possui apenas nome, e tem chave primaria no id
class EspacoCafe(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    nome_espaco = db.Column(db.String(40), nullable = False)
    def __str__(self):
        return str(self.id)+", "+ str(self.nome_espaco)
    
    def json(self):
        return {
            "id": self.id,
            "nome_espaco": self.nome_espaco,
        }

#Classe Sala, possui nome_sala e lotação, tem chave primaria no id

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
            "lotacao": self.lotacao,
        }

#Classe Pessoa, possui ligação com as duas outras classes, usando o cpf como chave primária.

class Pessoa(db.Model):
    cpf = db.Column(db.String(10),primary_key=True)
    fotoperfil = db.Column(db.String(40), nullable = False, default='imagens/fotopadrao.png')
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
        return str(self.cpf)+", "+ str(self.nome_pessoa)+", "+str(self.sobrenome)+", "+str(self.fotoperfil)+", "+str(self.sala_um_id)+", "+ str(self.sala_um)+", " + str(self.sala_dois_id)+", "+ str(self.sala_dois) +", "+str(self.espacocafe_um_id)+", "+ str(self.espacocafe_um)+", "+str(self.espacocafe_dois_id)+", "+ str(self.espacocafe_dois)
    
    def json(self):
        return {
            "cpf": self.cpf,
            "fotoperfil":self.fotoperfil,
            "nome_pessoa": self.nome_pessoa,
            "sobrenome": self.sobrenome,
            "sala_um_id": self.sala_um_id,
            "sala_um":self.sala_um.json(),
            "sala_dois_id": self.sala_dois_id,
            "sala_dois":self.sala_dois.json(),
            "espacocafe_um_id": self.espacocafe_um_id,
            "espacocafe_um":self.espacocafe_um.json(),
            "espacocafe_dois_id": self.espacocafe_dois_id,
            "espacocafe_dois":self.espacocafe_dois.json(),
        }

#aqui cria-se o bd
if __name__ == "__main__":
    db.create_all()