document.addEventListener("DOMContentLoaded", function () {
    const quill = new Quill("#description", {
      theme: "snow",
    });
  
    document.getElementById("cancel").addEventListener("click", () => {
      window.location.href = "/tasks/page/1";
    });
  
    document.getElementById("task-form").addEventListener("submit", (event) => {
      event.preventDefault();
  
      const title = document.getElementById("title").value;
      const type = document.getElementById("type").value;
      const priority = document.getElementById("priority").value;
      const description = quill.root.innerHTML;
  
      const taskData = {
        title: title,
        task_type: type,
        priority: priority,
        description: description,
        status: "Aberta",
      };
  
      fetch("/tasks", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(taskData),
      })
        .then((response) => {
          if (response.ok) {
            return response.json();
          }
          throw new Error("Erro ao salvar a tarefa");
        })
        .then((data) => {
          sessionStorage.setItem(
            "taskInserted",
            JSON.stringify({ taskId: data.id, title: title, showMessage: true })
          );
          window.location.href = "/tasks/page/1";
        })
        .catch((error) => {
          console.error("Erro:", error);
        });
    });
  
    const typeSelect = document.getElementById("type");
    const defaultOption = typeSelect.options[0];
  
    typeSelect.addEventListener("change", (event) => {
      const selectedOption = event.target.options[event.target.selectedIndex];
  
      if (selectedOption.value !== "") {
        typeSelect.removeChild(defaultOption);
      }
    });
  
    const prioritySelect = document.getElementById("priority");
    const defaultPriorityOption = prioritySelect.options[0];
  
    prioritySelect.addEventListener("change", (event) => {
      const selectedOption = event.target.options[event.target.selectedIndex];
  
      if (selectedOption.value !== "") {
        prioritySelect.removeChild(defaultPriorityOption);
      }
    });
  });
  