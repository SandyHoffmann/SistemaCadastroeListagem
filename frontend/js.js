
const registrar_pessoa = async() => {

    cpf = $("#cpf").val();
    nome_pessoa = $("#nome_pessoa").val();
    sobrenome = $("#sobrenome").val();
    sala_um_id = $("#sala1id").find('option:selected').attr("name");
    sala_dois_id = $("#sala2id").find('option:selected').attr("name");
    espacocafe_um_id = $("#espaco1id").find('option:selected').attr("name");
    espacocafe_dois_id = $("#espaco2id").find('option:selected').attr("name");
    var imagem = document.getElementById("fotoperfilteste").files[0];
    if (imagem != undefined){
        fotoperfil = await readFile(imagem);
    }
    else{
        fotoperfil = null;
    };

    dados = JSON.stringify({cpf:cpf, fotoperfil:fotoperfil, nome_pessoa:nome_pessoa,
        sobrenome:sobrenome, sala_um_id:sala_um_id,
        sala_dois_id:sala_dois_id,
        espacocafe_um_id:espacocafe_um_id, espacocafe_dois_id:espacocafe_dois_id});

    $.ajax({
        url: 'http://localhost:5000/incluir_pessoa',
        method: 'POST',
        contentType: 'application/json', 
        dataType: 'json',
        data: dados,
        success: incluir_pessoa, 
        error: erroincluir_pessoa
    });

    function incluir_pessoa(resposta){
        alert(resposta.resultado);
        alert(resposta.detalhes);
        if (resposta.resultado == 'Sucesso!'){
            alert('Parabens, seu cadastro foi um sucesso! ');
            $("#cpf").val("");
            $("#nome_pessoa").val("");
            $("#sobrenome").val("");
            $("#fotoperfil").val("");

        }
        else{
            alert('Algo não deu certo, tente novamente');
        }
    }
    
    function erroincluir_pessoa(resposta){
        alert('Algo não deu certo, tente novamente');
    }
    
};

function readURL(fotoperfil) {
    if (fotoperfil.files && fotoperfil.files[0]) {
      var reader = new FileReader();
      reader.onload = function (e) {
        $('#fotoperfil')
          .attr('src', e.target.result)
          .width(200)
          .height(200);
      };
      reader.readAsDataURL(fotoperfil.files[0]);
    }
};

async function readFile(fotoperfil) {

    return new Promise((resolve, reject) => {
        reader = new FileReader();

        reader.onload = () => {
            let base64 = (reader.result.split(",")[1]);
            resolve(base64);
        };

        reader.readAsDataURL(fotoperfil);
    
    })
};

function listarespacos(combo_id,numeroespaco,nome_classe) {
    $.ajax({
        url: 'http://localhost:5000/listar/'+nome_classe,
        method: 'GET',
        dataType: 'json',
        success: carregar,
        error: function(problema) {
            alert("erro, verifique backend ");
        }
    });
    function carregar (dados) {

        if (numeroespaco == 1){
            $('#'+combo_id).empty();
                for (var i in dados) {
                    $('#'+combo_id).append(
                        $('<option name='+dados[i].id+'></option>').attr("value", 
                        dados[i].nome_espaco).text(dados[i].nome_espaco))
                        ;
                    }
            }
        else{
            $('#'+combo_id).empty();
            idespacoselecionado = $("#espaco1id").find('option:selected').attr("name");
                for (var i in dados) {
                    if (dados[i].id != idespacoselecionado){
                        $('#'+combo_id).append(
                            $('<option name='+dados[i].id+'></option>').attr("value", 
                            dados[i].nome_espaco).text(dados[i].nome_espaco))
                            ;
                    }
                }
            }
    }               
}


function chamarsala(salaid,classe,numerosala,condicao) {
    listarsalasdisponiveis(salaid,classe,numerosala,condicao);

};

function chamarespaco(espacoid,numeroespaco) {
    listarespacos(espacoid, numeroespaco,"EspacoCafe");

};

const registrar_sala = async() => {

    nome_sala = $("#nome_sala").val();


    dados = JSON.stringify({nome_sala:nome_sala});

    $.ajax({
        url: 'http://localhost:5000/incluir_sala',
        method: 'POST',
        contentType: 'application/json', 
        dataType: 'json',
        data: dados,
        success: incluir_sala, 
        error: erroincluir_sala
    });

    function incluir_sala(resposta){
        alert(resposta.resultado);
        alert(resposta.detalhes);
        if (resposta.resultado == 'Sucesso!'){
            alert('Parabens, seu cadastro foi um sucesso! ');
            $("#").val("nome_sala");


        }
        else{
            alert('Algo não deu certo, tente novamente');
        }
    }
    
    function erroincluir_sala(resposta){
        alert('Algo não deu certo, tente novamente');
    }
    
};

