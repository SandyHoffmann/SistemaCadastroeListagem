from config import *
from model import Sala,Pessoa

redestribuicao=2
redestribuicao2=1

totalsalas = Sala.query.all()
totalpessoas = Pessoa.query.all()
totalsalas.reverse()
pessoasreversas = totalpessoas
pessoasreversas.reverse()
quantidade1 = 4
quantidade2 = 1

lotacaoexigidaqmenor = 1
lotacaoexigidaqmaior = 2

lotacaonecessariamenor=lotacaoexigidaqmenor*quantidade1
lotacaonecessariamaior=lotacaoexigidaqmaior*quantidade2

        if lotacaototal<len(totalsalas):
            pass
        elif redestribuicao == round(redestribuicao):
            quantidadedepessoasporsala = redestribuicao
            lotacaoporsala = lotacaototal
            for sala in totalsalas:
                while sala.lotacao<redestribuicao:
                    for pessoa in pessoasreversas:
                        salaantigaid1=Sala.query.filter_by(id=pessoa.sala_um_id).first()
                        salaantigaid2=Sala.query.filter_by(id=pessoa.sala_dois_id).first()
                        if lotacaoporsala>0:
                            if pessoa.sala_um_id == pessoa.sala_dois_id:
                                print('pessoa igual')
                                if pessoa.sala_um.lotacao>quantidadedepessoasporsala:
                                    print('teste')
                                    salaantigaid1.lotacao-=1
                                    sala.lotacao+=1
                                    print(sala.lotacao)
                                    pessoa.sala_um_id=sala.id       
                                    pessoa.sala_dois_id=sala.id       
                                    quantidadedepessoasporsala-=1
                                    db.session.commit()
                                elif pessoa.sala_dois_id!=sala.id:
                                    if pessoa.sala_dois.lotacao > quantidadedepessoasporsala:
                                        salaantigaid2.lotacao-=1
                                        sala.lotacao+=1
                                        pessoa.sala_dois_id=sala.id       
                                        quantidadedepessoasporsala-=1
                                        db.session.commit()
                                elif pessoa.sala_um_id!=sala.id:
                                    if pessoa.sala_um.lotacao > quantidadedepessoasporsala:
                                        salaantigaid1.lotacao-=1
                                        sala.lotacao+=1
                                        pessoa.sala_um_id=sala.id       
                                        quantidadedepessoasporsala-=1
                                        db.session.commit()
                                if quantidadedepessoasporsala==0:
                                    lotacaoporsala-=1
                                    quantidadedepessoasporsala=redestribuicao
        elif redestribuicao != round(redestribuicao):
            redestribuicao=math.ceil(redestribuicao) 
            redestribuicao2=redestribuicao-1
            n1=0
            n2=0
            lista1=[redestribuicao2,redestribuicao,lotacaototal]
            lista2=[1,1,len(totalsalas)]
            divisao=lista1[0]/lista2[0]
            lista1multiplicada = []
            lista2diminuida=[]
            for x in lista1:
                lista1multiplicada.append(x*divisao)
            for i in lista2:
                lista2diminuida.append(i-lista1multiplicada[n1])
                n1+=1
            divisao=lista1[1]/lista2diminuida[1]
            lista2multiplicada = []
            lista1diminuida=[]
            for x in lista2diminuida:
                lista2multiplicada.append(x*divisao)
            for i in lista1:
                lista1diminuida.append(i-lista2multiplicada[n2])
                n2+=1
            a=lista1diminuida[0]
            b=lista2diminuida[1]

            listafinal1=[]
            listafinal2=[]

            for y in lista1diminuida:
                listafinal1.append(y/a)
            for z in lista2diminuida:
                listafinal2.append(z/b)
                            
            quantidade1 = listafinal1[2]    
            quantidade2 = listafinal2[2]    

            print(quantidade1)
            print(quantidade2)
            #parei aqui

            #Revertendo a lista de pessoas para que as que mais recentes tenham que mudar de sala
            #afim de não prejudicar as que fizeram o cadastro antes.


            lotacaoexigidaqmaior=redestribuicao
            lotacaoexigidaqmenor=redestribuicao2

            lotacaonecessariamenor=lotacaoexigidaqmenor*quantidade1
            lotacaonecessariamaior=lotacaoexigidaqmaior*quantidade2

            for sala in totalsalas:
                while sala.lotacao<lotacaoexigidaqmaior:
                    print(sala.lotacao, sala.nome_sala)
                    for pessoa in pessoasreversas:
                        salaantigaid1=Sala.query.filter_by(id=pessoa.sala_um_id).first()
                        salaantigaid2=Sala.query.filter_by(id=pessoa.sala_dois_id).first()
                        if quantidade1>0 and lotacaoexigidaqmenor!=0:
                            if pessoa.sala_um_id == pessoa.sala_dois_id:
                                print('pessoa igual')
                                if pessoa.sala_um.lotacao>lotacaoexigidaqmenor:
                                    print('teste')
                                    salaantigaid1.lotacao-=1
                                    sala.lotacao+=1
                                    print(sala.lotacao)
                                    pessoa.sala_um_id=sala.id       
                                    pessoa.sala_dois_id=sala.id       
                                    lotacaoexigidaqmenor-=1
                                    db.session.commit()


                            elif pessoa.sala_dois_id!=sala.id:
                                if pessoa.sala_dois.lotacao > lotacaoexigidaqmenor:
                                    salaantigaid2.lotacao-=1
                                    sala.lotacao+=1
                                    pessoa.sala_dois_id=sala.id       
                                    lotacaoexigidaqmenor-=1
                                    db.session.commit()

                            elif pessoa.sala_um_id!=sala.id:
                                if pessoa.sala_um.lotacao > lotacaoexigidaqmenor:
                                    salaantigaid1.lotacao-=1
                                    sala.lotacao+=1
                                    pessoa.sala_um_id=sala.id       
                                    lotacaoexigidaqmenor-=1
                                    db.session.commit()

                            if lotacaoexigidaqmenor==0:
                                quantidade1-=1
                                lotacaoexigidaqmenor=redestribuicao2

                        elif quantidade2>0 and lotacaoexigidaqmaior!=0:
                            if pessoa.sala_um_id == pessoa.sala_dois_id:
                                print('pessoa igual 2')

                                if pessoa.sala_um.lotacao>lotacaoexigidaqmenor:
                                    salaantigaid1.lotacao-=1
                                    sala.lotacao+=1
                                    pessoa.sala_um_id=sala.id       
                                    pessoa.sala_dois_id=sala.id       
                                    lotacaoexigidaqmaior-=1
                                    db.session.commit()

                            elif pessoa.sala_dois_id!=sala.id:
                                if pessoa.sala_dois.lotacao > lotacaoexigidaqmenor:
                                    salaantigaid2.lotacao-=1
                                    sala.lotacao+=1
                                    pessoa.sala_dois_id=sala.id       
                                    lotacaoexigidaqmaior-=1
                                    db.session.commit()

                            elif pessoa.sala_um_id!=sala.id:
                                if pessoa.sala_um.lotacao > lotacaoexigidaqmenor:
                                    salaantigaid1.lotacao-=1
                                    sala.lotacao+=1
                                    pessoa.sala_um_id=sala.id       
                                    lotacaoexigidaqmaior-=1
                                    db.session.commit()
                        
                            if lotacaoexigidaqmenor==0:
                                quantidade2-=1
                                lotacaoexigidaqmaior=redestribuicao
                        