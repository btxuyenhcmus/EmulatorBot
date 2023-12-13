let activeProfileElement = null;
let activeProfileId = null;
let activeFolderId = null;

function selectProfile(profileId, folderId, element) {
  if (activeProfileElement) {
    activeProfileElement.classList.remove("active");
  }
  element.classList.add("active");
  activeProfileElement = element;
  activeProfileId = profileId;
  activeFolderId = folderId;
}

function runScript(scriptName) {
  const selectedProfile = activeProfileElement
    ? activeProfileElement.innerText
    : null;
  if (selectedProfile) {
    const outputElement = document.getElementById(`${scriptName}-output`);
    outputElement.innerText = "Running";

    fetch(
      `/run/${scriptName}?profile=${activeProfileId}&folder=${activeFolderId}`
    )
      .then((response) => {
        if (!response.ok) {
          throw new Error(`Error: ${response.status} - ${response.statusText}`);
        }
        return response.text();
      })
      .then((message) => {
        outputElement.innerText = message;
      })
      .catch((error) => {
        console.error(error);
        outputElement.innerText = "Error running the script.";
      })
      .finally(() => {
        outputElement.style.display = "block";
      });
  } else {
    alert("Please select a profile.");
  }
}

function runRefresh() {
  fetch("/refresh").then((data) => location.reload());
}
