// Resize content
$("nav").css("width", "90%");
$("nav").css("min-width", "1000px");

$("#content-div").css("width", "90%");
$("#content-div").css("min-width", "1000px");

let placedStones;
let nextColor;

let chart;
let gameTree;
let selectedNodeId;

initialConfig();

function reDrawTree() {
  gameTree = gameTree.redraw();
}

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
    onDragEnd: function(sizes) {
      reDrawTree();
    }
  })

  // Set board positions index and stones
  placedStones = {
    ...initialStones
  };

  $(".board-pos").each(function(index) {
    $(this).data("index", index);
    if (index in placedStones) {
      placeStone($(this), placedStones[index]);
    }
  })

  // Next color
  nextColor = firstColor;

  // Initial tree
  let treeConfig = {
    chart: {
      container: "#tree-div",
      connectors: {
        type: "step"
      },
      node: {
        collapsable: false
      }
    },
    nodeStructure: {
      image: "static/images/circle.png",
      HTMLclass: "selected-node",
      text: {
        data: {
          placedStones: {
            ...initialStones
          },
          nextColor: firstColor,
          forbiddenMoves: {
            ...forbiddenMoves
          }
        }
      }
    }
  }

  chart = new Treant(treeConfig, null, $);
  gameTree = chart.tree;

  // Selected node
  selectedNodeId = gameTree.root().id;

  // Move preview
  setMovePreview();
}

// Board changes
function placeStone(element, color) {
  element.append("<img class='stone' data-color='" + color + "' src='/static/images/" + color + ".png' alt=''>");
}

function removeStone(element) {
  element.empty();
}

function replaceStones() {
  $(".board-pos").each(function(index) {
    removeStone($(this));
    if (index in placedStones) {
      placeStone($(this), placedStones[index]);
    }
  })
}

// Preview move
function isForbidden(posElement) {
  return forbiddenMoves.includes(posElement.data("index"));
}

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

function removeMovePreview() {
  $(".board-pos").off("mouseenter");
  $(".board-pos").off("mouseleave");
}


// Make move
$(".board-pos").click(function(event) {
  if (isForbidden($(this))) {
    return;
  }

  // Get current color
  let currentColor = nextColor;

  // Update board
  updateBoardData($(this).data("index"));
})

function updateBoardData(stoneIndex) {
  let newStone = {}
  newStone[stoneIndex] = nextColor;

  $.post("/move", {
      placed_stones: JSON.stringify(placedStones),
      new_stone: JSON.stringify(newStone)
    },
    function(data) {
      let boardData = JSON.parse(data);
      placedStones = JSON.parse(boardData["placed_stones"]);
      forbiddenMoves = JSON.parse(boardData["forbidden_moves"]);

      nodeColor = nextColor;
      nextColor = nodeColor === "white" ? "black" : "white";

      replaceStones();
      addTreeNode(nodeColor);
    }
  )

}

  // Add node to tree
function addTreeNode(nodeColor) {
  let parentNode = gameTree.getNodeDb().get(selectedNodeId);
  parentNode.nodeDOM.classList.remove("selected-node");

  let newNodeData = {
    image: "static/images/" + nodeColor + ".png",
    HTMLclass: "selected-node",
    text: {
      data: {
        placedStones: {
          ...placedStones
        },
        nextColor: nextColor,
        forbiddenMoves: {
          ...forbiddenMoves
        }
      }
    }
  }

  let newNode = gameTree.addNode(parentNode, newNodeData);
  selectedNodeId = newNode.id;
}

// Tree navigation
function navigateTree(direction) {
  let selected = gameTree.getNodeDb().get(selectedNodeId);
  let next;
  switch (direction) {
    case "up":
      next = selected.parent();
      break;
    case "down":
      next = selected.firstChild();
      break;
    case "left":
      next = selected.leftSibling();
      break;
    case "right":
      next = selected.rightSibling();
  }

  if (next === undefined) {
    return;
  }

  selected.nodeDOM.classList.remove("selected-node");
  next.nodeDOM.classList.add("selected-node");
  selectedNodeId = next.id;

  // Retrieve state
  placedStones = {
    ...next.text.data["placedStones"]
  };
  nextColor = next.text.data["nextColor"];
  forbiddenMoves = Object.values(next.text.data["forbiddenMoves"]);

  replaceStones();
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
  let form = document.createElement("form");
  form.method = "post";
  form.action = "/";
  form.type = "hidden";

  document.body.appendChild(form);

  let placedStonesInput = document.createElement("input");
  placedStonesInput.name = "placed_stones";
  placedStonesInput.value = JSON.stringify(initialStones);
  placedStonesInput.type = "hidden";

  form.appendChild(placedStonesInput);

  let firstColorInput = document.createElement("input");
  firstColorInput.name = "first_color";
  firstColorInput.value = firstColor;
  firstColorInput.type = "hidden";

  form.appendChild(firstColorInput);

  form.submit();
})
