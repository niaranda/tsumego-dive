function initialiseInsertBoard() {
  // Set indexes and place stones
  setBoardPosIndexes();
  replaceStones();

  // Insertions
  $(".board-pos").click(function() {
    if (insertColor === undefined) {
      return;
    }
    index = $(this).data("index");
    color = placedStones[index];

    $(this).empty();
    if (color !== undefined) {
      delete placedStones[index];

      if (insertColor === color) {
        return;
      }
    }

    placedStones[index] = insertColor;

    placeStone($(this), insertColor);
  })
}

function initialiseSolveBoard() {
  // Set board positions index and stones
  placedStones = {
    ...initialStones
  };

  setBoardPosIndexes();
  replaceStones();
  setMakeMoveEvents();

  // Next color
  nextColor = firstColor;
}

function setBoardPosIndexes() {
  $(".board-pos").each(function(index) {
    $(this).data("index", index);
  })
}

// Board changes
function placeStone(element, color) {
  element.append("<img class='stone' data-color='" + color + "' src='/static/images/" + color + ".png' alt=''>");
}

function removeStone(element) {
  element.empty();
}

function replaceStones() {
  $(".board-path-mark").remove();
  $(".board-pos").each(function(index) {
    removeStone($(this));
    if (index in placedStones) {
      placeStone($(this), placedStones[index]);
    }
    if (index in exploredPaths) {
      placePathMark(index, exploredPaths[index]);
    }
  })
}

function isForbidden(posElement) {
  return forbiddenMoves.includes(posElement.data("index"));
}

// Make move
function setMakeMoveEvents() {
  $(".board-pos").click(function(event) {
    if (isForbidden($(this))) {
      return;
    }

    // Get current color
    let currentColor = nextColor;

    resetDive();

    // Update board
    let selectedNode = gameTree.getNodeDb().get(selectedNodeId);
    let children = getChildren(selectedNode);

    let index = $(this).data("index");

    if (index in exploredPaths) {
      let nextNode = children.filter(function(child) {
        let childStone = child.text.data["newStone"];
        return Object.keys(childStone)[0] == index;
      })[0]

      navigateTree(nextNode);
      return;
    }

    updateBoardData(index);
  })
}

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
      addTreeNode(newStone);
    }
  )

}
