//
// TextPrint
// Laboratoire IDHN
//

$(function() {

    // Declaration variables
    var login, mdp;

    $("#connexionButton").button().on("click", function() {
        login = $("#login").val();
        mdp = $("#password").val();

        if (((login === "idhn") && (mdp === "idhn3")) || ((login === "alexandra") && (mdp === "idhn_chemiirita"))) {
            var pageURL = $(location).attr("href");
            var pageURL = pageURL + "connexion";
            console.log(pageURL);
            window.open(pageURL, "_self");
        } else {
            $("#alert-message").removeClass("d-none");
        }
        
    });

});