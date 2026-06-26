// The URL of our FastAPI backend
const API_URL = "http://127.0.0.1:8000/tasks";

// Grab elements from the HTML
const taskForm = document.getElementById("task-form");
const taskInput = document.getElementById("task-input");
const taskList = document.getElementById("task-list");

// 1. FETCH TASKS FROM BACKEND
async function loadTasks() {
    try {
        const response = await fetch(API_URL);
        const tasks = await response.json();
        renderTasks(tasks);
    } catch (error) {
        console.error("Error loading tasks:", error);
    }
}

// 2. RENDER TASKS TO THE SCREEN
function renderTasks(tasks) {
    taskList.innerHTML = ""; // Clear the list first
    
    tasks.forEach(task => {
        // Create the task container
        const taskItem = document.createElement("div");
        taskItem.className = "task-item";
        taskItem.dataset.id = task.id; // Store ID for later

        // Create description text
        const desc = document.createElement("span");
        desc.className = "task-description";
        desc.textContent = task.description;

        // Create status badge
        const status = document.createElement("span");
        status.className = `task-status status-${task.status}`;
        status.textContent = task.status;

        // Create action buttons
        const actions = document.createElement("div");
        actions.className = "task-actions";
        
        const doneBtn = document.createElement("button");
        doneBtn.className = "btn-mark-done";
        doneBtn.textContent = "Done";
        doneBtn.dataset.action = "done";

        const deleteBtn = document.createElement("button");
        deleteBtn.className = "btn-delete";
        deleteBtn.textContent = "Delete";
        deleteBtn.dataset.action = "delete";

        // Assemble the task item
        actions.appendChild(doneBtn);
        actions.appendChild(deleteBtn);
        taskItem.appendChild(desc);
        taskItem.appendChild(status);
        taskItem.appendChild(actions);
        
        // Add to the screen
        taskList.appendChild(taskItem);
    });
}

// 3. ADD A NEW TASK
taskForm.addEventListener("submit", async (e) => {
    e.preventDefault(); // Stop the page from refreshing
    
    const description = taskInput.value.trim();
    if (!description) return;

    try {
        await fetch(API_URL, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ description: description })
        });
        taskInput.value = ""; // Clear input
        loadTasks(); // Refresh the list
    } catch (error) {
        console.error("Error adding task:", error);
    }
});

// 4. HANDLE BUTTON CLICKS (Delete & Mark Done)
// We use "Event Delegation" - listening on the parent container instead of every single button
taskList.addEventListener("click", async (e) => {
    const button = e.target.closest("button");
    if (!button) return;

    const taskItem = button.closest(".task-item");
    const taskId = taskItem.dataset.id;
    const action = button.dataset.action;

    try {
        if (action === "delete") {
            await fetch(`${API_URL}/${taskId}`, { method: "DELETE" });
        } else if (action === "done") {
            await fetch(`${API_URL}/${taskId}`, {
                method: "PUT",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ status: "done" })
            });
        }
        loadTasks(); // Refresh the list
    } catch (error) {
        console.error("Error updating task:", error);
    }
});

// Load tasks when the page first opens
loadTasks();