import config
from model import Pessoa,Sala
import math 

lotacaototal=0
pessoasreversas = Pessoa.query.all()
totalsalas = Sala.query.all()

listanumeroslotacao =[]

pessoasreversas.reverse()
totalsalas.reverse()

for sala in totalsalas:
    lotacaototal+=sala.lotacao
    listanumeroslotacao.append(sala.lotacao)

listamaioresnumeros = listanumeroslotacao.sort(reverse=True)
listamenoresnumeros = listanumeroslotacao.sort()
minimosala = min(listamenoresnumeros[1:])
maximosala = max(listamaioresnumeros)

redestribuicao= lotacaototal/len(totalsalas)
mediadepessoasporsala_high=math.ceil(redestribuicao) 
mediadepessoasporsala_low=redestribuicao-1

for x in listamenoresnumeros:
    while x.lotacao < mediadepessoasporsala_low:
        for y in listamaioresnumeros:
            while y.lotacao > mediadepessoasporsala_low:
                for pessoa in pessoasreversas:
                    if pessoa.sala_um.lotacao==y or pessoa_dois.lotacao==y:
                        if pessoa.sala_um_id == pessoa.sala_dois_id:
                            pessoa.sala_um.lotacao-=1
                            x.lotacao+=1
                            pessoa.sala_um_id=x.id       
                            pessoa.sala_dois_id=x.id       
                            db.session.commit()
                        elif pessoa.sala_um.lotacao==y:
                            pessoa.sala_um.lotacao-=1
                            x.lotacao+=1
                            pessoa.sala_dois_id=x.id       
                            db.session.commit()

                        elif pessoa.sala_dois.lotacao==y:
                            pessoa.sala_dois.lotacao-=1
                            x.lotacao+=1
                            pessoa.sala_dois_id=x.id       
                            db.session.commit()