
Split(['#split-board', '#split-tree'], {
  minSize: [400, 300],
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

// Set board positions index and stones
 $(".board-pos").each(function(index) {
  $(this).data("index", index);
  if (index in placedStones) {
    placeStone($(this), placedStones[index]);
  }
})

function placeStone(element, color) {
  element.append("<img class='stone' data-color='" + color + "' src='/static/images/" + color + ".png' alt=''>");
}
