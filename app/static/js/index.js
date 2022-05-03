let insertColor;


// Set board positions index and place stones
initialiseInsertBoard();

// Error message
if (error !== undefined) {
  alert(error);
}

// Insertion color
$("#insert-black").click(function() {
  chooseInsertColor("black");
})

$("#insert-white").click(function() {
  chooseInsertColor("white");
})

function chooseInsertColor(chosenColor) {
  if (insertColor === chosenColor) {
    insertColor = undefined;
    $("#insert-" + chosenColor).removeClass("selected");
    return;
  }

  if (insertColor !== undefined) {
    $(".insertion > .stone-btn").removeClass("selected");
  }

  insertColor = chosenColor;
  $("#insert-" + chosenColor).addClass("selected");
}

// Preview insertion
$(".board-pos").mouseenter(function(event) {
  if (insertColor === undefined || $(this).data("index") in placedStones) {
    return;
  }
  $(this).append("<img class='stone selected-pos' src='/static/images/" + insertColor + ".png' alt=''>");
})

$(".board-pos").mouseleave(function(event) {
  if (insertColor === undefined || $(this).data("index") in placedStones) {
    return;
  }
  removeStone($(this));
})

// First color selection
$("#first-black").click(function() {
  chooseFirstStoneColor("black");
})

$("#first-white").click(function() {
  chooseFirstStoneColor("white");
})

function chooseFirstStoneColor(chosenColor) {
  $(".bottom-container > .stone-btn").removeClass("selected");

  firstStoneColor = chosenColor;
  $("#first-" + chosenColor).addClass("selected");
}

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

  let form = createHiddenForm("/solve");
  addFormInput(form, "placed_stones", JSON.stringify(placedStones));
  addFormInput(form, "first_color", firstStoneColor);
  form.submit();
})

// Sgf upload
$("#from-sgf-btn").click(function() {
  $("#upload-sgf").click();
})

$("#upload-sgf").change(function() {
  $("#sgf-file-form").submit()
})
