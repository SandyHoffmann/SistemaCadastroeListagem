 <img alt="GitHub language count" src="https://img.shields.io/badge/python-v3.7-purple"><img alt="GitHub language count" src="https://img.shields.io/badge/flask-v1.1.1-purple">

<h1>Sistema Cadastro e Listagem - Treinamento</h1>

Esse projeto tem como motivação fazer um site que possa cadastrar e listar dados, respeitando a uma série de normas, utilizando python, javascript e html.

## 🚀 Em que consiste o site?

O site de treinamentos consiste em uma ficticia empresa que faz treinamentos, e que esta querendo organizar seus participantes em salas, e espaços de café.
Para conseguir organizar os participantes de uma forma organizada, foram impostas algumas normas:

* :star: A diferença entre a lotação das salas deve ser de no máximo 1 pessoa.
* :star: Em cada fase as pessoas devem ser legistradas em espaços de café diferentes.

O funcionamento do site ocorre com a utilização das bibliotecas Python SQLAlchemy  e Flask, com o auxilio do js.

![image](https://user-images.githubusercontent.com/60969091/109430283-55dac280-79df-11eb-89e0-79c62c24f427.png)
<i>Foto da home do website</i>

Tem-se então um servidor rodando a aplicação, por meio de rotas que desencadeiam as funcionalidades do site:

```
#Rota para listar as salas, conversando com o JS
@app.route("/listar/Sala")
def listar_salas():
    salas = db.session.query(Sala).all()
    salasjs = [ x.json() for x in salas ]
    resposta = jsonify(salasjs)
    resposta.headers.add("Access-Control-Allow-Origin", "*") 
    return resposta

```
<i>Exemplo de Rota, encontrada no backend.py</i>

Há tambem a permanencia de dados, que ficam registrados no banco de dados intitulado como evento.db.
A criação de Tabelas desse bd é feita por meio do SqlAlchemy, que utiliza da classe Model.

```
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
```
<i>Exemplo de Tabela, encontrada no model.py</i>

E por fim, para auxiliar a conexão entre as páginas html e o backend (em python), tem-se o js, que chama as rotas, pega os dados, e encaminha para o html.

```
$(function(){ 
    $.ajax({
        url: 'http://localhost:5000/listar/Sala',
        method: 'GET',
        dataType: 'json', 
        success: listar_salas, 
        error: function() {
            alert("Deu erro");
        }
    });
```
<i>Exemplo de função de js, encontrada no js.js</i>

### 📋 Como Executar o Programa

Para executar o programa é necessário ter a linguagem python instalada no computador, e executar o requirements.txt.
Nele estão contidas as bibliotecas que o programa usa, sendo extremamente necessárias para que o software funcione.

```
flask
flask_sqlalchemy
flask_cors
pillow
pytest
```
<i>Trecho do requirements.txt</i>


## 🛠️ Construído com

* [Pyhon](https://www.python.org/) - Python
* [js](https://developer.mozilla.org/pt-BR/docs/Web/JavaScript) - Javascript

## ✒️ Autora

* **Sandy Hoffmann** - *Programação* - [Sandy Hoffmann](https://github.com/SandyHoffmann)

## 📄 Licença

Este projeto está sob a licença (sua licença).
