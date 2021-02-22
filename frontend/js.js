
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

function chamarsala() {
    listarsalaseespacos("sala1id","Sala");
    listarsalaseespacos("sala2id","Sala");

};

function chamarespaco() {
    listarsalaseespacos("espaco1id","EspacoCafe");
    listarsalaseespacos("espaco2id","EspacoCafe");

};