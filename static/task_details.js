document.addEventListener("DOMContentLoaded", function () {
  const modal = document.getElementById("confirm-modal");
  const confirmBtn = document.getElementById("confirm-btn");
  const cancelBtn = document.getElementById("cancel-btn");
  const taskTitle = document.getElementById("task-title");
  const taskId = parseInt(window.location.pathname.split("/")[2]);
  const btnSave = document.getElementById("btn-save");
  const finishBtn = document.getElementById("finish-task");
  const newObservationTextArea = document.getElementById("new-observation-textarea");

  const quill = new Quill("#new-observation-textarea", {
    theme: "snow",
  });

  document.querySelector(".button-assume-task").addEventListener("click", function () {
    modal.style.display = "block";
    taskTitle.textContent = document.querySelector(".task-details h3").textContent;
  });

  document.getElementById('cancel').addEventListener('click', () => {
    window.location.href = '/tasks/page/1';
  });

  cancelBtn.addEventListener("click", function () {
    modal.style.display = "none";
  });

  confirmBtn.addEventListener("click", async function () {
    const response = await fetch(`/task/${taskId}/assume`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
    });

    if (response.status === 200) {
      modal.style.display = "none";
      location.reload();
    } else {
      alert("Houve um erro ao assumir a tarefa. Tente novamente.");
    }
  });

  finishBtn.addEventListener("click", function () {
    document.getElementById("task-status").value = "Concluída";
    console.log(document.getElementById("task-status").value);
    newObservationTextArea.removeAttribute("disabled");
    newObservationTextArea.focus();
    btnSave.classList.remove("btn-disabled");
  });


  btnSave.addEventListener("click", (event) => {
    if (!validateObservation()) {
      event.preventDefault();
      window.alert("Digite pelo menos 5 caracteres na nova observação.");
    } else {
      btnSave.classList.add("btn-disabled");
    }
  });


  window.addEventListener("click", function (event) {
    if (event.target === modal) {
      modal.style.display = "none";
    }
  });

  function validateObservation() {
    return newObservationTextArea.getText().trim().length >= 5;
  }

  document.querySelector('form').addEventListener('submit', () => {
    const newObservationContent = JSON.stringify(newObservationEditor.getContents());
    newObservationInput.value = newObservationContent;
  });
});
