function handleFormSubmit(formId, successFunction) {
  const form = document.getElementById(formId);
  if (!form) return;
  const dataFields = document.querySelectorAll("input, select, textarea");
  dataFields.forEach((field) => {
    field.addEventListener("input", () => {
      const errorElement = document.querySelector(`#${field.id}-errors`);
      if (errorElement) {
        errorElement.innerHTML = "";
      }
    });
  });
  form.addEventListener("submit", (event) => {
    event.preventDefault();
    const formData = new FormData(form);
    fetch(form.action, {
      method: "POST",
      body: formData,
    })
      .then((response) => {
        if (response.status === 400) {
          response.json().then((data) => {
            const errorMessages = Object.entries(data.errors);
            errorMessages.forEach(([field, message]) => {
              const errorElement = document.querySelector(`#${field}-errors`);
              errorElement.innerHTML = `<div class="btn btn-warn">${message}</div>`;
            });
          });
        } else if (response.status === 200) {
          response.json().then((data) => successFunction(data));
        }
      })
      .catch((error) => console.error(error));
  });
}

handleFormSubmit("login_form", function (data) {
  const params = new URLSearchParams(window.location.search);
  const redirect = params.get("redirect");
  if (redirect) window.location = redirect;
  else window.location = "/";
});

handleFormSubmit("register_form", function (data) {
  window.location = "/";
});

handleFormSubmit("upload_form", function (data) {
  window.location = `/post/${data.post}`;
});

handleFormSubmit("addtag_form", function (data) {
  window.location.reload();
});

handleFormSubmit("addcomment_form", function (data) {
  window.location.reload();
});

handleFormSubmit("editprofile_form", function (data) {
  window.location = `/profile/${data.username}`;
});

const spans = document.querySelectorAll("span[data-timestamp]");

spans.forEach((span) => {
  span.classList.add("timestamp");
  const options = {
    year: "numeric",
    month: "long",
    day: "numeric",
    hour: "numeric",
    minute: "numeric",
    hour12: true,
    timeZoneName: "short",
  };
  const timestamp = parseInt(span.getAttribute("data-timestamp"), 10);
  const date = new Date(timestamp * 1000);
  var formattedDate = date.toLocaleString("en-US", options);
  formattedDate = formattedDate.replace(
    `${date.getDate()},`,
    `${date.getDate()}`
  );
  span.textContent = formattedDate;
});

function addText(fieldId, fieldText) {
  var inputField = document.getElementById(fieldId);
  inputField.value += fieldText + " ";
}

function setText(fieldId, fieldText) {
  var inputField = document.getElementById(fieldId);
  inputField.value = fieldText;
}

function handlePreview(fieldId){
	var field = document.getElementById(fieldId);
	if(!field) return;
	field.onchange = function () {
		var src = URL.createObjectURL(field.files[0]);
		document.getElementById('preview-img').src = src;
	}
}

handlePreview('file');
handlePreview('avatar');
