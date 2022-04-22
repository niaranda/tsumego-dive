
Split(['#split-board', '#split-tree'], {
  minSize: [800, 300],
  gutterSize: 4,
  snapOffset: 0,
  dragInterval: 2,
  sizes: [70, 30],
  onDragStart: function(sizes) {
    $(".arrow").remove();
  }
})

$("nav").css("width", "90%");
$("nav").css("min-width", "1000px");

$("#content-div").css("width", "90%");
$("#content-div").css("min-width", "1000px");
