
Split(['#split-board', '#split-tree'], {
  minSize: [400, 300],
  gutterSize: 4,
  snapOffset: 0,
  dragInterval: 2,
  sizes: [70, 30],
  onDragStart: function(sizes) {
    $(".arrow").remove();
  }
})

$("nav").css("width", "90%");
$("nav").css("min-width", "1000px");

$("#content-div").css("width", "90%");
$("#content-div").css("min-width", "1000px");

// Set board positions index and stones
 $(".board-pos").each(function(index) {
  $(this).data("index", index);
  if (index in placedStones) {
    placeStone($(this), placedStones[index]);
  }
})

function placeStone(element, color) {
  element.append("<img class='stone' data-color='" + color + "' src='/static/images/" + color + ".png' alt=''>");
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
  placedStonesInput.value = JSON.stringify(placedStones);
  placedStonesInput.type = "hidden";

  form.appendChild(placedStonesInput);

  let firstColorInput = document.createElement("input");
  firstColorInput.name = "first_color";
  firstColorInput.value = firstColor;
  firstColorInput.type = "hidden";

  form.appendChild(firstColorInput);

  form.submit();
})

// Tree
let treeConfig = {
  chart: {
    container: "#tree-div",
    connectors: {
      type: "step"
    }
  },
  nodeStructure: {
    image: "static/images/" + firstColor + ".png",
    HTMLclass: "selected-node",
    text: {
      data: placedStones
    },
    children: [
      {
        image: "static/images/white.png",
        text: {
          data: placedStones
        }
      },
      {
        image: "static/images/white.png",
        text: {
          data: placedStones
        }
      }
    ]
  }
}

let gameTree = (new Treant(treeConfig, null, $)).tree;
let selected = gameTree.root();

function moveDown() {
  if (selected.children.length == 0) {
    return;
  }
  selected.nodeDOM.classList.remove("selected-node");
  let firstChildId = selected.children[0];
  let firstChild = gameTree.getNodeDb().get(firstChildId);
  firstChild.nodeDOM.classList.add("selected-node");
}
