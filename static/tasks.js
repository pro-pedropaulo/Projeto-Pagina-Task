function fetchTasks(page) {
    fetch(`/tasks?page=${page}`)
        .then((response) => response.json())
        .then((data) => {
            let tasks = data.tasks;
            let totalTasks = data.total_tasks;

            let tableBody = document.querySelector("#tasks-table tbody");
            tableBody.innerHTML = "";

            tasks.forEach((task) => {
                let row = document.createElement("tr");

                let idCell = document.createElement("td");
                idCell.innerText = task.id;
                row.appendChild(idCell);

                let titleCell = document.createElement("td");
                titleCell.innerText = task.title;
                row.appendChild(titleCell);

                let typeCell = document.createElement("td");
                typeCell.innerText = task.type;
                row.appendChild(typeCell);

                let priorityCell = document.createElement("td");
                priorityCell.innerText = task.priority;
                row.appendChild(priorityCell);

                let dateCell = document.createElement("td");
                dateCell.innerText = task.date;
                row.appendChild(dateCell);

                let responsibleCell = document.createElement("td");
                responsibleCell.innerText = task.responsible_name;
                row.appendChild(responsibleCell);
                

                tableBody.appendChild(row);
            });
        });
}

document.addEventListener('DOMContentLoaded', () => {
    const successMessage = document.getElementById('success-message');
    const taskInserted = JSON.parse(sessionStorage.getItem('taskInserted'));

    if (taskInserted && taskInserted.showMessage) {
        showSuccessMessage(`Tarefa ${taskInserted.title} inserida com sucesso!`);

        taskInserted.showMessage = false;
        sessionStorage.setItem('taskInserted', JSON.stringify(taskInserted));
    }
});

function showSuccessMessage(message) {
    const successMessage = document.getElementById('success-message');
    successMessage.textContent = message;
    successMessage.classList.remove('hidden');

    setTimeout(() => {
        successMessage.classList.add('hidden');
    }, 5000);
}

function completeTask(taskId, taskTitle) {
    fetch(`/tasks/${taskId}/complete`, {
        method: 'POST',
    })
        .then((response) => {
            if (response.ok) {
                sessionStorage.setItem('taskCompleted', JSON.stringify({ taskId: taskId, title: taskTitle, showMessage: true }));
                window.location.reload();
            } else {
                throw new Error('Erro ao concluir a tarefa');
            }
        })
        .catch((error) => {
            console.error('Erro:', error);
        });
}


window.addEventListener('DOMContentLoaded', () => {
    const taskUpdated = JSON.parse(sessionStorage.getItem('taskUpdated'));

    if (taskUpdated && taskUpdated.showMessage) {
        const successMessage = document.createElement('div');
        successMessage.id = 'success-message';
        successMessage.classList.add('success-message');
        successMessage.textContent = `Tarefa ${taskUpdated.title} - ${taskUpdated.taskId} fechada`;
        document.body.appendChild(successMessage);

        sessionStorage.removeItem('taskUpdated');

        setTimeout(() => {
            successMessage.classList.add('hidden');
        }, 5000);
    }
});

const logoutLink = document.querySelector("#logout a");

if (logoutLink) {
    logoutLink.addEventListener("click", (event) => {
        event.preventDefault();
        window.location.href = event.target.href;
    });
}

