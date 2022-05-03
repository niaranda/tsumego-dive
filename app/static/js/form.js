function createHiddenForm(action) {
  let form = document.createElement("form");
  form.method = "post";
  form.action = action;
  form.type = "hidden";

  document.body.appendChild(form);
  return form;
}

function addFormInput(form, name, value) {
  let input = document.createElement("input");
  input.name = name;
  input.value = value;
  input.type = "hidden";

  form.appendChild(input);
}
