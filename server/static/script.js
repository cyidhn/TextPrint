//
// TextPrint
// Laboratoire IDHN
//

$(function() {
  // Declaration de variables
  var tabTitle = $('#tab_title'),
    tabContent = $('#tab_content'),
    tabTemplate =
      "<li><a href='#{href}'>#{label}</a> <span class='ui-icon ui-icon-close' role='presentation'>Remove Tab</span></li>",
    tabCounter = 2;

  // Initialisation
  var tabs = $('#tabs').tabs();
  $('body').bind('DOMSubtreeModified', function() {
    tabs.find('.ui-tabs-nav').sortable({
      axis: 'x',
      stop: function() {
        tabs.tabs('refresh');
      },
    });
  });

  // Ajouter tabs
  // Actual addTab function: adds new tab using the input from the form above
  function addTab(myContent, Titre) {
    var label = Titre || 'Tab ' + tabCounter,
      id = 'tabs-' + tabCounter,
      li = $(
        tabTemplate
          .replace(/#\{href\}/g, '#' + id)
          .replace(/#\{label\}/g, label),
      ),
      tabContentHtml = tabContent.val() || 'Tab ' + tabCounter + ' content.';

    tabs.find('.ui-tabs-nav').append(li);
    tabs.append("<div id='" + id + "'><p>" + myContent + '</p></div>');
    tabs.tabs('refresh');
    tabCounter++;
  }

  $('#menu').menu();
  $('#accordion').accordion();
  $('.widget input[type=submit], .widget a, .widget button').button();
  $('#dialog').dialog({
    modal: true,
    buttons: {
      Ok: function() {
        $(this).dialog('close');
      },
    },
  });

  // Ouvrir file import depuis le menu
  $('#menu-importer').click(function() {
    $('#file-import').trigger('click');
  });

  // Ouvrir la base de recherche depuis le menu
  $('#recherche-bdd').click(function() {
    $('#click-tabs-1').trigger('click');
  });

  // Ouvrir la table des paramètres
  dialogParams = $('#dialog-form-parametres').dialog({
    autoOpen: false,
    height: 400,
    width: 450,
    modal: true,
  });

  $('#parametres').click(function() {
    dialogParams.dialog('open');
  });

  // Creer un nouveau texte
  dialogTexte = $('#dialog-form-importer-texte').dialog({
    autoOpen: false,
    height: 400,
    width: 450,
    modal: true,
  });

  $('#creer-texte').click(function() {
    dialogTexte.dialog('open');
  });

  // Creer un profil connu
  dialog = $('#dialog-form-profil-connu').dialog({
    autoOpen: false,
    height: 400,
    width: 450,
    modal: true,
  });

  // Creer association profil / texte
  dialogAssociationProfil = $('#dialog-association-profil-texte').dialog({
    autoOpen: false,
    height: 400,
    width: 450,
    modal: true,
  });

  // Fenetre de dialogue Dossiers / Profils
  var dialogDossiersAssoc = $('#dialog-association-dossiers-profils').dialog({
    autoOpen: false,
    height: 500,
    width: 450,
    modal: true,
  });

  // Fenetre de dialogue Dossiers / Textes
  var dialogDossiersTextes = $('#dialog-association-dossiers-textes').dialog({
    autoOpen: false,
    height: 500,
    width: 450,
    modal: true,
  });

  // Fenetre de dialogue Dossiers / Textes
  var dialogDossiersCollections = $('#dialog-association-dossiers-collections').dialog({
    autoOpen: false,
    height: 500,
    width: 450,
    modal: true,
  });

  // Fenetre de dialogue Dossiers / Textes
  var dialogDossiersAnalyses = $('#dialog-association-dossiers-analyses').dialog({
    autoOpen: false,
    height: 500,
    width: 450,
    modal: true,
  });

  // Fenetre de dialogue Dossiers / Textes
  var dialogDossiersRapports = $('#dialog-association-dossiers-rapports').dialog({
    autoOpen: false,
    height: 500,
    width: 450,
    modal: true,
  });

  $('#creer-profil-connu').click(function() {
    dialog.dialog('open');
  });

  $('#btn-creer-profil-connu').click(function() {
    let regexAge = /^(([1-9])|([1-9][0-9])|([1][0-1][0-9])|120)$/;
    let typeP = 'connu';
    let alias = $('#alias').val();
    let prenom = $('#prenom').val();
    let nom = $('#nom').val();
    let age = $('#age').val();
    let sexe = $('#sexe').val();
    let education = $('#education').val();
    let sociale = $('#sociale').val();
    let commentaire = $('#commentaire').val();
    probAge = false;
    if (!regexAge.test(age)) {
        probAge = true;
    } else {
        probAge = false;
    }
    if (prenom == '' || nom == '' || probAge) {
      alert(
        "Une erreur s'est produite. Vous devez compléter au minimum le prénom et le nom. Vérifier que l'âge est compris entre 1 et 120.",
      );
    } else {
      $.post('/creer-profil-connu', {
        typeP: typeP,
        alias: alias,
        prenom: prenom,
        nom: nom,
        age: age,
        sexe: sexe,
        education: education,
        sociale: sociale,
        commentaire: commentaire,
      }).done(function(data) {
        let myId = 0;
        // Retrouver le dernier ID
        $.ajax({
          type: 'GET',
          url: 'lastid-profil',
          dataType: 'JSON',
          success: function(data1) {
            for (var i = 0; i < data1.length; i++) {
              var obj = data1[i];
              myId = obj.id;
              console.log('Dans last ID');
              // Ajouter les champs personnalises
              $('.ccc-element').each(function(index) {
                let myContent = $(this).val();
                console.log('Contenu : ' + myContent);
                if (myContent != '') {
                  $.post('/ajouter-champs-personnalises', {
                    id: myId,
                    contenu: myContent,
                  }).done(function(data) {
                    //document.location.reload(true);
                  });
                }
              });
            }
            setTimeout(function() {
              alert(
                'Le profil de ' +
                  nom.toUpperCase() +
                  ' ' +
                  prenom +
                  ' a bien été crée.',
              );
              dialog.dialog('close');
              document.location.reload(true);
            }, 3000);
          },
          error: function(XMLHttpRequest, textStatus, errorThrown) {
            console.log('Error on #retrouver-dernier-id.');
          },
        });
        $('#alias').val('');
        $('#prenom').val('');
        $('#nom').val('');
        $('#age').val('');
        $('#sexe').val('');
        $('#education').val('');
        $('#sociale').val('');
        $('#commentaire').val('');
        //$(".ui-corner-all").val("");
      });
    }
  });

  $('#btn-creer-profil-anonyme').click(function() {
    let regex = /^[1-9][0-9][-](([1-9])|([1-9][0-9])|([1][0-1][0-9])|120)$/;
    let typeP = 'anonyme';
    let alias =
      $('#alias-a').val() != ''
        ? $('#alias-a').val()
        : 'J.Dupont_' + Date.now();
    let prenom = $('#prenom-a').val();
    let nom = $('#nom-a').val();
    let age = $('#age-a').val();
    let sexe = $('#sexe-a').val();
    let education = $('#education-a').val();
    let sociale = $('#sociale-a').val();
    let commentaire = $('#commentaire-a').val();
    const wordsAge = age.split('-');
    let age1 = Number(wordsAge[0]);
    let age2 = Number(wordsAge[1]);
    if (!regex.test(age) || age1 > age2) {
      alert(
        "Erreur. L'âge doit correspondre à une intervalle entre 10 et 120. Exemple : 25-30",
      );
    } else {
      $.post('/creer-profil-connu', {
        typeP: typeP,
        alias: alias,
        prenom: prenom,
        nom: nom,
        age: age,
        sexe: sexe,
        education: education,
        sociale: sociale,
        commentaire: commentaire,
      }).done(function(data) {
        let myId = 0;
        // Retrouver le dernier ID
        $.ajax({
          type: 'GET',
          url: 'lastid-profil',
          dataType: 'JSON',
          success: function(data1) {
            for (var i = 0; i < data1.length; i++) {
              var obj = data1[i];
              myId = obj.id;
              console.log('Dans last ID');
              // Ajouter les champs personnalises
              $('.ccc-element').each(function(index) {
                let myContent = $(this).val();
                console.log('Contenu : ' + myContent);
                if (myContent != '') {
                  $.post('/ajouter-champs-personnalises', {
                    id: myId,
                    contenu: myContent,
                  }).done(function(data) {
                    //document.location.reload(true);
                  });
                }
              });
            }
            setTimeout(function() {
              alert('Le profil de ' + data + ' a bien été crée.');
              dialogProfilInconnu.dialog('close');
              document.location.reload(true);
            }, 3000);
          },
          error: function(XMLHttpRequest, textStatus, errorThrown) {
            console.log('Error on #retrouver-dernier-id.');
          },
        });
        $('#alias-a').val('');
        $('#prenom-a').val('');
        $('#nom-a').val('');
        $('#age-a').val('');
        $('#sexe-a').val('');
        $('#education-a').val('');
        $('#sociale-a').val('');
        $('#commentaire-a').val('');
        //$(".ui-corner-all-a").val("");
        //document.location.reload(true);
      });
    }
  });

  // Creer un profil anonyme
  dialogProfilInconnu = $('#dialog-form-profil-inconnu').dialog({
    autoOpen: false,
    height: 400,
    width: 450,
    modal: true,
  });

  $('#creer-profil-anonyme').click(function() {
    dialogProfilInconnu.dialog('open');
  });

  $('#btn-profil-anonyme').click(function() {
    $('#alias-a').val($('#alias').val());
    //$("#prenom-a").val($("#prenom").val());
    //$("#nom-a").val($("#nom").val());
    $('#age-a').val($('#age').val());
    $('#sexe-a').val($('#sexe').val());
    $('#education-a').val($('#education').val());
    $('#sociale-a').val($('#sociale').val());
    $('#commentaire-a').val($('#commentaire').val());
    $('.ui-corner-all-a').val('');
    dialog.dialog('close');
    dialogProfilInconnu.dialog('open');
  });

  $('#btn-profil-connu').click(function() {
    console.log('Alias : ' + $('#alias-a').val());
    $('#alias').val($('#alias-a').val());
    console.log('Alias : ' + $('#alias').val());
    //$("#prenom").val($("#prenom-a").val());
    //$("#nom").val($("#nom-a").val());
    $('#age').val($('#age-a').val());
    $('#sexe').val($('#sexe-a').val());
    $('#education').val($('#education-a').val());
    $('#sociale').val($('#sociale-a').val());
    $('#commentaire').val($('#commentaire-a').val());
    //$(".ui-corner-all").val("");
    dialogProfilInconnu.dialog('close');
    dialog.dialog('open');
  });

  // Recherche element
  $('#recherche').keyup(function() {
    var saisieRecherche = $('#recherche').val();
    $.post('/test', { req: saisieRecherche }).done(function(data) {
      for (let i in data) {
        console.log('Result : ' + i[1]);
      }
    });
  });

  // Ouvrir tabs
  $('#profil-1').click(function() {
    $('#element-masque').removeClass('d-none');
  });

  // Test
  $.ajax({
    type: 'POST',
    url: 'test',
    dataType: 'JSON',
    data: {
      req: '',
    },
    success: function(data1) {
      $('.list-group-item-action').remove();
      for (var i = 0; i < data1.length; i++) {
        var obj = data1[i];
        if (obj.type == 'Profil') {
          if (obj.typeP == 'connu') {
            let nomMaj = obj.nom;
            nomMaj = nomMaj.toUpperCase();
            if (obj.alias == '') {
              $('#search-result').append(
                '<button type="button" id="sresult-' +
                  obj.id +
                  '" class="list-group-item list-group-item-action sresult">Type : ' +
                  obj.type +
                  ' ' +
                  obj.typeP +
                  ' | Identifiant : ' +
                  obj.prenom +
                  ' ' +
                  nomMaj +
                  '</button>',
              );
            } else {
              $('#search-result').append(
                '<button type="button" id="sresult-' +
                  obj.id +
                  '" class="list-group-item list-group-item-action sresult">Type : ' +
                  obj.type +
                  ' ' +
                  obj.typeP +
                  ' | Identifiant : ' +
                  obj.prenom +
                  ' ' +
                  nomMaj +
                  ' (' +
                  obj.alias +
                  ')</button>',
              );
            }
          } else {
            $('#search-result').append(
              '<button type="button" id="sresult-' +
                obj.id +
                '" class="list-group-item list-group-item-action sresult">Type : ' +
                obj.type +
                ' ' +
                obj.typeP +
                ' | Identifiant : ' +
                obj.alias +
                '</button>',
            );
          }
        }
        if (obj.type == 'Texte') {
          $('#search-result').append(
            '<button type="button" id="sresultexte-' +
              obj.id +
              '" class="list-group-item list-group-item-action sresultexte">Type : Texte ' +
              ' | Identifiant : ' +
              obj.titre +
              '</button>',
          );
        }

        if (obj.type == 'Dossiers') {
          $('#search-result').append(
            '<button type="button" id="sresuldossi-' +
              obj.id +
              '" class="list-group-item list-group-item-action sresuldossi">Type : Dossiers ' +
              ' | Identifiant : ' +
              obj.titre +
              '</button>',
          );
        }

        if (obj.type == 'Collections') {
          $('#search-result').append(
            '<button type="button" id="sresulcolle-' +
              obj.id +
              '" class="list-group-item list-group-item-action sresulcolle">Type : Collections ' +
              ' | Identifiant : ' +
              obj.titre +
              '</button>',
          );
        }
      }
    },
    error: function(XMLHttpRequest, textStatus, errorThrown) {
      console.log('Error on #search-result.');
    },
  });

  // Recherche d'elements
  $('#recherche').keyup(function() {
    // Recuperer l'element
    let maRecherche = $('#recherche').val();
    // Recherche
    $.ajax({
      type: 'POST',
      url: 'test',
      dataType: 'JSON',
      data: {
        req: maRecherche,
      },
      success: function(data1) {
        $('.list-group-item-action').remove();
        for (var i = 0; i < data1.length; i++) {
          var obj = data1[i];
          if (obj.type == 'Profil') {
            if (obj.typeP == 'connu') {
              let nomMaj = obj.nom;
              nomMaj = nomMaj.toUpperCase();
              if (obj.alias == '') {
                $('#search-result').append(
                  '<button type="button" id="sresult-' +
                    obj.id +
                    '" class="list-group-item list-group-item-action sresult">Type : ' +
                    obj.type +
                    ' ' +
                    obj.typeP +
                    ' | Identifiant : ' +
                    obj.prenom +
                    ' ' +
                    nomMaj +
                    '</button>',
                );
              } else {
                $('#search-result').append(
                  '<button type="button" id="sresult-' +
                    obj.id +
                    '" class="list-group-item list-group-item-action sresult">Type : ' +
                    obj.type +
                    ' ' +
                    obj.typeP +
                    ' | Identifiant : ' +
                    obj.prenom +
                    ' ' +
                    nomMaj +
                    ' (' +
                    obj.alias +
                    ')</button>',
                );
              }
            } else {
              $('#search-result').append(
                '<button type="button" id="sresult-' +
                  obj.id +
                  '" class="list-group-item list-group-item-action sresult">Type : ' +
                  obj.type +
                  ' ' +
                  obj.typeP +
                  ' | Identifiant : ' +
                  obj.alias +
                  '</button>',
              );
            }
          }
          if (obj.type == 'Texte') {
            $('#search-result').append(
              '<button type="button" id="sresultexte-' +
                obj.id +
                '" class="list-group-item list-group-item-action sresultexte">Type : Texte ' +
                ' | Identifiant : ' +
                obj.titre +
                '</button>',
            );
          }

          if (obj.type == 'Dossiers') {
            $('#search-result').append(
              '<button type="button" id="sresuldossi-' +
                obj.id +
                '" class="list-group-item list-group-item-action sresuldossi">Type : Dossiers ' +
                ' | Identifiant : ' +
                obj.titre +
                '</button>',
            );
          }

          if (obj.type == 'Collections') {
            $('#search-result').append(
              '<button type="button" id="sresulcolle-' +
                obj.id +
                '" class="list-group-item list-group-item-action sresulcolle">Type : Collections ' +
                ' | Identifiant : ' +
                obj.titre +
                '</button>',
            );
          }
        }
      },
      error: function(XMLHttpRequest, textStatus, errorThrown) {
        console.log('Error on #search-result.');
      },
    });
  });

  // Trouver un profil pour l'association
  function rechercheProfil() {
    // Recuperer l'element
    let maRecherche = $('#recherche-profil').val();
    // Recherche
    $.ajax({
      type: 'POST',
      url: 'searchprofil',
      dataType: 'JSON',
      data: {
        req: maRecherche,
      },
      success: function(data1) {
        $('.list-profil-action').remove();
        for (var i = 0; i < data1.length; i++) {
          var obj = data1[i];
          if (obj.type == 'Profil') {
            if (obj.typeP == 'connu') {
              let nomMaj = obj.nom;
              nomMaj = nomMaj.toUpperCase();
              if (obj.alias == '') {
                $('#search-result-profil').append(
                  '<button type="button" id="sresult-' +
                    obj.id +
                    '" class="list-group-item list-profil-action list-group-item-action sresult">Type : ' +
                    obj.type +
                    ' ' +
                    obj.typeP +
                    ' | Identifiant : ' +
                    obj.prenom +
                    ' ' +
                    nomMaj +
                    '</button>',
                );
              } else {
                $('#search-result-profil').append(
                  '<button type="button" id="sresult-' +
                    obj.id +
                    '" class="list-group-item list-profil-action list-group-item-action sresult">Type : ' +
                    obj.type +
                    ' ' +
                    obj.typeP +
                    ' | Identifiant : ' +
                    obj.prenom +
                    ' ' +
                    nomMaj +
                    ' (' +
                    obj.alias +
                    ')</button>',
                );
              }
            } else {
              $('#search-result-profil').append(
                '<button type="button" id="sresult-' +
                  obj.id +
                  '" class="list-group-item list-profil-action list-group-item-action sresult">Type : ' +
                  obj.type +
                  ' ' +
                  obj.typeP +
                  ' | Identifiant : ' +
                  obj.alias +
                  '</button>',
              );
            }
          } else {
            $('#search-result-profil').append(
              '<button type="button" id="sresultexte-' +
                obj.id +
                '" class="list-group-item list-profil-action list-group-item-action sresultexte">Type : Texte ' +
                ' | Identifiant : ' +
                obj.titre +
                '</button>',
            );
          }
        }
      },
      error: function(XMLHttpRequest, textStatus, errorThrown) {
        console.log('Error on #search-result.');
      },
    });
  }

    // Trouver un profil pour l'association profil / Dossier
    function rechercheProfilDossiers() {
      // Recuperer l'element
      let maRecherche = $('#recherche-profild').val();
      // Recherche
      $.ajax({
        type: 'POST',
        url: 'searchprofil',
        dataType: 'JSON',
        data: {
          req: maRecherche,
        },
        success: function(data1) {
          $('.list-profil-action').remove();
          for (var i = 0; i < data1.length; i++) {
            var obj = data1[i];
            if (obj.type == 'Profil') {
              if (obj.typeP == 'connu') {
                let nomMaj = obj.nom;
                nomMaj = nomMaj.toUpperCase();
                if (obj.alias == '') {
                  $('#search-result-dprofil').append(
                    '<button type="button" id="sresult-' +
                      obj.id +
                      '" class="list-group-item list-profil-action list-group-item-action sresult dprofil">Type : ' +
                      obj.type +
                      ' ' +
                      obj.typeP +
                      ' | Identifiant : ' +
                      obj.prenom +
                      ' ' +
                      nomMaj +
                      '</button>',
                  );
                } else {
                  $('#search-result-dprofil').append(
                    '<button type="button" id="sresult-' +
                      obj.id +
                      '" class="dprofil list-group-item list-profil-action list-group-item-action sresult">Type : ' +
                      obj.type +
                      ' ' +
                      obj.typeP +
                      ' | Identifiant : ' +
                      obj.prenom +
                      ' ' +
                      nomMaj +
                      ' (' +
                      obj.alias +
                      ')</button>',
                  );
                }
              } else {
                $('#search-result-dprofil').append(
                  '<button type="button" id="sresult-' +
                    obj.id +
                    '" class="dprofil list-group-item list-profil-action list-group-item-action sresult">Type : ' +
                    obj.type +
                    ' ' +
                    obj.typeP +
                    ' | Identifiant : ' +
                    obj.alias +
                    '</button>',
                );
              }
            } else {
              $('#search-result-dprofil').append(
                '<button type="button" id="sresultexte-' +
                  obj.id +
                  '" class="dprofil list-group-item list-profil-action list-group-item-action sresultexte">Type : Texte ' +
                  ' | Identifiant : ' +
                  obj.titre +
                  '</button>',
              );
            }
          }
        },
        error: function(XMLHttpRequest, textStatus, errorThrown) {
          console.log('Error on #recherche-profild-11.');
        },
      });
    }

    // Trouver un profil pour l'association profil / Dossier
    function rechercheTextesDossiers() {
      // Recuperer l'element
      let maRecherche = $('#recherche-texted').val();
      // Recherche
      $.ajax({
        type: 'POST',
        url: 'searchtextes',
        dataType: 'JSON',
        data: {
          req: maRecherche,
        },
        success: function(data1) {
          $('.list-profil-action').remove();
          for (var i = 0; i < data1.length; i++) {
            var obj = data1[i];
            if (obj.type == 'Profil') {
              if (obj.typeP == 'connu') {
                let nomMaj = obj.nom;
                nomMaj = nomMaj.toUpperCase();
                if (obj.alias == '') {
                  $('#search-result-dtextes').append(
                    '<button type="button" id="sresult-' +
                      obj.id +
                      '" class="list-group-item list-profil-action list-group-item-action sresult dprofil">Type : ' +
                      obj.type +
                      ' ' +
                      obj.typeP +
                      ' | Identifiant : ' +
                      obj.prenom +
                      ' ' +
                      nomMaj +
                      '</button>',
                  );
                } else {
                  $('#search-result-dtextes').append(
                    '<button type="button" id="sresult-' +
                      obj.id +
                      '" class="dprofil list-group-item list-profil-action list-group-item-action sresult">Type : ' +
                      obj.type +
                      ' ' +
                      obj.typeP +
                      ' | Identifiant : ' +
                      obj.prenom +
                      ' ' +
                      nomMaj +
                      ' (' +
                      obj.alias +
                      ')</button>',
                  );
                }
              } else {
                $('#search-result-dtextes').append(
                  '<button type="button" id="sresult-' +
                    obj.id +
                    '" class="dprofil list-group-item list-profil-action list-group-item-action sresult">Type : ' +
                    obj.type +
                    ' ' +
                    obj.typeP +
                    ' | Identifiant : ' +
                    obj.alias +
                    '</button>',
                );
              }
            } else {
              $('#search-result-dtextes').append(
                '<button type="button" id="sresultexte-' +
                  obj.id +
                  '" class="dprofil list-group-item list-profil-action list-group-item-action sresultexte">Type : Texte ' +
                  ' | Identifiant : ' +
                  obj.titre +
                  '</button>',
              );
            }
          }
        },
        error: function(XMLHttpRequest, textStatus, errorThrown) {
          console.log('Error on #recherche-profild-11.');
        },
      });
    }

  // Activation fenetre dialogue
  rechercheProfil();
  $('#recherche-profil').keyup(function() {
    rechercheProfil();
  });
  rechercheProfilDossiers();
  $('#recherche-profild').keyup(function() {
    rechercheProfilDossiers();
  });
  rechercheTextesDossiers()
  $('#recherche-texted').keyup(function() {
    rechercheTextesDossiers();
  });

  // Afficher un profil apres le clique
  let vPoint = 0;
  let tPoint = 0;
  setInterval(() => {
    vPoint = 0;
    tPoint = 0;
  }, 1000);
  $('#search-result-profil').bind('DOMSubtreeModified', function() {
    // Associer profil
    $('.list-profil-action').click(function() {
      let idElement = $(this).attr('id');
      idElement = idElement.substring(8);
      idTexte = $('#id-element-texte').val();

      if (tPoint != idElement) {
        // Verif
        tPoint = idElement;
        console.log('id_texte: ' + idTexte + ' // id_profil: ' + idTexte);

        if (confirm('Voulez-vous vraiment associer ce profil à ce texte ?')) {
          $.post('/associer-profil-texte', {
            id_profil: idElement,
            id_texte: idTexte,
          }).done(function(data) {
            document.location.reload(true);
            infoElement = 0;
            //document.location.reload(true);
          });
        }
      }
    });
  });

  $('#search-result-dprofil').bind('DOMSubtreeModified', function() {
    // Associer profil
    $('.list-profil-action').click(function() {
      let idElement = $(this).attr('id');
      idElement = idElement.substring(8);
      idTexte = $('#id-element-profild').val();

      if (tPoint != idElement) {
        // Verif
        tPoint = idElement;
        console.log('id_dossier : ' + idTexte + ' // id_profil: ' + idElement);

          $.post('/associer-generalement', {
            champs1: "Dossier",
            champs2: "Profil",
            idchamps1: idTexte,
            idchamps2: idElement,
          }).done(function(data) {
            //document.location.reload(true);
            $(`.ui-icon-close`).click();
            getDossier(idTexte);
            alert("Le profil a bien été ajouté à ce dossier.");
            dialogDossiersAssoc.dialog("close");
            infoElement = 0;
            //document.location.reload(true);
          }).fail(function(xhr, status, error) {
            alert("Erreur : " + xhr.responseText);
          });
      }
    });
  });

  $('#search-result-dtextes').bind('DOMSubtreeModified', function() {
    // Associer profil
    $('.list-profil-action').click(function() {
      let idElement = $(this).attr('id');
      idElement = idElement.substring(12);
      idTexte = $('#id-element-texted').val();

      if (tPoint != idElement) {
        // Verif
        tPoint = idElement;
        console.log('id_dossier : ' + idTexte + ' // id_texte: ' + idElement);

          $.post('/associer-generalement', {
            champs1: "Dossier",
            champs2: "Texte",
            idchamps1: idTexte,
            idchamps2: idElement,
          }).done(function(data) {
            $(`.ui-icon-close`).click();
            getDossier(idTexte);
            alert("Le texte a bien été ajouté à ce dossier.");
            dialogDossiersAssoc.dialog("close");            infoElement = 0;
            //document.location.reload(true);
          });
      }
    });
  });

  $('#search-result').bind('DOMSubtreeModified', function() {
    $('.sresultexte').click(function() {
      // Recuperer l'id
      console.log('Vpoint = ' + vPoint);
      console.log('+++');
      var elementId = $(this).attr('id');
      var words = elementId.split('-');
      elementId = words[1];
      console.log('ID : ' + elementId);

      if (vPoint != elementId) {
        // Verif
        vPoint = elementId;

        // Recuperer donnees
        $.post('search-texte', { req: elementId }).done(function(data) {
          // Recuperer donnees
          let id = data[0].id;
          let fichier = data[0].fichier;
          let titre = data[0].titre;
          let paternite = data[0].paternite;
          let typeDocument1 = data[0].typeDocument1;
          let typeDocument2 = data[0].typeDocument2;
          let typeDocument3 = data[0].typeDocument3;
          let specification = data[0].specification;
          let typeEcriture = data[0].typeEcriture;
          let segmentation = data[0].segmentation;
          let langue = data[0].langue;
          let registre = data[0].registre;
          let commentaire = data[0].commentaire;

          // Verifier s'il existe dans les tabs
          if (
            $('.ui-tabs-anchor')
              .text()
              .indexOf(titre) > -1
          ) {
          } else {
            // Creer un nouvel onglet
            //$("#my-tabs").append(`<li><a href="#tabsa-${elementId}">Profil - <b>${alias}</b></a></li>`)

            // Ajouter la tabs
            /* Ajouter l'analyse
           <iframe
            height="500"
            width="70%"
            src="/static/textes/${fichier}_analyse.html">
          </iframe>
          */
            let donneesTabs = `
          <div id="popup-search" style="overflow-y: scroll; height:500px;">
          <button class="ouvrir-analyse" id="ela-element-${fichier}">Voir l'analyse</button>
          <button class="associer-tabs" id="ass-element-${id}">Associer à un profil existant</button>
          <div class="row mt-3">
          <div class="col-md-4">
          <iframe
              height="500"
              width="100%"
              src="/static/textes/${fichier}.txt">
          </iframe>
          </div>
          <div class="col-md-8">
          <fieldset>
          <!-- Grand titre -->
          <h5 class="mb-2"><b>Importation</b></h5>

          <!-- Label -->
          <label for="alias">Titre du texte*</label>
          <input type="text" name="alias" id="titretexteb-${id}" value="${titre}" class="text ui-widget-content ui-corner-all">

          <!-- Type paternité -->
          <label for="paternite">Type de paternité*</label>
          <select name="paternite" id="paterniteb-${id}">
            <option value="no" ${
              paternite == 'no' ? 'selected' : ''
            }>Non spécifié</option>
            <option value="anonyme" ${
              paternite == 'anonyme' ? 'selected' : ''
            }>Anonyme</option>
            <option value="connu" ${
              paternite == 'connu' ? 'selected' : ''
            }>Connu</option>
          </select>

          <!-- Grand titre -->
          <h5 class="mt-5 mb-2"><b>Mise en forme</b></h5>

          <!-- Type document -->
          <label class="mt-4" for="type-document">Type de document</label>
          <select name="type-document" id="type-document-1" disabled>
            <option value="no">${typeDocument1}</option>
          </select>

          <select class="mt-3" name="type-document" id="type-document-2" disabled>
            <option value="no">${typeDocument2}</option>
          </select>

          <input type="text" name="autre" id="type-document-3" value="${typeDocument3}" class="text ui-widget-content ui-corner-all mt-3 d-none" disabled>


          <!-- Specification (autre) -->
          <label class="mt-4" for="autre">Spécification</label>
          <input type="text" name="autre" id="specificationtexteb-${id}" value="${specification}" class="text ui-widget-content ui-corner-all">

          <!-- Type d'écriture -->
          <label class="mt-4" for="type-ecriture-b">Type d'écriture</label>
          <select name="type-ecriture" id="typeecritureb-${id}">
            <option value="Non spécifié" ${
              typeEcriture == 'Non spécifié' ? 'selected' : ''
            }>Non spécifié</option>
            <option value="Manuscrite" ${
              typeEcriture == 'Manuscrite' ? 'selected' : ''
            }>Manuscrite</option>
            <option value="Tapuscrite" ${
              typeEcriture == 'Tapuscrite' ? 'selected' : ''
            }>Tapuscrite</option>
            <option value="Dactylographié" ${
              typeEcriture == 'Dactylographié' ? 'selected' : ''
            }>Dactylographié</option>
            <option value="Autre" ${
              typeEcriture == 'Autre' ? 'selected' : ''
            }>Autre</option>
          </select>

          <!-- Segmentation -->
          <label class="mt-4" for="segmentation-b">Segmentation</label>
          <select name="segmentation" id="segmentationb-${id}">
            <option value="Non spécifiée" ${
              segmentation == 'Non spécifiée' ? 'selected' : ''
            }>Non spécifiée</option>
            <option value="Origine" ${
              segmentation == 'Origine' ? 'selected' : ''
            }>D'origine</option>
            <option value="Passage" ${
              segmentation == 'Passage' ? 'selected' : ''
            }>Passage</option>
            <option value="Compilation" ${
              segmentation == 'Compilation' ? 'selected' : ''
            }>Compilation</option>
          </select>

          <!-- Grand titre -->
          <h5 class="mt-5 mb-2"><b>Description linguistique</b></h5>
          <!-- Langue -->
          <label for="langue-b">Langue (automatique)</label>
          <input type="text" name="langue" id="langue-b" value="${langue}" class="text ui-widget-content ui-corner-all" disabled>

          <!-- Registre -->
          <label for="registre">Registre</label>
          <select name="registre" id="registreb-${id}">
            <option value="Non spécifié" ${
              registre == 'Non spécifié' ? 'selected' : ''
            }>Non spécifié</option>
            <option value="Courant" ${
              registre == 'Courant' ? 'selected' : ''
            }>Courant</option>
            <option value="Familier" ${
              registre == 'Familier' ? 'selected' : ''
            }>Familier</option>
            <option value="Soutenu" ${
              registre == 'Soutenu' ? 'selected' : ''
            }>Soutenu</option>
          </select>

          <label class="mt-4" for="commentaire-b">Commentaire</label>
          <textarea name="commentaire" id="commentaireb-${id}" class="text ui-widget-content ui-corner-all" style="width: 100%;" cols="30" rows="10">${commentaire}</textarea>

          <!-- Allow form submission with keyboard without duplicating the dialog button -->
          <button class="maj-texte" id="sup-element-${id}">Mettre à jour le texte</button>
          <button class="supprimer-texte" id="sup-element-${id}">Supprimer la fiche</button>
      </fieldset>
          <h3 class="mt-3">Versions</h3>
          <table class="table">
          <thead>
            <tr>
              <th scope="col">Titre</th>
              <th scope="col"># Versions</th>
            </tr>
          </thead>
          <tbody>

          </tbody>
        </table>
          <h3 class="mt-3">Collections</h3>
            <table class="table">
            <thead>
              <tr>
                <th scope="col">Titre</th>
                <th scope="col"># de textes par l'auteur</th>
                <th scope="col"># de mots par l'auteur</th>
              </tr>
            </thead>
            <tbody>

            </tbody>
          </table>
          <h3 class="mt-3">Dossiers</h3>
          <table class="table">
          <thead>
            <tr>
              <th scope="col">Titre</th>
              <th scope="col"># de textes par l'auteur</th>
              <th scope="col"># de mots par l'auteur</th>
            </tr>
          </thead>
          <tbody>

          </tbody>
        </table>
        <h3 class="mt-3">Analyses</h3>
        <table class="table">
        <thead>
          <tr>
            <th scope="col">Titre</th>
            <th scope="col">Type d'analyse</th>
            <th scope="col">Ressources de l'auteur</th>
          </tr>
        </thead>
        <tbody>

        </tbody>
      </table>
      <h3 class="mt-3">Rapports</h3>
      <table class="table">
      <thead>
        <tr>
          <th scope="col">Titre</th>
          <th scope="col">Type de rapport</th>
        </tr>
      </thead>
      <tbody>

      </tbody>
    </table>
          </div>
          </div>
          </div>
          `;

            // Creer onglet
            addTab(donneesTabs, titre);
            $(`.ui-tabs-anchor:contains(${titre})`).click();
          }
        });
      }
    });

    $('.sresult').click(function() {
      // Recuperer l'id
      console.log('Vpoint = ' + vPoint);
      console.log('+++');
      var elementId = $(this).attr('id');
      var words = elementId.split('-');
      elementId = words[1];
      console.log('ID : ' + elementId);

      if (vPoint != elementId) {
        // Verif
        vPoint = elementId;

        // Recuperer donnees
        $.post('searchbyid', { req: elementId }).done(function(data) {
          // Recuperer donnees
          let id = data[0].id;
          let alias = data[0].alias;
          let prenom = data[0].prenom;
          let nom = data[0].nom;
          let age = data[0].age;
          let sexe = data[0].sexe;
          let education = data[0].education;
          let sociale = data[0].sociale;
          let commentaire = data[0].commentaire;
          let typeP = data[0].typeP;
          let tabsTitle = alias;
          let textChangerProfil = 'Changer le type de profil';

          if (alias == '') {
            aliasB = `${prenom.charAt(0)}. ${nom}`;
          } else {
            aliasB = alias;
          }

          if (
            $('.ui-tabs-anchor')
              .text()
              .indexOf(aliasB) > -1
          ) {
            console.log(`${prenom.charAt(0)}. ${nom}`);
            console.log(alias);
          } else {
            // Creer un nouvel onglet
            //$("#my-tabs").append(`<li><a href="#tabsa-${elementId}">Profil - <b>${alias}</b></a></li>`)
            let sexeOpt1 = sexe === 'no' ? 'selected' : '';
            let sexeOpt2 = sexe === 'femme' ? 'selected' : '';
            let sexeOpt3 = sexe === 'homme' ? 'selected' : '';

            let educationOpt1 = education === 'no' ? 'selected' : '';
            let educationOpt2 = education === 'primaire' ? 'selected' : '';
            let educationOpt3 = education === 'secondaire-1' ? 'selected' : '';
            let educationOpt4 = education === 'secondaire-2' ? 'selected' : '';
            let educationOpt5 = education === 'superieur' ? 'selected' : '';

            let socialeOpt1 = sociale === 'no' ? 'selected' : '';
            let socialeOpt2 = sociale === 'populaire' ? 'selected' : '';
            let socialeOpt3 = sociale === 'moyenne' ? 'selected' : '';
            let socialeOpt4 = sociale === 'aisee' ? 'selected' : '';

            let champsNomPrenom = `<label for="name">Prénom</label>
          <input type="text" name="name" id="prenom-${id}" value="${prenom}" class="text ui-widget-content ui-corner-all">
          <label for="email">Nom</label>
          <input type="text" name="email" id="nom-${id}" value="${nom}" class="text ui-widget-content ui-corner-all">`;

            if (typeP == 'anonyme') {
              champsNomPrenom = '';
              textChangerProfil = 'Changer à profil connu';
            } else {
              textChangerProfil = 'Changer à profil anonyme';
            }

            if (age == '0' || age == '') {
              age = 'Non spécifié';
            }

            if (alias == '') {
              tabsTitle = `${prenom.charAt(0)}. ${nom}`;
            }

            let affichageResultatPers = '';

            // Champs personnalises
            $.ajax({
              type: 'POST',
              url: 'champs-personnalises-resultat',
              dataType: 'JSON',
              data: {
                id: id,
              },
              success: function(data1) {
                for (var i = 0; i < data1.length; i++) {
                  var obj = data1[i];
                  affichageResultatPers += `<input type="text" placeholder="Entrez votre données personnalisées" value="${obj.contenu}" class="ccc-element-${obj.idProfil} text ui-widget-content ui-corner-all">`;
                }
              },
              error: function(XMLHttpRequest, textStatus, errorThrown) {
                console.log('Error on #champspersonnalises');
              },
            });

            // Verifier existance textes
            let statsTextes = '';
            $.post('textesbyprofil', { id: id }).done(function(data) {
              statsTextes = String(data);

              // Ajouter la tabs
              let donneesTabs = `
          <div id="popup-search" style="overflow-y: scroll; height:500px;">
            <h2>Profil ${typeP}</h2>
            <hr>
            <button class="changer-profil" class="mt-2" id="cha-element-${id}">${textChangerProfil}</button>
            <input type="hidden" id="tpi-element-${id}" value="${typeP}">
            <h5 class="mt-4 mb-2"><b>Identification</b></h5>
            <label for="alias">Alias</label>
            <input type="text" name="alias" id="alias-${id}" value="${alias}" class="text ui-widget-content ui-corner-all">
            ${champsNomPrenom}
            <h5 class="mt-5 mb-2"><b>Profil Sociologique</b></h5>
            <label for="password">Age</label>
            <input type="text" name="password" id="age-${id}" value="${age}" placeholder="Non spécifié" class="agep-${typeP} text ui-widget-content ui-corner-all">
            <label for="sexe1">Sexe</label>
            <select name="sexe" id="sexe-${id}">
              <option value="no" ${sexeOpt1}>Non spécifié</option>
              <option value="femme" ${sexeOpt2}>Femme</option>
              <option value="homme" ${sexeOpt3}>Homme</option>
            </select>
            <label for="education1">Niveau d'éducation</label>
            <select name="education" id="education-${id}">
              <option value="no ${educationOpt1}">Non spécifié</option>
              <option value="primaire" ${educationOpt2}>Primaire</option>
              <option value="secondaire-1" ${educationOpt3}>Secondaire 1</option>
              <option value="secondaire-2" ${educationOpt4}>Secondaire 2</option>
              <option value="superieur" ${educationOpt5}>Supérieur</option>
            </select>
            <label for="sociale1">Classe sociale</label>
            <select name="sociale" id="sociale-${id}">
              <option value="no" ${socialeOpt1}>Non spécifiée</option>
              <option value="populaire" ${socialeOpt2}>Classe populaire</option>
              <option value="moyenne" ${socialeOpt3}>Classe moyenne</option>
              <option value="aisee" ${socialeOpt4}>Classe aisée</option>
            </select>
            <h5 class="mt-5 mb-2"><b>Informations complémentaires</b></h5>
            <label for="commentaire1">Commentaire</label>
            <textarea name="commentaire" id="commentaire-${id}" class="text ui-widget-content ui-corner-all" style="width: 100%;" cols="30" rows="10">${commentaire}</textarea>
            <input type="hidden" name="typep" id="typep-${id}" value="${typeP}">
            <!-- <div id="emc-element-${id}">${affichageResultatPers}</div> -->
            <!-- <button class="ajouter-champs" class="mt-2" id="ajc-element-${id}">Ajouter un nouveau champs</button> -->
            <button class="maj-button-texte" id="maj-element-${id}">Mettre à jour</button>
            <button class="supprimer-button-texte" id="sup-element-${id}">Supprimer le profil</button>
            <hr>
            <h3>Textes</h3>
            <table class="table">
            <thead>
              <tr>
                <th scope="col">Titre (version)</th>
                <th scope="col"># de mots</th>
                <th scope="col">Type de document</th>
                <th scope="col">Type d'écriture</th>
                <th scope="col">Segmentation</th>
                <th scope="col">Langues</th>
                <th scope="col">Thèmes</th>
                <th scope="col">Registre</th>
                <th scope="col">Audience</th>
                <th scope="col">Prétraitements</th>
                <th scope="col">Collection</th>
                <th scope="col">Dossier</th>
              </tr>
            </thead>
            <tbody>
              ${statsTextes}
            </tbody>
          </table>
          <h3 class="mt-3">Collections</h3>
            <table class="table">
            <thead>
              <tr>
                <th scope="col">Titre</th>
                <th scope="col"># de textes par l'auteur</th>
                <th scope="col"># de mots par l'auteur</th>
              </tr>
            </thead>
            <tbody>

            </tbody>
          </table>
          <h3 class="mt-3">Dossiers</h3>
          <table class="table">
          <thead>
            <tr>
              <th scope="col">Titre</th>
              <th scope="col"># de textes par l'auteur</th>
              <th scope="col"># de mots par l'auteur</th>
            </tr>
          </thead>
          <tbody>

          </tbody>
        </table>
        <h3 class="mt-3">Analyses</h3>
        <table class="table">
        <thead>
          <tr>
            <th scope="col">Titre</th>
            <th scope="col">Type d'analyse</th>
            <th scope="col">Ressources de l'auteur</th>
          </tr>
        </thead>
        <tbody>

        </tbody>
      </table>
      <h3 class="mt-3">Rapports</h3>
      <table class="table">
      <thead>
        <tr>
          <th scope="col">Titre</th>
          <th scope="col">Type de rapport</th>
        </tr>
      </thead>
      <tbody>

      </tbody>
    </table>
        </div>
          `;

              // Creer onglet
              addTab(donneesTabs, tabsTitle);
              $(`.ui-tabs-anchor:contains(${tabsTitle})`).click();
            });
          }
        });
      }
    });
  });

  // Tabs
  // Close icon: removing the tab on click
  tabs.on('click', 'span.ui-icon-close', function() {
    var panelId = $(this)
      .closest('li')
      .remove()
      .attr('aria-controls');
    $('#' + panelId).remove();
    tabs.tabs('refresh');
  });

  tabs.on('keyup', function(event) {
    if (event.altKey && event.keyCode === $.ui.keyCode.BACKSPACE) {
      var panelId = tabs
        .find('.ui-tabs-active')
        .remove()
        .attr('aria-controls');
      $('#' + panelId).remove();
      tabs.tabs('refresh');
    }
  });

  // Creer un texte
  dialogTexte2 = $('#dialog-form-importer-texte-2').dialog({
    autoOpen: false,
    height: 400,
    width: 450,
    modal: true,
  });

  // Clique import texte
  $('#btn-creer-nouveau-texte').click(function() {
    // Stockage des valeurs
    let nomTexte = $('#nom-fichier-b').val();
    let titreTexte = $('#titre-texte-b').val();
    let paterniteTexte = $('#paternite-b').val();
    let typeDocument1 = $('#type-document-1').val();
    let typeDocument2 = $('#type-document-2').val();
    let typeDocument3 = $('#type-document-3').val();
    let specificationTexte = $('#specification-texte-b').val();
    let typeEcritureTexte = $('#type-ecriture-b').val();
    let segmentationTexte = $('#segmentation-b').val();
    let langueTexte = $('#langue-b').val();
    let registreTexte = $('#registre-b').val();
    let commentaireTexte = $('#commentaire-b').val();

    // Transformation des valeurs
    switch (typeDocument1) {
      case 'bopt-1-1':
        typeDocument1 = 'Écriture personnelle';
        break;
      case 'bopt-1-2':
        typeDocument1 = 'Correspondance';
        break;
      case 'bopt-1-3':
        typeDocument1 = 'Messagerie';
        break;
      case 'bopt-1-4':
        typeDocument1 = 'Web et réseaux sociaux';
        break;
      case 'bopt-1-5':
        typeDocument1 = 'Presse';
        break;
      case 'bopt-1-6':
        typeDocument1 = 'Rédactions Scientifiques et Académiques';
        break;
      case 'bopt-1-7':
        typeDocument1 = 'Rédactions litéraires';
        break;
      case 'bopt-1-8':
        typeDocument1 = 'Rédactions judiciaires';
        break;
      case 'bopt-1-9':
        typeDocument1 = 'Documents à intêret judiciaire';
        break;
      case 'bopt-1-10':
        typeDocument1 = 'Autres';
        break;
    }

    // Verification et suite
    if (titreTexte == '' || paterniteTexte == 'no') {
      alert('Veuillez compléter les champs obligatoires avant de poursuivre.');
    } else {
      $.post('/importer-texte-bdd', {
        fichier: nomTexte,
        titre: titreTexte,
        paternite: paterniteTexte,
        typeDocument1: typeDocument1,
        typeDocument2: typeDocument2,
        typeDocument3: typeDocument3,
        specification: specificationTexte,
        typeEcriture: typeEcritureTexte,
        segmentation: segmentationTexte,
        langue: langueTexte,
        registre: registreTexte,
        commentaire: commentaireTexte,
      }).done(function(data) {
        //document.location.reload(true);
        dialogTexte.dialog('close');
        dialogTexte2.dialog('open');
      });
      /*
      $.ajax({
        url: 'importer-texte-bdd',
        method: "POST",
        data: {
          fichier: nomTexte,
          titre: titreTexte,
          paternite: paterniteTexte,
          typeDocument1: typeDocument1,
          typeDocument2: typeDocument2,
          typeDocument3: typeDocument3,
          specification: specificationTexte,
          typeEcriture: typeEcritureTexte,
          segmentation: segmentationTexte,
          langue: langueTexte,
          registre: registreTexte,
          commentaire: commentaireTexte
        },
        success: function(result){
          dialogTexte.dialog("close");
          dialogTexte2.dialog("open");
        },
        error: function(er){alert("Erreur inconnue. Le texte n'a pu être sauvegardé.")}
      });
      */
    }
  });

  $('#btn-creer-nouveau-texte-2').click(function() {
    // Recuperer bouton radio
    let boutonRadio = $("input[name='profil_texte']:checked").val();
    alert(boutonRadio);

    // Association
    if (boutonRadio == 'associer') {
    }

    if (boutonRadio == 'connu') {
    }

    if (boutonRadio == 'anonyme') {
    }

    //document.location.reload(true);
  });

  function importerLeTexte(form) {
    $.ajax({
      url: 'importer-texte',
      method: 'POST',
      dataType: 'JSON',
      data: form,
      processData: false,
      contentType: false,
      success: function(result) {
        $('#btn-importer-texte').addClass('d-none');
        $('#affichage-suite-texte').removeClass('d-none');
        let filename = $('#importer-texte')
          .val()
          .replace(/C:\\fakepath\\/i, '');
        $('#titre-texte-b').val(filename);
        $('#texte-chargement-b').text('');
        $('#langue-b').val(result.langue);
        $('#nom-fichier-b').val(result.name);
      },
      error: function(er) {
        alert("Erreur inconnu. Le fichier n'a pu être chargé.");
      },
    });
  }

  $('#btn-importer-texte').click(function() {
    $('#btn-importer-texte').attr('disabled', true);
    console.log('Importation...');
    let form = new FormData($('#uploadForm')[0]);
    $('#texte-chargement-b').text(
      "Le fichier est en train d'être importé et analysé. Cela peut prendre environ une minute...",
    );
    $('#importer-texte').attr('disabled', true);
    $.ajax({
      url: 'verifier-texte',
      method: 'POST',
      dataType: 'html',
      data: form,
      processData: false,
      contentType: false,
      success: function(result) {
        console.log(result);
        importerLeTexte(form);
      },
      error: function(err) {
        $('#importer-texte').attr('disabled', false);
        $('#btn-importer-texte').attr('disabled', false);
        $('#importer-texte').val('');
        $('#texte-chargement-b').text('');
        alert("Une erreur s'est produite : " + err.responseText);
      },
    });
  });

  $('#parametres-deconnexion').click(function() {
    window.open('/deconnexion', '_self');
  });

  // Maj informations
  var infoElement = 0;
  var tid = setTimeout(repeatMe, 2000);
  function repeatMe() {
    infoElement = 0;
    tid = setTimeout(repeatMe, 2000); // repeat myself
  }

  // Texte et type de document
  $('#type-document-1').change(function() {
    // Suppression par defaut
    $('#type-document-2 option').remove();
    $('#type-document-2').addClass('d-none');
    $('#type-document-3').addClass('d-none');

    let valTypeDoc1 = $('#type-document-1').val();

    // Opt1
    if (valTypeDoc1 == 'bopt-1-1') {
      // Suppression par defaut
      $('#type-document-2').removeClass('d-none');

      // Ajout elements
      $('#type-document-2').append(
        `<option value="Journal / Entrée d'un journal">Journal / Entrée d'un journal</option>`,
      );
      $('#type-document-2').append(
        `<option value="Notes personnelles">Notes personnelles</option>`,
      );
      $('#type-document-2').append(`<option value="Autre">Autre</option>`);
    }

    // Opt2
    if (valTypeDoc1 == 'bopt-1-2') {
      // Suppression par defaut
      $('#type-document-2').removeClass('d-none');

      // Ajout elements
      $('#type-document-2').append(`<option value="Note">Note</option>`);
      $('#type-document-2').append(
        `<option value="Carte postale">Carte postale</option>`,
      );
      $('#type-document-2').append(`<option value="Lettre">Lettre</option>`);
      $('#type-document-2').append(`<option value="Email">Email</option>`);
      $('#type-document-2').append(`<option value="Autre">Autre</option>`);
    }

    // Opt3
    if (valTypeDoc1 == 'bopt-1-3') {
      // Suppression par defaut
      $('#type-document-2').removeClass('d-none');

      // Ajout elements
      $('#type-document-2').append(`<option value="SMS">SMS</option>`);
      $('#type-document-2').append(
        `<option value="Messagerie instantanée">Messagerie instantanée</option>`,
      );
      $('#type-document-2').append(`<option value="Autre">Autre</option>`);
    }

    // Opt4
    if (valTypeDoc1 == 'bopt-1-4') {
      // Suppression par defaut
      $('#type-document-2').removeClass('d-none');

      // Ajout elements
      $('#type-document-2').append(`<option value="Tweet">Tweet</option>`);
      $('#type-document-2').append(
        `<option value="Publication sur forum">Publication sur forum</option>`,
      );
      $('#type-document-2').append(
        `<option value="Publication sur Facebook">Publication sur Facebook</option>`,
      );
      $('#type-document-2').append(
        `<option value="Billet de blog">Billet de blog</option>`,
      );
      $('#type-document-2').append(
        `<option value="Commentaires et interactions">Commentaires et interactions</option>`,
      );
      $('#type-document-2').append(`<option value="Autre">Autre</option>`);
    }

    // Opt5
    if (valTypeDoc1 == 'bopt-1-5') {
      // Suppression par defaut
      $('#type-document-2').removeClass('d-none');

      // Ajout elements
      $('#type-document-2').append(`<option value="Article">Article</option>`);
      $('#type-document-2').append(`<option value="Journal">Journal</option>`);
      $('#type-document-2').append(`<option value="Revue">Revue</option>`);
      $('#type-document-2').append(`<option value="Autre">Autre</option>`);
    }

    // Opt6
    if (valTypeDoc1 == 'bopt-1-6') {
      // Suppression par defaut
      $('#type-document-2').removeClass('d-none');

      // Ajout elements
      $('#type-document-2').append(`<option value="Article">Article</option>`);
      $('#type-document-2').append(`<option value="Essai">Essai</option>`);
      $('#type-document-2').append(
        `<option value="Dissértation">Dissértation</option>`,
      );
      $('#type-document-2').append(`<option value="Memoire">Memoire</option>`);
      $('#type-document-2').append(`<option value="Rapport">Rapport</option>`);
      $('#type-document-2').append(
        `<option value="Revue Scientifique">Revue Scientifique</option>`,
      );
      $('#type-document-2').append(
        `<option value="Livre d'instruction">Livre d'instruction</option>`,
      );
      $('#type-document-2').append(`<option value="Autre">Autre</option>`);
    }

    // Opt7
    if (valTypeDoc1 == 'bopt-1-7') {
      // Suppression par defaut
      $('#type-document-2').removeClass('d-none');

      // Ajout elements
      $('#type-document-2').append(`<option value="Poésie">Poésie</option>`);
      $('#type-document-2').append(`<option value="Roman">Roman</option>`);
      $('#type-document-2').append(
        `<option value="Pièce de théatre">Pièce de théatre</option>`,
      );
      $('#type-document-2').append(`<option value="Conte">Conte</option>`);
      $('#type-document-2').append(`<option value="Fable">Fable</option>`);
      $('#type-document-2').append(
        `<option value="Autobiographie ou mémoire">Autobiographie ou mémoire</option>`,
      );
      $('#type-document-2').append(
        `<option value="Biographie">Biographie</option>`,
      );
      $('#type-document-2').append(`<option value="Autre">Autre</option>`);
    }

    // Opt8
    if (valTypeDoc1 == 'bopt-1-8') {
      // Suppression par defaut
      $('#type-document-2').removeClass('d-none');

      // Ajout elements
      $('#type-document-2').append(`<option value="Rapport">Rapport</option>`);
      $('#type-document-2').append(
        `<option value="Témoignage">Témoignage</option>`,
      );
      $('#type-document-2').append(
        `<option value="Lettre d'aveu">Lettre d'aveu</option>`,
      );
      $('#type-document-2').append(`<option value="Autre">Autre</option>`);
    }

    // Opt9
    if (valTypeDoc1 == 'bopt-1-9') {
      // Suppression par defaut
      $('#type-document-2').removeClass('d-none');

      // Ajout elements
      $('#type-document-2').append(
        `<option value="Lettre d'adieu">Lettre d'adieu</option>`,
      );
      $('#type-document-2').append(
        `<option value="Lettre de ménce">Lettre de ménce</option>`,
      );
      $('#type-document-2').append(
        `<option value="Demande de rançon">Demande de rançon</option>`,
      );
      $('#type-document-2').append(
        `<option value="Testament">Testament</option>`,
      );
      $('#type-document-2').append(`<option value="Autre">Autre</option>`);
    }

    // Opt9
    if (valTypeDoc1 == 'bopt-1-10') {
      // Suppression par defaut
      $('#type-document-3').removeClass('d-none');
    }
  });

  $('#type-document-2').change(function() {
    let valTypeDoc2 = $('#type-document-2').val();
    if (valTypeDoc2 == 'Autre') {
      $('#type-document-3').removeClass('d-none');
    } else {
      $('#type-document-3').addClass('d-none');
    }
  });

  $('#tabs').bind('DOMSubtreeModified', function() {
    // Supprimer
    $('.supprimer-button-texte').click(function() {
      if (infoElement == 0) {
        infoElement++;
        let idElement = $(this).attr('id');
        idElement = idElement.substring(12);

        if (
          confirm('Voulez-vous vraiment supprimer ce profil définitivement ?')
        ) {
          $.post('/supprimer-profil', { id: idElement }).done(function(data) {
            document.location.reload(true);
            infoElement = 0;
            //document.location.reload(true);
          });
        }
      }
    });


    // Supprimer association
    $('.delete-association').click(function() {
      if (infoElement == 0) {
        infoElement++;
        let idElement = $(this).attr('id');
        idElement = idElement.substring(12);


        if (
          confirm('Voulez-vous vraiment supprimer cette association ?')
        ) {
          $.post('/supprimer-association', { id: idElement }).done(function(data) {
            $(`.ui-icon-close`).click();
            getDossier(data);
            //document.location.reload(true);
            infoElement = 0;
            //document.location.reload(true);
          });
        }
      }
    });

    // Supprimer Texte
    $('.supprimer-texte').click(function() {
      if (infoElement == 0) {
        infoElement++;
        let idElement = $(this).attr('id');
        idElement = idElement.substring(12);

        if (
          confirm(
            'Voulez-vous vraiment supprimer ce texte et ses analyses définitivement ?',
          )
        ) {
          $.post('/supprimer-texte', { id: idElement }).done(function(data) {
            document.location.reload(true);
            infoElement = 0;
            //document.location.reload(true);
          });
        }
      }
    });

    // Supprimer Dossier
    $('.supprimer-dossier').click(function() {
      if (infoElement == 0) {
        infoElement++;
        let idElement = $(this).attr('id');
        idElement = idElement.substring(12);

        if (
          confirm('Voulez-vous vraiment supprimer ce dossier définitivement ?')
        ) {
          $.post('/supprimer-dossier', { id: idElement }).done(function(data) {
            document.location.reload(true);
            infoElement = 0;
            //document.location.reload(true);
          });
        }
      }
    });

    // Supprimer Dossier
    $('.imprimer-dossier').click(function() {
      if (infoElement == 0) {
        infoElement++;
        let idElement = $(this).attr('id');
        idElement = idElement.substring(12);

        // Ouvrir pour impression
        let imprimer = window.open(`/imprimer-dossier/${idElement}`, '_blank');
        imprimer.document.close(); //missing code
        imprimer.focus();
        imprimer.print(); 
        setTimeout(function(){ imprimer.close();}, 1000);
      }
    });

    // Supprimer Collection
    $('.supprimer-collection').click(function() {
      if (infoElement == 0) {
        infoElement++;
        let idElement = $(this).attr('id');
        idElement = idElement.substring(12);

        if (
          confirm(
            'Voulez-vous vraiment supprimer cette collection définitivement ?',
          )
        ) {
          $.post('/supprimer-collection', { id: idElement }).done(function(
            data,
          ) {
            document.location.reload(true);
            infoElement = 0;
            //document.location.reload(true);
          });
        }
      }
    });

    // Associer profil / texte
    $('.associer-tabs').click(function() {
      if (infoElement == 0) {
        infoElement++;
        let idElement = $(this).attr('id');
        idElement = idElement.substring(12);
        $('#id-element-texte').val(idElement);
        dialogAssociationProfil.dialog('open');
      }
    });

    // Associer dossiers / profils
    $('.associer-tabs-dprofil').click(function() {
      if (infoElement == 0) {
        infoElement++;
        let idElement = $(this).attr('id');
        idElement = idElement.substring(12);
        $('#id-element-profild').val(idElement);
        dialogDossiersAssoc.dialog('open');
      }
    });

    // Associer dossiers / textes
    $('.associer-tabs-dtextes').click(function() {
      if (infoElement == 0) {
        infoElement++;
        let idElement = $(this).attr('id');
        idElement = idElement.substring(12);
        $('#id-element-texted').val(idElement);
        dialogDossiersTextes.dialog('open');
      }
    });

    // Associer dossiers / collections
    $('.associer-tabs-dcollection').click(function() {
      if (infoElement == 0) {
        infoElement++;
        let idElement = $(this).attr('id');
        idElement = idElement.substring(12);
        $('#id-element-texted').val(idElement);
        dialogDossiersCollections.dialog('open');
      }
    });

    // Associer dossiers / analyses
    $('.associer-tabs-danalyse').click(function() {
      if (infoElement == 0) {
        infoElement++;
        let idElement = $(this).attr('id');
        idElement = idElement.substring(12);
        $('#id-element-texted').val(idElement);
        dialogDossiersAnalyses.dialog('open');
      }
    });

    // Associer dossiers / rapports
    $('.associer-tabs-drapports').click(function() {
      if (infoElement == 0) {
        infoElement++;
        let idElement = $(this).attr('id');
        idElement = idElement.substring(12);
        $('#id-element-texted').val(idElement);
        dialogDossiersRapports.dialog('open');
      }
    });

    $('.ajouter-champs').click(function() {
      if (infoElement == 0) {
        infoElement++;
        let idElement = $(this).attr('id');
        idElement = idElement.substring(12);

        // Ajout du champs
        $('#emc-element-' + idElement).append(`
        <input type="text" placeholder="Entrez votre données personnalisées" class="ccc-element-${idElement} text ui-widget-content ui-corner-all">
        `);
      }
    });

    // Changer type profil
    $('.changer-profil').click(function() {
      if (infoElement == 0) {
        infoElement++;
        let idElement = $(this).attr('id');
        idElement = idElement.substring(12);
        let typeProfil = $('#tpi-element-' + idElement).val();
        console.log('Valeur : ' + typeProfil);

        // Sur de changer le type de profil
        if (confirm('Êtes-vous sûr de vouloir changer le type de profil ?')) {
          $.ajax({
            type: 'POST',
            url: 'changer-type-profil',
            dataType: 'html',
            data: {
              id: idElement,
              type: typeProfil,
            },
            success: function(data) {
              alert('Le type de profil a été changé');
              document.location.reload(true);
            },
            error: function(XMLHttpRequest, textStatus, errorThrown) {
              alert('Error on .changer-profil.');
            },
          });
        }
      }
    });

    // Ouvrir analyse
    $('.ouvrir-analyse').click(function() {
      if (infoElement == 0) {
        infoElement++;
        let idElement = $(this).attr('id');
        idElement = idElement.substring(12);

        let donneesTabs = `
        <div id="popup-search" style="overflow-y: scroll; height:500px;">
        <iframe
            height="500"
            width="100%"
            frameBorder="0"
            src="/static/textes/${idElement}_analyse.html">
        </iframe>
        </div>
        `;

        // Creer onglet
        let titreOnglet = 'Analyse-' + Date.now();
        addTab(donneesTabs, titreOnglet);
        $(`.ui-tabs-anchor:contains(${titreOnglet})`).click();
      }
    });

    // MAJ
    $('.maj-texte').click(function() {
      if (infoElement == 0) {
        infoElement++;
        let idElement = $(this).attr('id');
        idElement = idElement.substring(12);
        console.log('Id element : ' + idElement);

        // Mise a jour
        let alias = $('#titretexteb-' + idElement).val();
        let paternite = $('#paterniteb-' + idElement).val();
        let specification = $('#specificationtexteb-' + idElement).val();
        let typeEcriture = $('#typeecritureb-' + idElement).val();
        let segmentation = $('#segmentationb-' + idElement).val();
        let registre = $('#registreb-' + idElement).val();
        let commentaire = $('#commentaireb-' + idElement).val();

        // Modification des informations du profil
        $.post('/modifier-texte', {
          id: idElement,
          alias: alias,
          paternite: paternite,
          specification: specification,
          typeEcriture: typeEcriture,
          segmentation: segmentation,
          registre: registre,
          commentaire: commentaire,
        }).done(function(data) {
          alert('Les informations ont bien été mises à jour.');
          $('li.ui-tabs-active > a').html(alias);
          infoElement = 0;
          //document.location.reload(true);
        });
      }
    });

    // MAJ
    $('.sauvegarder-dossier').click(function() {
      if (infoElement == 0) {
        infoElement++;
        let idElement = $(this).attr('id');
        idElement = idElement.substring(12);
        console.log('Id element : ' + idElement);

        // Mise a jour
        let commentaire = $('#commentaire-b-' + idElement).val();

        // Modification des informations du profil
        $.post('/modifier-dossier', {
          id: idElement,
          commentaire: commentaire,
        }).done(function(data) {
          alert('Les informations ont bien été mises à jour.');
          //$('li.ui-tabs-active > a').html(alias);
          infoElement = 0;
          //document.location.reload(true);
        });
      }
    });

    // MAJ
    $('.maj-button-texte').click(function() {
      if (infoElement == 0) {
        infoElement++;
        let idElement = $(this).attr('id');
        idElement = idElement.substring(12);
        console.log('Id element : ' + idElement);

        // Mise a jour
        let alias = $('#alias-' + idElement).val();
        let prenom = $('#prenom-' + idElement).val();
        let nom = $('#nom-' + idElement).val();
        let age = $('#age-' + idElement).val();
        let sexe = $('#sexe-' + idElement).val();
        let education = $('#education-' + idElement).val();
        let sociale = $('#sociale-' + idElement).val();
        let commentaire = $('#commentaire-' + idElement).val();
        let typep = $('#typep-' + idElement).val();

        let verifAge = false;
        if (age != '') {
          if ($('#age-' + idElement).hasClass('agep-connu')) {
            console.log('profil connu...');
            let regex = /^(([1-9])|([1-9][0-9])|([1][0-1][0-9])|120)$/;
            if (!regex.test(age)) {
              verifAge = true;
            }
            if (age == 'Non spécifié') {
              verifAge = false;
            }
          } else {
            // Si profil anonyme
            console.log('profil anonyme...');
            let regexAge = /^[1-9][0-9][-](([1-9])|([1-9][0-9])|([1][0-1][0-9])|120)$/;
            let wordsAge = age.split('-');
            let age1 = Number(wordsAge[0]);
            let age2 = Number(wordsAge[1]);
            if (!regexAge.test(age) || age1 > age2) {
              verifAge = true;
            }
            if (age == 'Non spécifié') {
              verifAge = false;
            }
          }
        }

        if (age == 'Non spécifié') {
          verifAge = false;
        }

        if (typep == 'anonyme') {
          prenom = ' ';
          nom = ' ';
        }
        if (
          (typep == 'anonyme' && alias == '') ||
          (typep == 'anonyme' && verifAge)
        ) {
          alert(
            "Une erreur s'est produite. Vous devez compléter au minimum l'alias. Vérifiez que l'âge soit spécifié entre une intervalle (ex: 20-30).",
          );
        } else {
          if ((typep == 'connu' && (prenom == '' || nom == '')) || verifAge) {
            alert(
              "Une erreur s'est produite. Vous devez compléter au minimum le prénom et le nom. Vérfiez que l'âge soit spécifié correctement.",
            );
          } else {
            // Ajout des champs personnalise
            $.post('/supprimer-champs-personnalises', { id: idElement }).done(
              function(data) {
                //document.location.reload(true);
              },
            );
            $('.ccc-element-' + idElement).each(function(index) {
              let myContent = $(this).val();
              if (myContent != '') {
                $.post('/ajouter-champs-personnalises', {
                  id: idElement,
                  contenu: myContent,
                }).done(function(data) {
                  //document.location.reload(true);
                });
              }
            });

            // Modification des informations du profil
            $.post('/modifier-profil', {
              id: idElement,
              alias: alias,
              prenom: prenom,
              nom: nom,
              age: age,
              sexe: sexe,
              education: education,
              sociale: sociale,
              commentaire: commentaire,
            }).done(function(data) {
              alert('Les informations ont bien été mises à jour.');
              $('li.ui-tabs-active > a').html(
                alias ? alias : `${prenom.charAt(0)}. ${nom}`,
              );
              infoElement = 0;
              //document.location.reload(true);
            });
          }
        }
      }
    });
  });

  // Ajouter des champs dans les formulaires
  $('.btn-ajout-champs').click(function() {
    // Ajout du champs
    $('.champs-persos').append(`
      <input type="text" placeholder="Entrez votre données personnalisées" class="ccc-element text ui-widget-content ui-corner-all">
      `);
  });

  // Intercepter la fermeture d'une fenetre
  $('body').on('dialogclose', function(event) {
    // Actualiser profil connu
    $('.champs-persos').html('');

    // Actualiser profil anonyme

    // Actualiser texte
    $('#importer-texte').attr('disabled', false);
    $('#btn-importer-texte').removeClass('d-none');
    $('#btn-importer-texte').attr('disabled', false);
    $('#importer-texte').val('');
    $('#affichage-suite-texte').addClass('d-none');
    $('#texte-chargement-b').text('');
    $('#titre-texte-b').val('');
    $('#paternite-b').val('no');
    $('#type-document-1').val('Non spécifié');
    $('#type-document-2').addClass('d-none');
    $('#type-document-3').addClass('d-none');
    $('#specification-texte-b').val('');
    $('#type-ecriture-b').val('Non spécifié');
    $('#segmentation-b').val('Non spécifiée');
    $('#langue-b').val('');
    $('#registre-b').val('Non spécifié');
    $('#commentaire-b').val('');
  });

  // Changement de la langue
  $('#check-langue').click(function() {
    if ($('#langue-b').is(':disabled')) {
      if (
        confirm(
          'Êtes-vous sûr de vouloir changer la langue par défaut du texte ?',
        )
      ) {
        $('#langue-b').prop('disabled', false);
        $('#btn-change-de-langue').addClass('d-none');
      }
    }
  });


  // -- DOSSIERS --

  // Fenetre de dialogue Dossiers
  dialogDossiers = $('#dialog-dossiers').dialog({
    autoOpen: false,
    height: 400,
    width: 450,
    modal: true,
  });

  // Au clic du Dossiers
  $('#creer-dossier').click(function() {
    dialogDossiers.dialog('open');
  });

  // Creer un nouveau dossier
  $('#btn-creer-nouveau-dossier').click(function() {
    let titreDossier = $('#titre-dossier').val();
    if (titreDossier == '') {
      alert('Erreur. Vous devez donner un titre à votre dossier.');
    } else {
      $.ajax({
        type: 'POST',
        url: 'creer-dossier',
        dataType: 'html',
        data: {
          titre: titreDossier,
        },
        success: function(data1) {
          alert(data1);
          dialogDossiers.dialog('close');
          $('#titre-dossier').val("");
          $('#recherche').keyup();
        },
        error: function(err) {
          alert("Une erreur s'est produite : " + err.responseText);
        },
      });
    }
  });

  // Fonction 
  function getDossier(paramsId) {

          elementId = paramsId;
          console.log('ID : ' + elementId);
  
    
            // Recuperer donnees
            $.post('search-dossier', { req: elementId }).done(function(data) {
              // Recuperer donnees
              let id = data[0].id;
              let titre = data[0].titre;
              let commentaire = data[0].commentaire;
    
              // Verifier s'il existe dans les tabs
              if (
                $('.ui-tabs-anchor')
                  .text()
                  .indexOf(titre) > -1
              ) {
              } else {
              $.post('resultassocoiation', { id: id, type: "Dossier", get: "Profil" }).done(function(data) {
                statsProfils = String(data);
                $.post('resultassocoiation', { id: id, type: "Dossier", get: "Texte" }).done(function(data) {
                   statsTextes = String(data); 
                   let donneesTabs = `
                   <div id="mypop-${id}" style="overflow-y: scroll; height:500px;">
                   <h2>Dossier ${titre}</h2>
                   <hr>
                   <div class="row mt-3">
                   <div class="col-md-12">
                   <h3 class="mt-3">Profils</h3>
                   <table class="table">
                   <thead>
                     <tr>
                       <th scope="col">Type</th>
                       <th scope="col">Alias</th>
                       <th scope="col">Prénom NOM</th>
                     </tr>
                   </thead>
                   <tbody>
                     ${statsProfils}
                   </tbody>
                 </table>
                 <button class="associer-tabs-dprofil mb-3" id="dpr-element-${id}">Ajouter un profil</button>
                   <h3 class="mt-3">Textes</h3>
                   <table class="table">
                   <thead>
                     <tr>
                       <th scope="col">Titre</th>
                       <th scope="col"># Versions</th>
                     </tr>
                   </thead>
                   <tbody>
                     ${statsTextes}
                   </tbody>
                 </table>
                 <button class="associer-tabs-dtextes mb-3" id="dte-element-${id}">Ajouter un texte</button>
                   <h3 class="mt-3">Collections</h3>
                     <table class="table">
                     <thead>
                       <tr>
                         <th scope="col">Titre</th>
                         <th scope="col"># de textes par l'auteur</th>
                         <th scope="col"># de mots par l'auteur</th>
                       </tr>
                     </thead>
                     <tbody>
         
                     </tbody>
                   </table>
                   <button class="associer-tabs-dcollection mb-3" id="dte-element-${id}">Ajouter une collection</button>
                 <h3 class="mt-3">Analyses</h3>
                 <table class="table">
                 <thead>
                   <tr>
                     <th scope="col">Titre</th>
                     <th scope="col">Type d'analyse</th>
                     <th scope="col">Ressources de l'auteur</th>
                   </tr>
                 </thead>
                 <tbody>
         
                 </tbody>
               </table>
               <button class="associer-tabs-danalyse mb-3" id="dte-element-${id}">Ajouter une analyse</button>
               <h3 class="mt-3">Rapports</h3>
               <table class="table">
               <thead>
                 <tr>
                   <th scope="col">Titre</th>
                   <th scope="col">Type de rapport</th>
                 </tr>
               </thead>
               <tbody>
         
               </tbody>
             </table>
             <button class="associer-tabs-drapports mb-3" id="dte-element-${id}">Ajouter un rapport</button>
                   <fieldset>
                   <input type="text" name="autre" id="type-document-3" value="${titre}" class="text ui-widget-content ui-corner-all mt-3 d-none" disabled>
         
                   <label class="mt-4" for="commentaire-b-${id}">Commentaire</label>
                   <textarea name="commentaire" id="commentaire-b-${id}" class="text ui-widget-content ui-corner-all" style="width: 100%;" cols="30" rows="10">${commentaire}</textarea>
                   <!-- Allow form submission with keyboard without duplicating the dialog button -->
                   <button class="sauvegarder-dossier" id="sav-element-${id}">Sauvegarder le dossier</button>
                   <button class="supprimer-dossier" id="sup-element-${id}">Supprimer le dossier</button>
                   <button class="imprimer-dossier" id="imp-element-${id}">Imprimer le dossier</button>
               </fieldset>
               </div>
                   </div>
                   </div>
                   `;
         
                     // Creer onglet
                     addTab(donneesTabs, titre);
                     $(`.ui-tabs-anchor:contains(${titre})`).click();
                });
              });
              }
            });
      }
  // Algo affichage fenetre
  $('#search-result').bind('DOMSubtreeModified', function() {
    $('.sresuldossi').click(function() {
          // Recuperer l'id
          console.log('Vpoint = ' + vPoint);
          console.log('+++');
          var elementId = $(this).attr('id');
          var words = elementId.split('-');
          elementId = words[1];

          if (vPoint != elementId) {
            // Verif
            vPoint = elementId;
            getDossier(elementId);
          }

    });
  });

  // -- /DOSSIERS
});
