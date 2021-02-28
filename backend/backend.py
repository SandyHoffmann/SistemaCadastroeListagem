from config import *
from model import Pessoa
from model import Sala
from model import EspacoCafe
#Acima temos as importações padrão

#Rota para listar as pessoas, conversando com o JS
@app.route("/listar_pessoas")
def listar_pessoas():
    pessoas = db.session.query(Pessoa).all()
    pessoasjs = [ x.json() for x in pessoas ]
    resposta = jsonify(pessoasjs)
    resposta.headers.add("Access-Control-Allow-Origin", "*") 
    return resposta

#Rota para listar as salas, conversando com o JS
@app.route("/listar/Sala")
def listar_salas():
    salas = db.session.query(Sala).all()
    salasjs = [ x.json() for x in salas ]
    resposta = jsonify(salasjs)
    resposta.headers.add("Access-Control-Allow-Origin", "*") 
    return resposta

#Rota para listar os espaços de café, conversando com o JS
@app.route("/listar/EspacoCafe")
def listar_espacos():
    espacos = db.session.query(EspacoCafe).all()
    espacosjs = [ x.json() for x in espacos ]
    resposta = jsonify(espacosjs)
    resposta.headers.add("Access-Control-Allow-Origin", "*") 
    return resposta

#Essa rota serve para mostrar as pessoas que se encontram registradas em determinado espaço de café
#sendo util na página onde se lista os espaços.
@app.route("/listar_pessoas_espacos/<int:id>")
def listar_pessoas_espacos(id):
    pessoas=Pessoa.query.all()
    listapessoasdoespaco=[]
    #aqui eu faço a checagem das pessoas que possuem o id do espaco de café igual ao que foi requerido. 
    for pessoa in pessoas:
        if pessoa.espacocafe_um_id==id and pessoa.espacocafe_dois_id==id:
            listapessoasdoespaco.append(pessoa)
        elif pessoa.espacocafe_um_id==id:
            listapessoasdoespaco.append(pessoa)        
        elif pessoa.espacocafe_dois_id==id:
            listapessoasdoespaco.append(pessoa)

    listapessoasdoespacojs = [ x.json() for x in listapessoasdoespaco ]
    resposta = jsonify(listapessoasdoespacojs)
    #e depois eu mando essa lista pro js, onde é posteriormente inserida em um model html
    resposta.headers.add("Access-Control-Allow-Origin", "*") 
    return resposta

#Aqui faço a mesma coisa que fiz acima, pego as pessoas que estão alojadas nas salas, e organizo em uma lista
@app.route("/listar_pessoas_salas/<int:id>")
def listar_pessoas_salas(id):
    pessoas=Pessoa.query.all()
    listapessoasdasala=[]
    for pessoa in pessoas:
        if pessoa.sala_um_id==id and pessoa.sala_dois_id==id:
            listapessoasdasala.append(pessoa)
        elif pessoa.sala_um_id==id:
            listapessoasdasala.append(pessoa)        
        elif pessoa.sala_dois_id==id:
            listapessoasdasala.append(pessoa)

    listapessoasdasalajs = [ x.json() for x in listapessoasdasala ]
    resposta = jsonify(listapessoasdasalajs)
    #Após, mando essa lista para o js, e assim ela aparece na parte onde lista as salas, em um modal.
    resposta.headers.add("Access-Control-Allow-Origin", "*") 
    return resposta

#Esta é a parte onde ocorre a inclusão de pessoas, com o metodo Post
@app.route('/incluir_pessoa', methods=['POST'])
def incluir_pessoa():
    resposta=jsonify({"resultado": "Sucesso!", "detalhes": "Seu cadastro foi um sucesso!"})
    dados=request.get_json()
    try:
        pessoa=Pessoa(**dados)
        #Coloquei a foto de perfil como opcional, então a pessoa pode ter, ou não.
        if (dados["fotoperfil"] != None):
            pessoa.fotoperfil=salvar_imagem_perfil('/imagens',(dados["fotoperfil"]))
        #Retiro os caracteres da máscara do cpf, afim de não causar maus entendidos no db.
        #Escolhi o cpf como chave primária por conta de que aprendi que quando mexemos com pessoas em banco de dados
        #essa é a melhor opção.
        pessoa.cpf=pessoa.cpf.replace(".","")
        pessoa.cpf=pessoa.cpf.replace("-","")
        sala1 = pessoa.sala_um_id
        sala2 = pessoa.sala_dois_id
        espaco1 = pessoa.espacocafe_um_id
        espaco2 = pessoa.espacocafe_dois_id
        #Aqui, dependendo da sala que a pessoa escolher, eu faço a lotação aumentar.
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

#Essa função verifica se o usuario em questão ira ter salas iguais ou diferentes para as suas etapas.
#Decidi fazer assim para seguir a regra de que 50% das pessoas devem participar da segunda etapa do treinamento
#em salas diferentes. A lógica só não serve pra quando o numero for impar, então fiz para que quando for impar
#o usuario escolha salas diferentes.
@app.route("/verificarmetadepessoas")
def verificarmetade():
    listapessoas = Pessoa.query.all()
    totalpessoas = len(listapessoas)
    #primeiro usuário inicia com salas diferentes
    if not listapessoas:
        escolhasalas = 'salas diferentes'
    #O segundo com iguais
    elif totalpessoas == 1:
        escolhasalas = 'salas iguais'
    #E os demais vão seguindo essa ordem
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

