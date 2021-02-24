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

@app.route("/verificandosalas")
def verificardados():
    salas = Sala.query.all()
    listasalas=[]
    salaspossiveis=[]
    quantinicial=[]
    for x in range(1,len(salas)+1):
        lotacaocount=Sala.query.filter_by(id=x).first()
        listasalas.append(lotacaocount.lotacao)
    totalsalas=listasalas
    print(totalsalas)
    salaminimo=min(totalsalas) 
    print(salaminimo) 
    salamaximo=max(totalsalas)
    print(salamaximo)
    if salaminimo==salamaximo:
        salaspossiveis=totalsalas
    else:
        for sala in totalsalas:
            if sala == salaminimo:
                salaspossiveis.append(sala)
    possivel=salaspossiveis
    print(possivel)
    salasencaminhadas=[]
    contador=1
    for x in possivel:
        sala=Sala.query.filter_by(id=contador,lotacao=x).first()
        contador+=1
        salasencaminhadas.append(sala)
    listasalas=salasencaminhadas
    salas = [ x.json() for x in listasalas ]
    print(salas)
    resposta = jsonify(salas)
    resposta.headers.add("Access-Control-Allow-Origin", "*") 
    return(resposta)

@app.route("/verificarmetadepessoas")
def verificarmetade():
    listapessoas = Pessoa.query.all()
    totalpessoas = len(listapessoas)
    pessoaanterior = listapessoas[totalpessoas-1]
    if pessoaanterior == None:
        escolhasalas = 'escolha inicial'
    else:
        if totalpessoas>1:
            pessoaanteanterior = listapessoas[totalpessoas-2]
        if pessoaanterior.sala_um_id == pessoaanterior.sala_dois_id:
            escolhasalas = 'salas diferentes'
        elif pessoaanterior.sala_um_id != pessoaanterior.sala_dois_id and totalpessoas==1:
            escolhasalas = 'salas iguais'
        elif (pessoaanteanterior.sala_um_id == pessoaanteanterior.sala_dois_id):
            escolhasalas = 'salas diferentes'
        elif (pessoaanteanterior.sala_um_id != pessoaanteanterior.sala_dois_id):
            escolhasalas = 'salas iguais'
    escolhasalas=jsonify(escolhasalas)
    return(escolhasalas)




app.run(debug=True)
verificardados()
