
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

function listarsalaseespacos(combo_id,nome_classe) {
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
        $('#'+combo_id).empty();
        if (nome_classe=='Sala'){
            for (var i in dados) {
                $('#'+combo_id).append(
                    $('<option name='+dados[i].id+'></option>').attr("value", 
                        dados[i].nome_sala).text(dados[i].nome_sala+' - lotação - '+dados[i].lotacao));
                }
            }
        else{
            for (var i in dados) {
                $('#'+combo_id).append(
                    $('<option name='+dados[i].id+'></option>').attr("value", 
                    dados[i].nome_espaco).text(dados[i].nome_espaco))
                    ;
                }
    }               
}
}

function chamarsala(salaid,classe,numerosala,condicao) {
    listarsalasdisponiveis(salaid,classe,numerosala,condicao);

};

function chamarespaco() {
    listarsalaseespacos("espaco1id","EspacoCafe");
    listarsalaseespacos("espaco2id","EspacoCafe");

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
            for (var i in dados) {
                $('#'+combo_id).append(
                    $('<option name='+dados[i].id+'></option>').attr("value", 
                        dados[i].nome_sala).text(dados[i].nome_sala+' - lotação - '+dados[i].lotacao));
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

