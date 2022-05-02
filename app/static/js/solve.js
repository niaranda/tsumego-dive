// Resize content
$("nav").css("width", "90%");
$("nav").css("min-width", "1000px");

$("#content-div").css("width", "90%");
$("#content-div").css("min-width", "1000px");

let placedStones;
let nextColor;
let gameTree;
let selectedNodeId;

let treeConfig;
let treeNodes;

initialConfig();

function initialConfig() {
  // Create split
  function reDrawTree() {
    gameTree = gameTree.reload();
  }

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
  placedStones = initialStones;

  $(".board-pos").each(function(index) {
    $(this).data("index", index);
    if (index in placedStones) {
      placeStone($(this), placedStones[index]);
    }
  })

  // Next color
  nextColor = firstColor;

  // Initial tree
  treeConfig = [{
    container: "#tree-div",
    connectors: {
      type: "step"
    }
  }];

  root = {
    image: "static/images/circle.png",
    HTMLclass: "selected-node",
    text: {
      data: {
        placedStones: initialStones,
        nextColor: firstColor,
        forbiddenMoves: forbiddenMoves
      }
    }
  };

  treeConfig.push(root);
  treeNodes = {};
  treeNodes[0] = root;

  let chart = new Treant(treeConfig, null, $);
  gameTree = chart.tree;

  // Selected node
  selectedNodeId = gameTree.root().id;
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
   if (index in placedStones) {
     placeStone($(this), placedStones[index]);
   } else {
     removeStone($(this));
   }
 })
}

// Preview move
function isForbidden(posElement) {
  return forbiddenMoves.includes(posElement.data("index"));
}

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
  placedStones = next.text.data["placedStones"];
  nextColor = next.text.data["nextColor"];
  forbiddenMoves = next.text.data["forbiddenMoves"];

  replaceStones();
}

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