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

  let nodeColor = Object.values(newStone)[0];
  let nodePathType = "unknown";

  // For student moves take path type from grandparent,
  // if it exists and there are no other paths (no siblings or uncles)
  let isNewStudentMove = nodeColor === firstColor;
  let hasGrandParent = parentNode.id !== gameTree.root().id;

  if (isNewStudentMove && hasGrandParent) {
    let grandParentNode = parentNode.parent();
    let hasUncles = getChildren(grandParentNode).length !== 1;
    let hasSiblings = getChildren(parentNode).length !== 0; // Not yet counted

    if (!hasUncles && !hasSiblings) {
      nodePathType = grandParentNode.text.data["pathType"];
    }
  }

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

  if (isNewStudentMove) {
    updatePathType(nodePathType);
  }

  updateExploredPaths();
  replaceStones();

  resetDive();
}

function scrollIntoView(node) {
  node.nodeDOM.scrollIntoView({
    behavior: "smooth",
    block: "nearest"
  });
}

// Tree navigation
function navigateTree(next) {
  if (next === undefined || next === null) {
    return;
  }

  let selected = gameTree.getNodeDb().get(selectedNodeId);
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

  updateExploredPaths();
  replaceStones();

  resetDive();
}

function updateExploredPaths() {
  let selected = gameTree.getNodeDb().get(selectedNodeId);
  exploredPaths = {};

  let children = getChildren(selected);
  if (children.length === 0) {
    return;
  }

  children.forEach(function(child) {
    let index = Object.keys(child.text.data["newStone"])[0];
    let pathType = child.text.data["pathType"];
    exploredPaths[index] = pathType;
  })
}

function getNextNode(direction) {
  let selected = gameTree.getNodeDb().get(selectedNodeId);

  switch (direction) {
    case "up":
      return selected.parent();
    case "down":
      return getCentralChild(selected);
    case "left":
      return selected.leftNeighbor();
    case "right":
      return selected.rightNeighbor();
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

function getTreeStudentLeaves() {
  let studentLeaves = getStudentLeaves(gameTree.root());
  return [...new Set(studentLeaves)]; // Remove possible duplicates
}

function getStudentLeaves(node) {
  let children = getChildren(node);
  if (children.length === 0) {
    if (isStudentMove(node)) {
      return [node];
    }

    let parent = node.parent();

    let hasSiblings = parent.children.length !== 1;

    if (!hasSiblings) {
      return [parent];
    }

    let hasNephews = false;
    let siblings = getChildren(parent).filter(function(child) {
      return child.id !== node.id;
    });
    siblings.forEach(function(sibling) {
      let nephews = getChildren(sibling);
      if (nephews.length !== 0) {
        hasNephews = true;
      }
    })

    if (!hasNephews) {
      return [parent];
    }

    return [];
  }

  if (children.length === 1) {
    return getStudentLeaves(children[0]);
  }

  let leaves = [];
  children.forEach(function(child) {
    leaves = leaves.concat(getStudentLeaves(child));
  })
  return leaves;
}

function updatePathType(type) {
  if (selectedNodeId === gameTree.root().id) {
    return;
  }

  let selectedNode = gameTree.getNodeDb().get(selectedNodeId);

  // If selected is not student move and does not have children, apply to parent
  let children = getChildren(selectedNode);
  if (!isStudentMove(selectedNode) && children.length === 0) {
    selectedNode = selectedNode.parent();
  }

  // Downwards update
  updateDescendantsPathType(selectedNode, type);

  let leaves = getTreeStudentLeaves();
  updateAncestorsPathType(leaves);

  updatePathMarks();
  updateExploredPaths();
  replaceStones();
}

function updateDescendantsPathType(node, type) {
  if (isStudentMove(node)) {
    node.text.data["pathType"] = type;
  }

  getChildren(node).forEach(function(child) {
    updateDescendantsPathType(child, type);
  })
}

function updateAncestorsPathType(leaves) {
  let correctLeaves = [];
  let unknownLeaves = [];
  let wrongLeaves = [];

  leaves.forEach(function(leaf) {
    if (!isStudentMove(leaf)) {
      return;
    }
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
  if (isStudentMove(node)) {
    node.text.data["pathType"] = type;
  }

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

  if (node.text.data["nextColor"] == firstColor) {
    return;
  }

  if (type === "unknown") {
    return;
  }

  let image = document.createElement("img");
  if (type === "correct") {
    image.src = "static/images/check-mark.png";
  }
  if (type === "wrong") {
    image.src = "static/images/cross-mark.png";
  }
  node.nodeDOM.appendChild(image);
}

function removeNodePathMark(node) {
  while (node.nodeDOM.childNodes.length !== 1) {
    node.nodeDOM.removeChild(node.nodeDOM.lastChild);
  }
}

function generateTreeData() {
  return generateNodeData(gameTree.root());
}

function generateNodeData(node) {
  let data = {};

  let raw_data = node.text.data;

  if (node.id === gameTree.root().id) {
    data["initial_stones"] = raw_data["placedStones"];
  } else {
    data["new_stone"] = raw_data["newStone"];
    data["path_type"] = raw_data["pathType"];
  }

  let children = getChildren(node);
  if (children.length === 0) {
    return data;
  }

  let childrenData = [];
  children.forEach(function(child) {
    childrenData.push(generateNodeData(child));
  })

  data["children"] = childrenData;

  return data;
}

function placePathMark(index, pathType) {
  let row = Math.floor(index / 19);
  let col = index % 19;

  let topPixels = 21 + 33.3 * row;
  let leftPixels = 23 + 33.3 * col;

  let element = document.createElement("img");

  if (pathType === "unknown" || nextColor != firstColor) {
    element.src = "static/images/" + nextColor + "-mark.png";
  } else {
    element.src = "static/images/" + pathType + "-mark.png";
  }

  element.classList.add("board-path-mark");
  element.style = "top: " + topPixels + "px; left: " + leftPixels + "px;"
  $(".board-positions").append(element);
}

function isStudentMove(node) {
  return node.text.data["nextColor"] != firstColor;
}
