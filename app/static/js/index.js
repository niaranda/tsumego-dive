
let insertColor;
let firstStoneColor;
let placedStones = {};

// Insertion color
$("#insert-black").click(function() {
  if (insertColor === "black") {
    insertColor = undefined;
    $(this).removeClass("selected");
    return;
  }

  if (insertColor !== undefined) {
    $(".insertion > .stone-btn").removeClass("selected");
  }

  insertColor = "black";
  $(this).addClass("selected");
})

$("#insert-white").click(function() {
  if (insertColor === "white") {
    insertColor = undefined;
    $(this).removeClass("selected");
    return;
  }

  if (insertColor !== undefined) {
    $(".insertion > .stone-btn").removeClass("selected");
  }

  insertColor = "white";
  $(this).addClass("selected");
})

// First color
$("#first-black").click(function() {
  $(".bottom-container > .stone-btn").removeClass("selected");

  firstStoneColor = "black";
  $(this).addClass("selected");
})

$("#first-white").click(function() {
  $(".bottom-container > .stone-btn").removeClass("selected");

  firstStoneColor = "white";
  $(this).addClass("selected");
})

$("#start-btn").click(function() {
  if (Object.keys(placedStones).length === 0) {
    alert("Insert stones");
    return;
  }

  if (firstStoneColor === undefined) {
    alert("Choose first stone color");
  }
})

// Set board positions index
 $(".board-pos").each(function(index) {
  $(this).data("index", index);
})

// Insertions
$(".board-pos").click(function() {
  if (insertColor === undefined) {
    return;
  }
  index = $(this).data("index");
  color = placedStones[index];

  if (color !== undefined) {
    $(this).empty();
    delete placedStones[index];

    if (insertColor === color) {
      return;
    }
  }

  placedStones[index] = insertColor;

  if (insertColor === "black") {
    $(this).append("<img class='stone' data-color='black' src='/static/images/black.png' alt=''>");
    return;
  }

  $(this).append("<img class='stone' data-color='white' src='/static/images/white.png' alt=''>");
})