function listarsalasdisponiveis(combo_id,nome_classe,numerosala,condicao) {
    $.ajax({
        url: 'http://localhost:5000/verificandosalas',
        method: 'GET',
        dataType: 'json',
        success: carregar,
        error: function(problema) {
            alert("erro, verifique backend  aaaaaaaaaa");
        }
    });
    function carregar (dados) {
        $('#'+combo_id).empty();
        if (numerosala==1){
            contador1 = 0
            contador2 = 0
            numeroa=0
            numerob=0
            n1=0
            n2=0
            lista = []
            for (var i in dados) {
                lista.push(dados[i].lotacao);
            }
            alert(lista);
            numeroinicial=lista[0];
            for (item in lista){
                contador1=lista[item]
                if (contador1==numeroinicial){
                    numeroa+=1
                    n1=lista[item]
                }
                if (contador1!=numeroinicial){
                    numerob+=1
                    n2=lista[item]
                }
            }
            alert(numeroa);
            alert(numerob);
            if (numeroa==1){
                for (var i in dados) {
                    if (dados[i].lotacao == n1){
                    $('#'+combo_id).append(
                        $('<option name='+dados[i].id+'></option>').attr("value", 
                            dados[i].nome_sala).text(dados[i].nome_sala+' - lotação - '+dados[i].lotacao));
                        }
                    }
                    }
            if (numerob==1){
                for (var i in dados) {
                    if (dados[i].lotacao == n2){
                    $('#'+combo_id).append(
                        $('<option name='+dados[i].id+'></option>').attr("value", 
                            dados[i].nome_sala).text(dados[i].nome_sala+' - lotação - '+dados[i].lotacao));
                        }
                    }
            }
            else{
                for (var i in dados) {
                    $('#'+combo_id).append(
                        $('<option name='+dados[i].id+'></option>').attr("value", 
                            dados[i].nome_sala).text(dados[i].nome_sala+' - lotação - '+dados[i].lotacao));
                        }
                }
            }
        else{
            idsalaselecionada = $("#sala1id").find('option:selected').attr("name"); 
            if (condicao =='salasdiferentes'){
                    for (var i in dados) {
                        if (dados[i].id != idsalaselecionada){
                            $('#'+combo_id).append(
                                $('<option name='+dados[i].id+'></option>').attr("value", 
                                    dados[i].nome_sala).text(dados[i].nome_sala+' - lotação - '+dados[i].lotacao));
                                }
                        }
                }
            else{
                for (var i in dados) {
                    if (dados[i].id == idsalaselecionada){
                    $('#'+combo_id).append(
                        $('<option name='+dados[i].id+'></option>').attr("value", 
                            dados[i].nome_sala).text(dados[i].nome_sala+' - lotação - '+dados[i].lotacao));
                        }
                    }
                }
                    
        }
        }
}


function verificar(){
    $.ajax({
        url: 'http://localhost:5000/verificarmetadepessoas',
        method: 'GET',
        dataType: 'json',
        success: lendoresposta,
        error: function(problema) {
            alert("erro, verifique backend  aaaaaaaaaa");
        }
    });
    function lendoresposta (escolhasalas) {
        if (escolhasalas == 'salas diferentes'){
            conteudo="<label for='sala1id' onClick=chamarsala('sala1id','Sala',1,'nenhum');>Salas Disponiveis - 1</label>"+
                        "<select class='form-control' id='sala1id' value='sala1id' aria-describedby='sala1id' placeholder='sala1id' onClick=chamarsala('sala2id','Sala',2,'salasdiferentes'); >"+
                        '</select>'+
                        '<div class="form-group">'+
                        '<label for="sala1id">Salas Disponiveis - 2</label>'+
                        '<select class="form-control" id="sala2id" value="sala2id" aria-describedby="sala2id" placeholder="sala2id" >'+
                        '</select>'+
                        '</div>'

            $('#teste').append( $(conteudo));
            alert("deubom");
        }
        if (escolhasalas == 'salas iguais'){
            conteudo="<label for='sala1id' onClick=chamarsala('sala1id','Sala',1,'nenhum');>Salas Disponiveis - 1</label>"+
                        "<select class='form-control' id='sala1id' value='sala1id' aria-describedby='sala1id' placeholder='sala1id' onClick=chamarsala('sala2id','Sala',2,'salasiguais'); >"+
                        '</select>'+
                        '<div class="form-group">'+
                        '<label for="sala1id">Salas Disponiveis - 2</label>'+
                        '<select class="form-control" id="sala2id" value="sala2id" aria-describedby="sala2id" placeholder="sala2id" >'+
                        '</select>'+
                        '</div>'
            $('#teste').append( $(conteudo));
            alert("deubom");
        }
}
}

const registrar_espaco_cafe = async() => {

    nome_espaco = $("#nome_espaco").val();

    dados = JSON.stringify({nome_espaco:nome_espaco});

    $.ajax({
        url: 'http://localhost:5000/incluir_espaco_cafe',
        method: 'POST',
        contentType: 'application/json', 
        dataType: 'json',
        data: dados,
        success: incluir_espaco_cafe, 
        error: erroincluir_espaco
    });

    function incluir_espaco_cafe(resposta){
        alert(resposta.resultado);
        alert(resposta.detalhes);
        if (resposta.resultado == 'Sucesso!'){
            alert('Parabens, seu cadastro foi um sucesso! ');
            $("#").val("nome_espaco");

        }
        else{
            alert('Algo não deu certo, tente novamente');
        }
    }
    
    function erroincluir_espaco(resposta){
        alert('Algo não deu certo, tente novamente');
    }
    
};

