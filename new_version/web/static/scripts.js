var num = 2; // adds 2 fields at a time

var createInputs = function () {
  // $("#ip_div").append('<form id="form"></form>');
  for (var i = 0; i < num; i++) {
    if (i % 2 == 0) {
      $("#data_form").append('<input type="text"></input>');
    }
    else {
      $("#data_form").append(' = <input type="text"></input> <br>');
    }
  }
};

$("#btn").click(function () {
  createInputs();
  //create unique ID for each input
  $("#data_form")
    .find("input")
    .each(function (i) {
      $(this).attr("name", "num" + i);

      if (i % 2 == 0) { $(this).attr("placeholder", "type - " + i); }
      else            { 
        s = i-1;
        $(this).attr("placeholder", "value - " + s); }
    });
});
// var num = 2; // adds 2 fields at a time

// var createInputs = function () {
//   $("#ip_div").append('<form id="form"></form>');
//   for (var i = 0; i < num; i++) {
//     if (i % 2 == 0) {
//       $("#form").append('<input type="text"></input>');
//     }
//     else {
//       $("#form").append(' = <input type="text"></input> <br>');
//     }
//   }
// };

// $("#btn").click(function () {
//   createInputs();
//   //create unique ID for each input
//   $("#form")
//     .find("input")
//     .each(function (i) {
//       $(this).attr("id", "num" + i);

//       if (i % 2 == 0) { $(this).attr("placeholder", "type - " + i); }
//       else            { 
//         s = i-1;
//         $(this).attr("placeholder", "value - " + s); }
//     });
// });