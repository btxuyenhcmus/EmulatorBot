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
  const hostInput = document.getElementById('host-input');
  const host = hostInput.value;
  console.log(hostInput);

  const profileSelect = document.getElementById('profile-select');
  console.log(profileSelect)
   const profileId = profileSelect ? profileSelect.value : null;
  // const folderId = profileSelect ? profileSelect.options[profileSelect.selectedIndex].getAttribute('data-folder-id') : null;
console.log(profileId);
  if (!host) {
    alert('Please enter a HOST.');
    return;
  }

  // if (!profileId) {
  //   alert('Please select a profile.');
  //   return;
  // }

  const outputElement = document.getElementById(`${scriptName}-output`);
  outputElement.innerText = "Running";

  const url = new URL(`api/multilogin/run/${scriptName}`, window.location.origin);
  url.searchParams.append('host', host);
  url.searchParams.append('profile_id', profileId);
  // url.searchParams.append('folder_id', folderId);

  fetch(url)
    .then((response) => {
      if (!response.ok) {
        throw new Error(`Error: ${response.status} - ${response.statusText}`);
      }
      return response.json();
    })
    .then((data) => {
      if (data.error) {
        outputElement.innerText = `Error: ${data.error}`;
      } else {
        outputElement.innerText = data.output;
      }
    })
    .catch((error) => {
      console.error(error);
      outputElement.innerText = "Error running the script: " + error.message;
    })
    .finally(() => {
      outputElement.style.display = "block";
    });
}

function runRefresh() {
  fetch("/refresh").then((data) => location.reload());
}
