// Resize content
$("nav").css("width", "90%");
$("nav").css("min-width", "1000px");

$("#content-div").css("width", "90%");
$("#content-div").css("min-width", "1000px");

let placedStones;
let nextColor;

let diveCounter = 0;

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
  navigateTree(getNextNode("up"));
})

$("#arrow-key-down").click(function(event) {
  navigateTree(getNextNode("down"));
})

$("#arrow-key-left").click(function(event) {
  navigateTree(getNextNode("left"));
})

$("#arrow-key-right").click(function(event) {
  navigateTree(getNextNode("right"));
})

// Return button
$("#return-btn").click(function() {
  let form = createHiddenForm("/");

  addFormInput(form, "placed_stones", JSON.stringify(initialStones));
  addFormInput(form, "first_color", firstColor);

  form.submit();
  document.body.removeChild(form);
})

// Dive button
$("#dive-btn").click(function() {
  if (diveCounter == 4) {
    resetDive();
    return;
  }

  $.post("/dive", {
      placed_stones: JSON.stringify(placedStones),
      next_color: nextColor,
      dive_counter: JSON.stringify(diveCounter)
    },
    function(data) {
      let diveIndexes = JSON.parse(data);
      diveCounter += 1;

      addDiveSelections(diveIndexes);

      $("#dive-btn").text("Dive further");
      if (diveCounter == 4) {
        $("#dive-btn").text("Remove");
      }

    }
  )
})

function addDiveSelections(diveIndexes) {
  let recommendationLevels = getRecommendationLevels();

  $(".board-pos").each(function(index) {
    if (diveIndexes.includes(index)) {
      let num = diveIndexes.indexOf(index);
      $(this).addClass("dive-selection" + recommendationLevels[num]);
    }
  })
}

function getRecommendationLevels() {
  if (diveCounter == 1) {
    return [1];
  }
  if (diveCounter == 2) {
    return [1, 2, 2];
  }
  if (diveCounter == 3) {
    return [1, 2, 2, 3, 3];
  }
  return [1, 2, 2, 3, 3, 4, 4, 4, 4, 4];
}

function resetDive() {
  diveCounter = 0;

  $(".dive-selection1").removeClass("dive-selection1");
  $(".dive-selection2").removeClass("dive-selection2");
  $(".dive-selection3").removeClass("dive-selection3");
  $(".dive-selection4").removeClass("dive-selection4");
  $("#dive-btn").text("Dive");
  $("#dive-btn").removeClass("unavailable");
}

// Mark buttons
$("#correct-btn").click(function() {
  updateMark("correct");
})

$("#unknown-btn").click(function() {
  updateMark("unknown");
})

$("#wrong-btn").click(function() {
  updateMark("wrong");
})

// To sgf button
$("#to-sgf-btn").click(function() {
  let treeData = generateTreeData();

  $.post("/download_sgf", {
      tree_data: JSON.stringify(treeData)
    },
    function(data) {
      download(data);
    })
})

function download(data) {
  let blob = new Blob([data]);
  let url = window.URL.createObjectURL(blob);

  let link = document.createElement("a");
  link.href = url;
  link.download = "tsumego.sgf";
  link.type = "hidden";

  console.log(link.href);

  document.body.appendChild(link);
  link.click();

  document.body.removeChild(link);
  setTimeout(function() {
    window.URL.revokeObjectURL(url);
  }, 500);
}
