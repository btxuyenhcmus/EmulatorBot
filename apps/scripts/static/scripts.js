let step = 1;
let scriptSteps = [];
let selectedProfiles = [];
function runScript(scriptId) {
  const hostInput = document.getElementById("host-input");
  const host = hostInput.value;
  console.log(hostInput);

  const profileSelect = document.getElementById("profile-select");
  console.log(profileSelect);
  const profileId = profileSelect ? profileSelect.value : null;
  console.log(profileId);
  if (!host) {
    alert("Please enter a HOST.");
    return;
  }
  const url = new URL(`script/run/${scriptId}`, window.location.origin);
  url.searchParams.append("host", host);
  url.searchParams.append("profile_id", profileId);

  fetch(url)
    .then((response) => {
      if (!response.ok) {
        throw new Error(`Error: ${response.status} - ${response.statusText}`);
      }
      return response.json();
    })
    .catch((error) => {
      console.error(error);
    });
}

function createScript() {
  const scriptName = document.getElementById("script-name").value;
  const scriptId = document.getElementById("script-id").value;
  console.log(scriptId)
  let steps = [];
  if (!scriptName) {
    alert("Please enter a script name.");
    returns;
  }
  for (let index = 1; index <= step; index++) {
    const actionSelect = document.getElementById(`action-select-${index}`);
    if (actionSelect == null) {
      continue;
    }
    const actionOption = actionSelect.options[actionSelect.selectedIndex];
    const actionValue = actionOption.value;
    const parametersContainer = document.getElementById(
      `parameters-container-${index}`
    );
    const inputs = parametersContainer.querySelectorAll("input");
    const parameters = {};
    inputs.forEach((input) => {
      parameters[input.name] = input.value;
    });
    if (!actionValue) {
      alert("Please select an action for step " + index);
      return;
    } else {
      const step = {
        step_order: index,
        action: actionValue,
        parameters: parameters,
      };
      steps.push(step);
    }
  }
  fetch("script/create-script/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": getCookie("csrftoken"),
    },
    body: JSON.stringify({ scriptId, scriptName, steps }),
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.status === "success") {
        reloadScripts();
        $("#createScriptModal").modal("hide");
      } else {
        console.error("Error:", data.message);
      }
    })
    .catch((error) => {
      console.error("Error:", error);
    });
  console.log(steps);
}
function runRefresh() {
  fetch("/refresh").then((data) => location.reload());
}
function showParameters(step) {
  const actionSelect = document.getElementById(`action-select-${step}`);
  console.log(actionSelect)
  const selectedAction = actionSelect.value;
  const parametersContainer = document.getElementById(
    `parameters-container-${step}`
  );
  const parametersForm = document.getElementById(`parameters-form-${step}`);

  // Clear previous parameters
  parametersForm.innerHTML = "";
  parametersContainer.style.display = "none";
  if (selectedAction) {
    parametersContainer.style.display = "block";
    let parametersHtml = "";
    switch (selectedAction) {
      case "open_url":
        parametersHtml +=
          '<div class="form-inline mb-2"><label for="url">URL:</label><input type="text" class="form-control" name="url" required /></div>' +
          '<div class="form-inline mb-2"><label for="delay">Delay:</label><input type="number" class="form-control" name="delay" required /></div>';
        break;
      case "scroll_to_element":
        parametersHtml +=
          '<div class="form-inline mb-2"><label for="selector">CSS_Selector:</label><input type="text" class="form-control" name="selector" required /></div>' +
          '<div class="form-inline mb-2"><label for="delay">Delay:</label><input type="number" class="form-control" name="delay" required /></div>';
        break;
      case "watch_video":
        parametersHtml +=
          '<div class="form-inline mb-2"><label for="url">Video URL:</label><input type="text" class="form-control" name="url" required /></div>' +
          '<div class="form-inline mb-2"><label for="delay">Delay:</label><input type="number" class="form-control" name="delay" required /></div>';
        break;
      case "click_element":
        parametersHtml +=
          '<div class="form-inline mb-2"><label for="selector">CSS_Selector:</label><input type="text" class="form-control" name="selector" required /></div>' +
          '<div class="form-inline mb-2"><label for="delay">Delay:</label><input type="number" class="form-control" name="delay" required /></div>';
        break;
      default:
        parametersHtml+='<div class="form-inline mb-2"><label for="delay">Delay:</label><input type="number" class="form-control" name="delay" required /></div>';
        break;
    }
    parametersForm.innerHTML = parametersHtml;
  }
}

