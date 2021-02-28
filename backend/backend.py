from config import *
from model import Pessoa
from model import Sala
from model import EspacoCafe
from flask import render_template

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

@app.route("/listar_pessoas_espacos/<int:id>")
def listar_pessoas_espacos(id):
    pessoas=Pessoa.query.all()
    listapessoasdoespaco=[]
    for pessoa in pessoas:
        if pessoa.espacocafe_um_id==id and pessoa.espacocafe_dois_id==id:
            listapessoasdoespaco.append(pessoa)
        elif pessoa.espacocafe_um_id==id:
            listapessoasdoespaco.append(pessoa)        
        elif pessoa.espacocafe_dois_id==id:
            listapessoasdoespaco.append(pessoa)

    listapessoasdoespacojs = [ x.json() for x in listapessoasdoespaco ]
    resposta = jsonify(listapessoasdoespacojs)
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
        sala1 = pessoa.sala_um_id
        sala2 = pessoa.sala_dois_id
        espaco1 = pessoa.espacocafe_um_id
        espaco2 = pessoa.espacocafe_dois_id
        if sala1 == sala2:
            salaescolhida=Sala.query.get(sala1)
            salaescolhida.lotacao+=1
        else:
            salaescolhida1=Sala.query.get(sala1)
            salaescolhida1.lotacao+=1
            salaescolhida2=Sala.query.get(sala2)
            salaescolhida2.lotacao+=1
        db.session.add(pessoa)
        db.session.commit()
    except Exception as e: 
        resposta = jsonify({"resultado":"Erro!", "detalhes":str(e)}) 
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

@app.route('/incluir_sala', methods=['POST'])
def incluir_sala():
    resposta=jsonify({"resultado": "Sucesso!", "detalhes": "Seu cadastro foi um sucesso!"})
    dados=request.get_json()
    try:
        #Para novos cadastros de sala, as salas da etapa 1 e 2 das pessoas terão que ser redistribuidas, afim de manter o padrão da diferença
        #de no maximo uma pessoa por sala.
        sala=Sala(**dados)
        db.session.add(sala)
        db.session.commit()
    except Exception as e: 
        resposta = jsonify({"resultado":"Erro!", "detalhes":str(e)}) 
    resposta.headers.add("Access-Control-Allow-Origin", "*") 
    conferir_sala_nova()
    return resposta

def conferir_sala_nova():
        lotacaototal=0
        pessoasreversas = Pessoa.query.all()
        totalsalas = Sala.query.all()
        pessoasreversas.reverse()
        totalsalas.reverse()
        listanumeroslotacao=[]

        for sala in totalsalas:
            print(sala)
            lotacaototal+=sala.lotacao
            listanumeroslotacao.append(sala.lotacao)

        print(listanumeroslotacao)
        listamaioresnumeros = sorted(listanumeroslotacao,reverse=True)
        listamenoresnumeros = sorted(listanumeroslotacao)
        print(listamaioresnumeros)
        print(listamenoresnumeros)

        minimosala = min(listamenoresnumeros[1:])
        maximosala = max(listamaioresnumeros)

        distribuicaoporsala= lotacaototal/len(totalsalas)
        mediadepessoasporsala_high=math.ceil(distribuicaoporsala) 
        mediadepessoasporsala_low=mediadepessoasporsala_high-1

        
        if lotacaototal<len(totalsalas):
            pass
            print('a')
        else:          
            for y in listamaioresnumeros:
                for z in range(lotacaototal):
                    salay=Sala.query.filter_by(id=z,lotacao=y).first()
                    print(salay)
                    if salay:
                        if salay.lotacao > minimosala:
                            for x in listamenoresnumeros:
                                print(x)
                                salax=Sala.query.filter_by(lotacao=x).first()
                                print(salax)
                                if salax:
                                    for pessoa in pessoasreversas:
                                        if salax.lotacao < minimosala:
                                            print('aaaaa')
                                            if pessoa.sala_um_id == salay.id or pessoa.sala_dois_id ==salay.id:
                                                print(salax.lotacao,salax.id)
                                                print(salay.lotacao, salay.id)
                                                if pessoa.sala_um_id == pessoa.sala_dois_id:
                                                    print('a')
                                                    salay.lotacao-=1
                                                    salax.lotacao+=1
                                                    pessoa.sala_um=salax      
                                                    pessoa.sala_dois=salax
                                                    pessoa.sala_um_id=salax.id       
                                                    pessoa.sala_dois_id=salax.id       
                                                    db.session.commit()

                                                elif pessoa.sala_um_id==salay.id:
                                                    print('c')
                                                    salay.lotacao-=1
                                                    salax.lotacao+=1
                                                    pessoa.sala_um= salax
                                                    pessoa.sala_um_id=salax.id       
                                                    db.session.commit()

                                                elif pessoa.sala_dois_id==salay.id:
                                                    print('d')
                                                    salay.lotacao-=1
                                                    salax.lotacao+=1
                                                    pessoa.sala_dois = salax
                                                    pessoa.sala_dois_id=salax.id       
                                                    db.session.commit()
                    
@app.route('/incluir_espaco_cafe', methods=['POST'])
def incluir_espaco_cafe():
    resposta=jsonify({"resultado": "Sucesso!", "detalhes": "Seu cadastro foi um sucesso!"})
    dados=request.get_json()
    try:
        espacocafe=EspacoCafe(**dados)
        db.session.add(espacocafe)
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
        numeroescolhido=[]
        numerosalas=len(salaspossiveis)
        for x in range(1,numerosalas+1):
            numeroescolhido.append(x)
    else:
        contador=0
        numeroescolhido=[]
        for sala in totalsalas:
            contador+=1
            if sala == salaminimo:
                numeroescolhido.append(contador)
                salaspossiveis.append(sala)
                print(salaspossiveis)
                print(numeroescolhido)
        if len(salaspossiveis)==1:
            salaspossiveis=totalsalas
            numerosalas=len(salaspossiveis)
            numeroescolhido= []
            for x in range(1,numerosalas+1):
                numeroescolhido.append(x)
            
    possivel=salaspossiveis
    numerosdassalas=numeroescolhido
    print(numeroescolhido)
    salasencaminhadas=[]
    contador=0
    for x in possivel:
        sala=Sala.query.filter_by(id=numeroescolhido[contador],lotacao=x).first()
        salasencaminhadas.append(sala)
        contador+=1
        print(sala)
    listasalas=salasencaminhadas
    print(listasalas)
    salas = [ x.json() for x in listasalas ]
    print(salas)
    resposta = jsonify(salas)
    resposta.headers.add("Access-Control-Allow-Origin", "*") 
    return(resposta)

@app.route("/verificarmetadepessoas")
def verificarmetade():
    listapessoas = Pessoa.query.all()
    totalpessoas = len(listapessoas)
    a = not listapessoas
    print(a)
    if not listapessoas:
        escolhasalas = 'salas diferentes'
    elif totalpessoas == 1:
        escolhasalas = 'salas iguais'
    elif totalpessoas>1:
        if totalpessoas>1:
            pessoaanterior = listapessoas[totalpessoas-1]
        if totalpessoas>2:
            pessoaanteanterior = listapessoas[totalpessoas-2]
        if pessoaanterior.sala_um_id == pessoaanterior.sala_dois_id:
            escolhasalas = 'salas diferentes'
        elif pessoaanterior.sala_um_id != pessoaanterior.sala_dois_id:
            escolhasalas = 'salas iguais'
    escolhasalas=jsonify(escolhasalas)
    return(escolhasalas)

app.run(debug=True)