let chart;
let gameTree;
let selectedNodeId;

let resizeTimeout;

function reDrawTree() {
  gameTree = gameTree.redraw();
}

// Redraw tree on window resize
$(window).resize(function() {
  clearTimeout(resizeTimeout);
  resizeTimeout = setTimeout(reDrawTree, 50);
})

function initialiseTree() {
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
  let next = getNextNode(selected, direction);

  if (next === undefined || next === null) {
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

function getNextNode(selected, direction) {
  switch (direction) {
    case "up":
      return selected.parent();
    case "down":
      return selected.firstChild();
    case "left":
      return selected.leftSibling();
    case "right":
      return selected.rightSibling();
    default:
      return null;
  }
}
