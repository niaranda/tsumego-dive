let placedStones;
let nextColor;

function initialiseBoard() {
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

function isForbidden(posElement) {
  return forbiddenMoves.includes(posElement.data("index"));
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