$(function(){ 
    $.ajax({
        url: 'http://localhost:5000/listar_pessoas',
        method: 'GET',
        dataType: 'json', 
        success: listar_pessoas, 
        error: function() {
            alert("Deu erro");
        }
    });

    function listar_pessoas(pessoas) {
        for (var i in pessoas) { 
            lin ='<div class="card" >'+
                    '<img class="card-img-top" src="../backend/'+pessoas[i].fotoperfil+'"alt="Card image cap">'+
                    '<div class="card-body">'+
                        '<h5 class="card-title">'+pessoas[i].nome_pessoa+' '+pessoas[i].sobrenome+'</h5>'+
                        '<p class="card-text">'+'CPF = '+pessoas[i].cpf+'</p>'+
                    '</div>'+
                    '<ul class="list-group list-group-flush" id=listasala>'+
                    '<hr>'+
                        '<b>Salas da Pessoa</b>'+
                        '<li class="list-group-item"> Etapa 1 - '+pessoas[i].sala_um.nome_sala+' - '+pessoas[i].sala_um.id+'</li>'+
                        '<li class="list-group-item"> Etapa 2 - '+pessoas[i].sala_dois.nome_sala+' - '+pessoas[i].sala_dois.id+'</li>'+
                    '</ul>'+
                    '<ul class="list-group list-group-flush" id=espacocafe>'+
                        '<b>Espaços de Café</b>'+
                        '<li class="list-group-item">'+pessoas[i].espacocafe_um.nome_espaco+' - '+pessoas[i].espacocafe_um.id+'</li>'+
                        '<li class="list-group-item">'+pessoas[i].espacocafe_dois.nome_espaco+' - '+pessoas[i].espacocafe_dois.id+'</li>'+
                        '</ul>'+
                '</div>'
            $('#blocolistar').append(lin);
        };
    }
})

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

    function listar_salas(salas) {
        for (var i in salas) { 
            lin ='<div class="card" style="width: 18rem;">'+
                    '<div class="card-body">'+
                    '<h5 class="card-title">'+salas[i].nome_sala+'</h5>'+
                    '<h6 class="card-subtitle mb-2 text-muted">Id - '+ salas[i].id+'</h6>'+
                    '<p class="card-text">Lotação  - '+ salas[i].lotacao+'</p>'+
                    '</div>'+
                '</div>'
            $('#blocolistarsalas').append(lin);
        };
    }
})

$(function(){ 
    $.ajax({
        url: 'http://localhost:5000/listar/EspacoCafe',
        method: 'GET',
        dataType: 'json', 
        success: listar_espaco_cafe, 
        error: function() {
            alert("Deu erro");
        }
    });

    function listar_espaco_cafe(espacos) {
        var lista = []
        for (var i in espacos) { 
            lin ='<div class="card" style="width: 18rem;">'+
                    '<div class="card-body">'+
                    '<h5 class="card-title">'+espacos[i].nome_espaco+'</h5>'+
                    '<h6 class="card-subtitle mb-2 text-muted">Id - '+ espacos[i].id+'</h6>'+
                    "<button onclick=document.getElementById('id01').style.display='block' class='salasespacosconferir'style='background-color: #888;color:whitesmoke;border-style: none;' idt='"+espacos[i].id+"'>Pessoas na Sala</button>"+
                    '<div class="salasespacosconferir" id="'+espacos[i].id+'"></div>'+
                    '</div>'+
                '</div>'
            $('#blocolistarpessoasespaco').append(lin);
        };
    }
})

$(document).on("click",".salasespacosconferir",function(){
    alert('a')
    var clicado = $(this).attr('idt');
    $.ajax({
        url: 'http://localhost:5000/listar_pessoas_espacos/'+clicado,
        method: 'GET',
        dataType: 'json',
        success: salasespacosconferir,
        error: function(problema) {
            alert("erro, verifique backend  aaaaaaaaaa");
        }
    });
    function salasespacosconferir(pessoas) {
        var node = document.getElementById("inicial");
        if (node.parentNode) {
        node.parentNode.removeChild(node);
        }
        conteudo='<div id="inicial">'
        for (var i in pessoas) { 
            conteudo += '<li class="list-group-item active" style="background-color:grey">'+pessoas[i].nome_pessoa+' '+pessoas[i].sobrenome+'</li>'+
                        '<li class="list-group-item">'+'CPF = '+pessoas[i].cpf+'</li>'+
                        '<li class="list-group list-group-flush" id=listasala>'+
                        '<hr>'+
                            '<b>Salas da Pessoa</b>'+
                            '<li class="list-group-item"> Etapa 1 - '+pessoas[i].sala_um.nome_sala+' - '+pessoas[i].sala_um.id+'</li>'+
                            '<li class="list-group-item"> Etapa 2 - '+pessoas[i].sala_dois.nome_sala+' - '+pessoas[i].sala_dois.id+'</li>'+
                        '</ul>'
        };
        conteudo+='</div>'
    $('#model').append(conteudo);

}})
