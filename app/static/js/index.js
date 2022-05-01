
let insertColor;

// Error message
if (error !== undefined) {
  alert(error);
}

// Set board positions index and stones
 $(".board-pos").each(function(index) {
  $(this).data("index", index);
  if (index in placedStones) {
    placeStone($(this), placedStones[index]);
  }
})

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

// First color selection
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

// First color from sgf
if (firstStoneColor !== undefined) {
  $("#first-" + firstStoneColor).click();
}

// Start
$(".start-btn").click(function() {
  if (Object.keys(placedStones).length === 0) {
    alert("Insert stones");
    return;
  }

  if (firstStoneColor === undefined) {
    alert("Choose first stone color");
    return;
  }

  let form = document.createElement("form");
  form.method = "post";
  form.action = "/solve";
  form.type = "hidden";

  document.body.appendChild(form);

  let placedStonesInput = document.createElement("input");
  placedStonesInput.name = "placed_stones";
  placedStonesInput.value = JSON.stringify(placedStones);
  placedStonesInput.type = "hidden";

  form.appendChild(placedStonesInput);

  let nextColorInput = document.createElement("input");
  nextColorInput.name = "next_color";
  nextColorInput.value = firstStoneColor;
  nextColorInput.type = "hidden";

  form.appendChild(nextColorInput);

  form.submit();
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

  placeStone($(this), insertColor);
})

// Sgf upload
$("#from-sgf-btn").click(function() {
  $("#upload-sgf").click();
})

$("#upload-sgf").change(function() {
  $("#sgf-file-form").submit()
})

function placeStone(element, color) {
  element.append("<img class='stone' data-color='" + color + "' src='/static/images/" + color + ".png' alt=''>");
}
