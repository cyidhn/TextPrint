//
// TextPrint
// Laboratoire IDHN
// 

// Attendre le chargement de jQuery
$(function() {

    // Ouvrir collections
    dialogCollections = $("#dialog-collections").dialog({
        autoOpen: false,
        height: 400,
        width: 450,
        modal: true,
    });
  
    $("#creer-collection").click(function() {
        dialogCollections.dialog("open");
    });

    // Creer un nouveau dossier
    $("#btn-creer-nouvelle-collection").click(function() {
        let titreDossier = $("#titre-collection").val();
        if (titreDossier == "") {
            alert("Erreur. Vous devez donner un titre à votre collection.")
        } else {
            $.ajax({
                type:'POST',
                url:'creer-collection',
                dataType:'html',
                data:{
                  titre: titreDossier
                },
                success:function(data1){
                    alert(data1);
                },
                error:function(err) {
                    alert("Une erreur s'est produite : " + err.responseText);
                }
            });
        }
    });

});