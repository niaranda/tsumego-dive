
let insertColor;
let firstStoneColor;
let placedStones = {};

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
  if (firstStoneColor === undefined) {
    alert("Choose first stone color");
  }
})
