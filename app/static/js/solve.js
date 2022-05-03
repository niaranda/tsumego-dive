// Resize content
$("nav").css("width", "90%");
$("nav").css("min-width", "1000px");

$("#content-div").css("width", "90%");
$("#content-div").css("min-width", "1000px");

let placedStones;
let nextColor;

let dragTimeout;

initialConfig();

function initialConfig() {
  // Create split
  Split(['#split-board', '#split-tree'], {
    minSize: [400, 300],
    gutterSize: 4,
    snapOffset: 0,
    dragInterval: 2,
    sizes: [70, 30],
    onDragStart: function(sizes) {
      $(".arrow").remove();
    },
    onDrag: function(sizes) {
      clearTimeout(dragTimeout);
      dragTimeout = setTimeout(reDrawTree, 50);
    }
  })

  initialiseSolveBoard();
  initialiseTree();

  // Move preview
  setMovePreview();
}

// Preview move
function setMovePreview() {
  $(".board-pos").mouseenter(function(event) {
    if (isForbidden($(this))) {
      return;
    }
    $(this).append("<img class='stone selected-pos' src='/static/images/" + nextColor + ".png' alt=''>");
  })

  $(".board-pos").mouseleave(function(event) {
    if (isForbidden($(this))) {
      return;
    }
    removeStone($(this));
  })
}

// Key events
$("body").keydown(function(event) {
  event.preventDefault();
  switch (event.key) {
    case "ArrowUp":
      $("#arrow-key-up").click();
      break;
    case "ArrowLeft":
      $("#arrow-key-left").click();
      break;
    case "ArrowRight":
      $("#arrow-key-right").click();
      break;
    case "ArrowDown":
      $("#arrow-key-down").click();
      break;
    case " ":
      $("#dive-btn").click();
  }
})

// Button clicks
$(".arrow-key, #dive-btn").click(function(event) {
  $(this).addClass("pressed");
  setTimeout(function() {
    $(".pressed").removeClass("pressed");
  }, 100);
})

$("#arrow-key-up").click(function(event) {
  navigateTree("up");
})

$("#arrow-key-down").click(function(event) {
  navigateTree("down");
})

$("#arrow-key-left").click(function(event) {
  navigateTree("left");
})

$("#arrow-key-right").click(function(event) {
  navigateTree("right");
})

// Return button
$("#return-btn").click(function() {
  let form = createHiddenForm("/");

  addFormInput(form, "placed_stones", JSON.stringify(initialStones));
  addFormInput(form, "first_color", firstColor);

  form.submit();
})
