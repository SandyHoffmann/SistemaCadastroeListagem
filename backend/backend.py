from config import *
from model import Pessoa
from model import Sala
from model import EspacoCafe

@app.route("/home")
def home():
    return('alo')

@app.route("/listar_pessoas")
def listar_pessoas():
    pessoas = db.session.query(Pessoa).all()
    pessoasjs = [ x.json() for x in pessoas ]
    resposta = jsonify(pessoasjs)
    resposta.headers.add("Access-Control-Allow-Origin", "*") 
    return resposta

@app.route("/listar/Sala")
def listar_salas():
    salas = db.session.query(Sala).all()
    salasjs = [ x.json() for x in salas ]
    resposta = jsonify(salasjs)
    resposta.headers.add("Access-Control-Allow-Origin", "*") 
    return resposta

@app.route("/listar/EspacoCafe")
def listar_espacos():
    espacos = db.session.query(EspacoCafe).all()
    espacosjs = [ x.json() for x in espacos ]
    resposta = jsonify(espacosjs)
    resposta.headers.add("Access-Control-Allow-Origin", "*") 
    return resposta

def salvar_imagem_perfil(caminho, nomeimagem):
    novonome = secrets.token_hex(9)
    nomefoto = novonome + ".png"
    nomefoto='imagens/'+nomefoto
    diretorio = os.path.join(app.root_path, nomefoto )
    imagem = base64.b64decode(str(nomeimagem)) 
    imagemmenor = Image.open(io.BytesIO(imagem))
    tamanho_imagem = (200, 200)
    imagemmenor.thumbnail(tamanho_imagem)
    imagemmenor.save(diretorio)
    
    return nomefoto
    
@app.route('/incluir_pessoa', methods=['POST'])
def incluir_pessoa():
    resposta=jsonify({"resultado": "Sucesso!", "detalhes": "Seu cadastro foi um sucesso!"})
    dados=request.get_json()
    try:
        pessoa=Pessoa(**dados)
        if (dados["fotoperfil"] != None):
            print("aa")
            pessoa.fotoperfil=salvar_imagem_perfil('/imagens',(dados["fotoperfil"]))
        pessoa.cpf=pessoa.cpf.replace(".","")
        pessoa.cpf=pessoa.cpf.replace("-","")
        print(pessoa.cpf)
        db.session.add(pessoa)
        db.session.commit()
    except Exception as e: 
        resposta = jsonify({"resultado":"Erro!", "detalhes":str(e)}) 
    resposta.headers.add("Access-Control-Allow-Origin", "*") 
    return resposta

app.run(debug=True)
