$(document).ready( function() {
    $("#id_data_nascimento").mask("00/00/0000")
    $("#id_data_instalacao").mask("00/00/0000")
    $("#id_cpf").mask("000.000.000-00");
    $("#id_cnpj").mask("00.000.000/0000-00");
    $("#id_telefone").mask("(00) 00000-0000");
    $("#id_cep").mask("00000-000")
}); 

function atualizarLocalizacao() {

    navigator.geolocation.getCurrentPosition(function(position) {
        $.ajax({
            url: "/tecnico/localizacao/atualizar",
            data: {
                "latitude": position.coords.latitude,
                "longitude": position.coords.longitude,
                "csrfmiddlewaretoken": window.CSRF_TOKEN
            },
            method: "POST"
        })
    })
}