function addParameters() {
  step++;
  const stepsContainer = document.getElementById("select-container");
  const newStep = document.createElement("div");
  newStep.className = "form-inline mb-3";
  // Tạo HTML cho các lựa chọn hành động
  let optionsHTML = `<option value="" selected disabled hidden>Chọn hành động</option>`;
  actionChoices.forEach((choice) => {
    optionsHTML += `<option value="${choice.value}">${choice.display}</option>`;
  });

  newStep.innerHTML = `
  <p class='mt-3 mr-2'>${step}</p>
      <select id="action-select-${step}" class="form-control" onchange="showParameters(${step})">
          ${optionsHTML}
      </select>
      <button class="form-control ml-2" type="button" onclick="removeSelect(this)">Xoá</button>
      <div id="parameters-container-${step}" style="display: none">
          <div id="parameters-form-${step}" class="mb-2 mt-2"></div>
      </div>
  `;
  stepsContainer.appendChild(newStep);
}

function removeSelect(button) {
  console.log(step);
  const selectDiv = button.parentElement;
  selectDiv.remove();
}
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      // Check if this cookie string begins with the name we want
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}
function editScript(scriptId) {
  fetch(`script/fetch-script-by-id/${scriptId}`, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
    },
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.success) {
        document.getElementById("script-id").value = scriptId;
        // Điền thông tin kịch bản vào modal
        document.getElementById("script-name").value = data.script.name;
        const stepsContainer = document.getElementById("select-container");
        stepsContainer.innerHTML = ""; // Xóa tất cả bước hiện tại
        step = 0; // Reset bước

        data.script.steps.forEach((scriptStep) => {
          step++;
          const newStep = document.createElement("div");
          newStep.className = "form-inline mb-3";
          newStep.innerHTML = `
            <p class="mt-3 mr-2">${step}</p>
            <select id="action-select-${step}" class="form-control" onchange="showParameters(${step})">
              ${actionChoices
                .map(
                  (choice) =>
                    `<option value="${choice.value}" action-id="${choice.id}" ${
                      choice.value === scriptStep.action ? "selected" : ""
                    }>${choice.display}</option>`
                )
                .join("")}
            </select>
            <button class="form-control ml-2" type="button" onclick="removeSelect(this)">Xoá</button>
            <div id="parameters-container-${step}" style="display: block;">
              <div id="parameters-form-${step}" class="mb-2 mt-2">
                ${Object.keys(scriptStep.parameters)
                  .map(
                    (key) =>
                      `<div class="form-inline mb-2">
                         <label for="${key}">${key}:</label>
                         <input type="text" class="form-control" name="${key}" value="${scriptStep.parameters[key]}" required />
                       </div>`
                  )
                  .join("")}
              </div>
            </div>`;
          stepsContainer.appendChild(newStep);
        });

        $("#createScriptModal").modal("show");
      } else {
        alert("Không thể tải dữ liệu kịch bản!");
      }
    })
    .catch((error) => console.error("Error:", error));
}

function reloadScripts() {
  fetch("script/fetch-scripts/", {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
    },
  })
    .then((response) => response.json())
    .then((data) => {
      updateTable(data.scripts);
    })
    .catch((error) => {
      console.error("Error:", error);
    });
}

function updateTable(scripts) {
  const tableBody = document.getElementById("scriptsTableBody");
  tableBody.innerHTML = "";

  scripts.forEach((script) => {
    const row = document.createElement("tr");
    row.innerHTML = `
          <td>${script.name}</td>
          <td>${script.steps[0].created}</td>
          <td>${script.steps.length}</td>
          <td>
              <button type="button" class="btn btn-light" onclick="runScript('${script.id}')"><i class="fa-solid fa-play" style="color: #2ce24a;"></i></button>
               <button type="button" class="btn btn-light" onclick="editScript('${script.id}')"><i class="fa-solid fa-pen-to-square"></i></button>
            <button type="button" class="btn btn-light" onclick="deleteScript('${script.id}')"><i class="fa-solid fa-trash" style="color: #d9172a;"></i></button>
          </td>
      `;
    tableBody.appendChild(row);
  });
}
function deleteScript(scriptId) {
  fetch(`script/delete-script/${scriptId}`, {
    method: "POST",
    headers: {
      "X-CSRFToken": getCookie("csrftoken"), // Đảm bảo gửi CSRF token
      "Content-Type": "application/json",
    },
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.success) {
        alert(data.message);
        reloadScripts();
      } else {
        alert(`Lỗi: ${data.message}`);
      }
    })
    .catch((error) => console.error("Error:", error));
}
function updateSelectedProfiles() {
  selectedProfiles = [];
  document.querySelectorAll(".form-check-input:checked").forEach((checkbox) => {
    const profileId = checkbox.value;
    if (!selectedProfiles.includes(profileId)) {
      selectedProfiles.push(profileId); // Only add if it doesn't exist in the array
    }
  });

}
function resetCreateScriptForm() {
  document.getElementById('createScriptForm').reset(); // Reset form
    const stepsContainer = document.getElementById('select-container');
    
    if (stepsContainer.children.length > 0) {
        while (stepsContainer.children.length > 1) {
            stepsContainer.removeChild(stepsContainer.lastChild);
        }
    }
    step = 1; 
}
function openCreateScriptModal() {
  resetCreateScriptForm();
  $('#createScriptModal').modal('show');
}