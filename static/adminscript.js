$(document).ready(function () {
  $("#theForm").on("submit", function (event) {
    var name = $("#username").val(),
        auth = $('#password').val() === 'password' && name === 'jennifer',
        msgBox = $("#welcome"),
        origMsg = msgBox.html(),
        newMsg = 'Welcome. <span>' + name +'.' +'</span>',
        message = name !== '' && auth ? newMsg : origMsg;
  
    msgBox.html(message);
    if (auth) {
      $('#flippr .flipper').addClass('logged-in');
    }
  
    event.preventDefault();
  });
  
});



/* 

var app = {

  shipping : 5.00,
  products : [
      {
        "name" : "bart1",
        "password" : "hallo",
        "img" : "http://willemsol.nl/codepenimg/FlipImg3.png"
      },
      {
        "name" : "bart2",
        "password" : "hallo",
        "img" : "http://willemsol.nl/codepenimg/FlipImg3.png"
      },
      {
        "name" : "bart3",
        "password" : "hallo",
        "img" : "http://willemsol.nl/codepenimg/FlipImg3.png"
      },
      {
        "name" : "bart4",
        "password" : "hallo",
        "img" : "http://willemsol.nl/codepenimg/FlipImg3.png" 
              }
    ];

*/