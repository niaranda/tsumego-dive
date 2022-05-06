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
          },
          pathType: "unknown"
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
function addTreeNode(newStone) {
  let parentNode = gameTree.getNodeDb().get(selectedNodeId);
  parentNode.nodeDOM.classList.remove("selected-node");

  let parentPathType = parentNode.text.data["pathType"];
  let nodePathType = parentPathType;
  if (getChildren(parentNode).length != 0) {
    nodePathType = "unknown";
  }

  let nodeColor = Object.values(newStone)[0];

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
        },
        pathType: nodePathType,
        newStone: newStone
      }
    }
  }

  let newNode = gameTree.addNode(parentNode, newNodeData);

  scrollIntoView(newNode);

  selectedNodeId = newNode.id;
  updatePathType(nodePathType);

  resetDive();
}

function scrollIntoView(node) {
  node.nodeDOM.scrollIntoView({
    behavior: "smooth",
    block: "nearest"
  });
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

  scrollIntoView(next);

  // Retrieve state
  placedStones = {
    ...next.text.data["placedStones"]
  };
  nextColor = next.text.data["nextColor"];
  forbiddenMoves = Object.values(next.text.data["forbiddenMoves"]);

  replaceStones();

  resetDive();
}

function getNextNode(selected, direction) {
  switch (direction) {
    case "up":
      return selected.parent();
    case "down":
      return getCentralChild(selected);
    case "left":
      return selected.leftSibling();
    case "right":
      return selected.rightSibling();
    default:
      return null;
  }
}

function getCentralChild(parent) {
  let children = getChildren(parent);
  let centralNumber = Math.round(children.length / 2);
  return children[centralNumber - 1];
}

function getChildren(node) {
  let children = [];

  let childrenId = node.children;
  if (childrenId === undefined) {
    return [];
  }

  childrenId.forEach(function(id) {
    children.push(gameTree.getNodeDb().get(id));
  });

  return children;
}

function getTreeLeaves() {
  return getLeaves(gameTree.root());
}

function getLeaves(node) {
  let children = getChildren(node);
  if (children.length === 0) {
    return [node];
  }

  if (children.length === 1) {
    return getLeaves(children[0]);
  }

  let leaves = [];
  children.forEach(function(child) {
    leaves = leaves.concat(getLeaves(child));
  })
  return leaves;
}

function updatePathType(type) {
  let selectedNode = gameTree.getNodeDb().get(selectedNodeId);

  // Downwards update
  updateDescendantsPathType(selectedNode, type);

  let leaves = getTreeLeaves();
  updateAncestorsPathType(leaves);

  updatePathMarks();
}

function updateDescendantsPathType(node, type) {
  node.text.data["pathType"] = type;

  getChildren(node).forEach(function(child) {
    updateDescendantsPathType(child, type);
  })
}

function updateAncestorsPathType(leaves) {
  let correctLeaves = [];
  let unknownLeaves = [];
  let wrongLeaves = [];

  leaves.forEach(function(leaf) {
    let pathType = leaf.text.data["pathType"];
    switch (pathType) {
      case "correct":
        correctLeaves.push(leaf);
        break;
      case "unknown":
        unknownLeaves.push(leaf);
        break;
      case "wrong":
        wrongLeaves.push(leaf);
    }
  })

  wrongLeaves.forEach(function(leaf) {
    updateNodeAncestorsPathType(leaf, "wrong");
  })
  unknownLeaves.forEach(function(leaf) {
    updateNodeAncestorsPathType(leaf, "unknown");
  })
  correctLeaves.forEach(function(leaf) {
    updateNodeAncestorsPathType(leaf, "correct");
  })
}

function updateNodeAncestorsPathType(node, type) {
  node.text.data["pathType"] = type;
  let parent = node.parent();

  if (parent === undefined) {
    return;
  }
  updateNodeAncestorsPathType(parent, type);
}

function updatePathMarks() {
  updateDescendantsPathMarks(gameTree.root());
}

function updateDescendantsPathMarks(node) {
  let type = node.text.data["pathType"];
  removeNodePathMark(node);
  addNodePathMark(node, type);

  getChildren(node).forEach(function(child) {
    updateDescendantsPathMarks(child);
  })
}

function addNodePathMark(node, type) {
  if (node.id === gameTree.root().id) {
    return;
  }

  if (type === "unknown") {
    return;
  }

  if (type === "correct") {
    node.nodeDOM.append("✔️");
  }
  if (type === "wrong") {
    node.nodeDOM.append("❌");
  }
}

function removeNodePathMark(node) {
  while (node.nodeDOM.childNodes.length !== 1) {
    node.nodeDOM.removeChild(node.nodeDOM.lastChild);
  }
}
