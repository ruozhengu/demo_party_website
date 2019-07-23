//DRILL DOWN CONTENT TOGGLE
$(".drilldown").hide();

$("#drilldown-trigger").click(function(){
  $(".drilldown").slideToggle('fast');
});

//DRILLDOWN VIEWS & TRIGGERS
$('#view-content').hide();
$('#view-proofs').hide();
$('#view-completed').hide();
$('#view-activity').hide();
$('#view-notes').hide();

$("#trigger-notes").click(function(){
  $('#view-billing').hide();
  $('#view-content').hide();
  $('#view-proofs').hide();
  $('#view-completed').hide();
  $('#view-activity').hide();
  $("#view-notes").fadeIn('fast');
});

$("#trigger-billing").click(function(){
  $('#view-content').hide();
  $('#view-proofs').hide();
  $('#view-completed').hide();
  $('#view-activity').hide();
  $('#view-notes').hide();
  $("#view-billing").fadeIn('fast');
});
$("#trigger-content").click(function(){
  $('#view-billing').hide();
  $('#view-proofs').hide();
  $('#view-completed').hide();
  $('#view-activity').hide();
  $('#view-notes').hide();
  $("#view-content").fadeIn('fast');
});
$("#trigger-proofs").click(function(){
  $('#view-billing').hide();
  $('#view-content').hide();
  $('#view-completed').hide();
  $('#view-activity').hide();
  $('#view-notes').hide();
  $("#view-proofs").fadeIn('fast');
});
$("#trigger-completed").click(function(){
  $('#view-billing').hide();
  $('#view-content').hide();
  $('#view-proofs').hide();
  $('#view-notes').hide();
  $("#view-completed").fadeIn('fast');
});
$("#trigger-activity").click(function(){
  $('#view-billing').hide();
  $('#view-content').hide();
  $('#view-proofs').hide();
  $('#view-notes').hide();
  $("#view-activity").fadeIn('fast');
});

//DRILLDOWN TOGGLE BUTTON STATES
$('.btn-group').on('click', '.btn', function() {
  $(this).addClass('btn-primary').siblings().removeClass('btn-primary').addClass('btn-primary-ghost');
});

//TURN OFF 'NUOVO' CLASS ON NOTIFY LI ROW
$("#allRead").click(function(){
  $("li").removeClass("nuovo");
});

//TOOLTIP INFO FOR IMAGES IN 'CONTENT' AREA
// $('[data-toggle="tooltip"]').tooltip();

//ADDING SELECTED '#SELEZIONATO' TO TAGGED/APPROVED IMAGES, THIS ISN'T WORKING THAT GREAT AT THE MOMENT
//NEED A WAY TO TARGET THE NEXT ELEMENT FROM THE DROPDOWN: A > IMG TO TARGET AND ADD '#SELEZIONATO'
$('a[href="#agent_headshot"]').click(function() {
  $('a').find('img').attr("id","selezionato");
  alert('Image tagged as Headshot.');
});


//SENDING PROOFS TO PORTAL

$('#feedback').hide(); //this is hidden UNLESS it's feedback provided back from the agent, via the portal.

$("#send-proof-yes").click(function() {
  $("#sent-proof").hide();
});

$("#send-proof-no").click(function() {
  $('#feedback').slideDown('fast');
});

$("#submit-to-designer").click(function() {
  $('#sent-proof').hide();
});





//TAKEN FROM SAME DRAG AND DROP BEHAVIORAL APPROACH FROM CLIENT PORTAL
+ function($) {
    'use strict';

    // UPLOAD CLASS DEFINITION
    // ======================

    var dropZone = document.getElementById('drop-zone');
    var uploadForm = document.getElementById('js-upload-form');

    var startUpload = function(files) {
        console.log(files)
    }

    uploadForm.addEventListener('submit', function(e) {
        var uploadFiles = document.getElementById('js-upload-files').files;
        e.preventDefault()

        startUpload(uploadFiles)
    })

    dropZone.ondrop = function(e) {
        e.preventDefault();
        this.className = 'upload-drop-zone';

        startUpload(e.dataTransfer.files)
    }

    dropZone.ondragover = function() {
        this.className = 'upload-drop-zone drop';
        return false;
    }

    dropZone.ondragleave = function() {
        this.className = 'upload-drop-zone';
        return false;
    }

}(jQuery);
