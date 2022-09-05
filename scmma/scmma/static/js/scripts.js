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


$(document).ready( function() {
    $("#id_data_nascimento").mask("00/00/0000")
    $("#id_data_instalacao").mask("00/00/0000")
    $("#id_cpf").mask("000.000.000-00");
    $("#id_cnpj").mask("00.000.000/0000-00");
    $("#id_telefone").mask("(00) 00000-0000");
    $("#id_cep").mask("00000-000")

    if ($(".tecnico-ocupado").prop("checked")) {
        atualizarLocalizacao();
    }

    $(".tecnico-ocupado").on("click", function() {
        tecnico_ocupado =  $(this).prop("checked") ? false : true;
        if (tecnico_ocupado) atualizarLocalizacao();
        $.ajax({
            url: "/tecnico/disponibilidade/atualizar",
            data: {
                // se o técnico estiver indisponível, altera para não ocupado
                // se o técnico estiver disponível, altera para ocupado
                "tecnico_ocupado": tecnico_ocupado,
                "csrfmiddlewaretoken": window.CSRF_TOKEN
            },
            method: "POST",
        });
    });
}); 