#Aqui eu vejo que salas são possiveis de escolha para o usuário, afinal a diferença da lotação de salas
#pode ser de no máximo 1 pessoa.
@app.route("/verificandosalas")
def verificardados():
    #pego todas as salas
    salas = Sala.query.all()
    listasalas=[]
    salaspossiveis=[]
    #coloco em uma lista com as suas respectivas lotações
    for x in range(1,len(salas)+1):
        lotacaocount=Sala.query.filter_by(id=x).first()
        listasalas.append(lotacaocount.lotacao)
    totalsalas=listasalas
    #pego seu minimo e seu máximo
    salaminimo=min(totalsalas) 
    salamaximo=max(totalsalas)
    # e então sigo as condições
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
        if len(salaspossiveis)==1:
            salaspossiveis=totalsalas
            numerosalas=len(salaspossiveis)
            numeroescolhido= []
            for x in range(1,numerosalas+1):
                numeroescolhido.append(x)
            
    possivel=salaspossiveis
    numerosdassalas=numeroescolhido
    salasencaminhadas=[]
    contador=0
    #depois de conseguir as salas possiveis, retorno uma lista com os objetos de classe que são possiveis para escolher
    for x in possivel:
        sala=Sala.query.filter_by(id=numeroescolhido[contador],lotacao=x).first()
        salasencaminhadas.append(sala)
        contador+=1
    listasalas=salasencaminhadas
    salas = [ x.json() for x in listasalas ]
    resposta = jsonify(salas)
    resposta.headers.add("Access-Control-Allow-Origin", "*") 
    return(resposta)

#Essa função salva a foto de perfil no sistema
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

#Esse é o metodo que inclui novas salas.
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

#Essa função temo como intuito conferir a lotação das salas que as pessoas tem incluida, afim de redistribuir
#as pessoas, para manter a lotação com no máximo uma pessoa de diferença entre as salas. 
#Outro fator a ser respeitado é as condição de salas iguais ou diferentes que as pessoas escolheram inicialmente.
#Por conta desses fatores ela acabou ficando um pouco longa, para satisfazer a todas as condições impostas.
def conferir_sala_nova():
        #aqui eu seto as variaveis essenciais ao processo
        lotacaototal=0
        pessoasreversas = Pessoa.query.all()
        totalsalas = Sala.query.all()
        if len(totalsalas)>1:
            pessoasreversas.reverse()
            totalsalas.reverse()
            listanumeroslotacao=[]
            #nesse loop eu consigo a lotação de todas as salas
            for sala in totalsalas:
                lotacaototal+=sala.lotacao
                listanumeroslotacao.append(sala.lotacao)
            #com isso eu coloco elas em uma lista com maiores lotações e menores
            listamaioresnumeros = sorted(listanumeroslotacao,reverse=True)
            listamenoresnumeros = sorted(listanumeroslotacao)
            #aqui eu vejo o quanto eu tenho que ter por sala
            minimosala = min(listamenoresnumeros[1:])
            maximosala = max(listamaioresnumeros)
            #se a lotação total for menor do que o numero de salas, não temo o porquê de redistribuir
            #então a sala vai ser registrada com 0 lotação
            if lotacaototal<len(totalsalas):
                pass
            else:
                #aqui eu sigo as condições afim de fazer com que os itens da menor lista fiquem com a lotação minima necessária
                # e que os que tem a lotação maior distribuam para os menores.          
                for y in listamaioresnumeros:
                    for z in range(lotacaototal):
                        salay=Sala.query.filter_by(id=z,lotacao=y).first()
                        if salay:
                            if salay.lotacao > minimosala:
                                for x in listamenoresnumeros:
                                    salax=Sala.query.filter_by(lotacao=x).first()
                                    if salax:
                                        for pessoa in pessoasreversas:
                                            if salax.lotacao < minimosala:
                                                if pessoa.sala_um_id == salay.id or pessoa.sala_dois_id ==salay.id:
                                                    if pessoa.sala_um_id == pessoa.sala_dois_id:
                                                        salay.lotacao-=1
                                                        salax.lotacao+=1
                                                        pessoa.sala_um=salax      
                                                        pessoa.sala_dois=salax
                                                        pessoa.sala_um_id=salax.id       
                                                        pessoa.sala_dois_id=salax.id       
                                                        db.session.commit()

                                                    elif pessoa.sala_um_id==salay.id:
                                                        salay.lotacao-=1
                                                        salax.lotacao+=1
                                                        pessoa.sala_um= salax
                                                        pessoa.sala_um_id=salax.id       
                                                        db.session.commit()

                                                    elif pessoa.sala_dois_id==salay.id:
                                                        salay.lotacao-=1
                                                        salax.lotacao+=1
                                                        pessoa.sala_dois = salax
                                                        pessoa.sala_dois_id=salax.id       
                                                        db.session.commit()

#Essa função inclui o espaço do café
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


app.run(debug=True)