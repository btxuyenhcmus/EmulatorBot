let step = 1;
let scriptSteps = [];
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

  // const outputElement = document.getElementById(`${scriptName}-output`);
  // outputElement.innerText = "Running";

  const url = new URL(
    `api/multilogin/run/${scriptId}`,
    window.location.origin
  );
  url.searchParams.append("host", host);
  url.searchParams.append("profile_id", profileId);
  // url.searchParams.append('folder_id', folderId);

  fetch(url)
    .then((response) => {
      if (!response.ok) {
        throw new Error(`Error: ${response.status} - ${response.statusText}`);
      }
      return response.json();
    })
    // .then((data) => {
    //   if (data.error) {
    //     outputElement.innerText = `Error: ${data.error}`;
    //   } else {
    //     outputElement.innerText = data.output;
    //   }
    // })
    .catch((error) => {
      console.error(error);
      // outputElement.innerText = "Error running the script: " + error.message;
    })
    // .finally(() => {
    //   // outputElement.style.display = "block";
    // });
}

function createScript() {
  const scriptName = document.getElementById("script-name").value;
  let scriptId;
  let steps=[]
    
  for (let index = 1; index <= step; index++) {
    const actionSelect = document.getElementById(`action-select-${index}`);
    if (actionSelect == null) {
      continue;
    }
    const actionOption = actionSelect.options[actionSelect.selectedIndex];
    const selectedActionId = actionOption.getAttribute("action-id");
    // console.log(selectedActionId)
    const parametersContainer = document.getElementById(
      `parameters-container-${index}`
    );
    const inputs = parametersContainer.querySelectorAll("input");
    const parameters = {};
    inputs.forEach((input) => {
      parameters[input.name] = input.value;
    });
    if (!selectedActionId) {
      alert("Please select an action for step " + index);
    } else {
      const step = {
        // script_id: scriptId,
        step_order: index,
        action_id: selectedActionId,
        parameters: parameters,
      };
      steps.push(step)
    }
  }
  fetch("create-script/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": getCookie("csrftoken"),
    },
    body: JSON.stringify({scriptName,steps})
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.status === "success") {
        // scriptId = data.script_id;
        // console.log("Script ID:", scriptId);
      } else {
        console.error("Error:", data.message);
      }
    })
    .catch((error) => {
      console.error("Error:", error);
    });
  console.log(steps)
}
function runRefresh() {
  fetch("/refresh").then((data) => location.reload());
}
function showParameters(step) {
  const actionSelect = document.getElementById(`action-select-${step}`);
  const selectedAction = actionSelect.value;
  const parametersContainer = document.getElementById(
    `parameters-container-${step}`
  );
  const parametersForm = document.getElementById(`parameters-form-${step}`);
  // console.log(selectedAction);

  // Clear previous parameters
   parametersForm.innerHTML = "";
  parametersContainer.style.display = "none";
  if (selectedAction) {
    parametersContainer.style.display = "block";
    let parametersHtml = "";
    switch (selectedAction) {
      case "visit_website":
        parametersHtml +=
          '<div class="form-inline mb-2"><label for="url">URL:</label><input type="text" class="form-control" name="url" required /></div>' +
          '<div class="form-inline mb-2"><label for="delay">Delay:</label><input type="number" class="form-control" name="delay" required /></div>';
        break;
      case "scroll_start":
        parametersHtml +=
          '<div class="form-inline mb-2"><label for="delay">Delay:</label><input type="number" class="form-control" name="delay" required /></div>';
        break;
      case "scroll_end":
        parametersHtml +=
          '<div class="form-inline mb-2"><label for="delay">Delay:</label><input type="number" class="form-control" name="delay" required /></div>';
        break;
      case "scroll_up":
        parametersHtml +=
          '<div class="form-inline mb-2"><label for="amount">Amount:</label><input type="number" name="amount"></input><p class="ml-2">px</p>' +
          '<div class="form-inline mb-2"><label for="delay">Delay:</label><input type="number" class="form-control" name="delay" required /></div>';
        break;
      case "scroll_down":
        parametersHtml +=
          '<div class="form-inline mb-2"><label for="amount">Amount:</label><input type="number" name="amount"></input><p class="ml-2">px</p>' +
          '<div class="form-inline mb-2"><label for="delay">Delay:</label><input type="number" class="form-control" name="delay" required /></div>';
        break;
      case "watch_video":
        parametersHtml +=
          '<div class="form-inline mb-2"><label for="url">Video URL:</label><input type="text" class="form-control" name="url" required /></div>' +
          '<div class="form-inline mb-2"><label for="delay">Delay:</label><input type="number" class="form-control" name="delay" required /></div>';
        break;
      case "click_position":
        parametersHtml +=
          '<div class="form-inline mb-2"><label for="x_position">X Position:</label><input type="number" class="form-control" name="x_position" required /></div>';
        parametersHtml +=
          '<div class="form-inline mb-2"><label for="y_position">Y Position:</label><input type="number" class="form-control" name="y_position" required /></div>' +
          '<div class="form-inline mb-2"><label for="delay">Delay:</label><input type="number" class="form-control" name="delay" required /></div>';
        break;
      default:
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
    optionsHTML += `<option action-id="${choice.id}" value="${choice.value}">${choice.display}</option>`;
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
  // Xóa select và nút tương ứng'
  // step--;
  console.log(step);
  const selectDiv = button.parentElement;
  selectDiv.remove();
}
// function removeSelect(button) {
//   // Tìm bước cha chứa nút bấm
//   const stepDiv = button.parentElement;
//   const stepsContainer = document.getElementById("select-container");

//   // Xóa bước hiện tại
//   stepsContainer.removeChild(stepDiv);

//   // Cập nhật lại thứ tự các bước
//   const remainingSteps = stepsContainer.children;
//   for (let index = 0; index < remainingSteps.length; index++) {
//     const currentStepDiv = remainingSteps[index];
//     // Cập nhật số thứ tự hiển thị
//     const stepNumber = index + 1; // Bắt đầu từ 1
//     currentStepDiv.querySelector("p").innerText = stepNumber;

//     // Cập nhật ID cho select
//     const actionSelect = currentStepDiv.querySelector("select");
//     actionSelect.id = `action-select-${stepNumber}`;
//     // Cập nhật hàm onchange
//     actionSelect.setAttribute("onchange", `showParameters(${stepNumber})`);
//     // Cập nhật ID cho parameters-container
//     const parametersContainer = currentStepDiv.querySelector(
//       `parameters-container-${stepNumber}`
//     );
//     if (parametersContainer) {
//       parametersContainer.id = `parameters-container-${stepNumber}`;
//     }

//     // Cập nhật ID cho parameters-form
//     const parametersForm = currentStepDiv.querySelector(
//       `parameters-form-${stepNumber + 1}`
//     );
//     if (parametersForm) {
//       parametersForm.id = `parameters-form-${stepNumber}`;
//     }
//   }

//   // Giảm bước nếu cần
//   step--;
// }
// Function to get CSRF token
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


