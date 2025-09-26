document.addEventListener('DOMContentLoaded', () => {

    // --- Theme Switcher Logic ---
    const themeToggle = document.getElementById('theme-toggle');
    const htmlEl = document.documentElement;

    // Function to set the theme
    const setTheme = (theme) => {
        htmlEl.setAttribute('data-theme', theme);
        localStorage.setItem('theme', theme);
        themeToggle.checked = theme === 'dark';
    };

    // Event listener for the toggle button
    themeToggle.addEventListener('change', () => {
        const newTheme = themeToggle.checked ? 'dark' : 'light';
        setTheme(newTheme);
    });

    // Check for saved theme preference on page load
    const savedTheme = localStorage.getItem('theme') || 'light';
    setTheme(savedTheme);


    // --- AJAX for Adding New Tasks ---
    const addTaskForm = document.getElementById('addTaskForm');
    
    addTaskForm.addEventListener('submit', function(event) {
        // 1. Prevent the default form submission (which causes a page reload)
        event.preventDefault();

        const titleInput = document.getElementById('task-title');
        const descriptionInput = document.getElementById('task-description');
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        
        // 2. Use the Fetch API to send data to the server asynchronously
        fetch(window.location.href, { // Submits to the same URL ('home')
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': csrfToken,
                'X-Requested-With': 'XMLHttpRequest' // Helps Django identify AJAX
            },
            body: `title=${encodeURIComponent(titleInput.value)}&description=${encodeURIComponent(descriptionInput.value)}`
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert(data.error);
            } else {
                // 3. If successful, dynamically create and add the new task card to the page
                const taskListContainer = document.getElementById('task-list-container');
                const noTasksMessage = document.getElementById('no-tasks-message');
                
                // Remove the "No tasks yet" message if it exists
                if (noTasksMessage) {
                    noTasksMessage.remove();
                }

                // Create the new task card HTML
                const newTaskHtml = `
                    <div class="col-lg-4 col-md-6 mb-3" id="task-${data.id}">
                        <div class="card">
                            <div class="card-body">
                                <h5 class="card-title">${data.title}</h5>
                                <p class="card-text">${data.description}</p>
                                <a href="/update/${data.id}" class="btn btn-sm btn-primary">Update</a>
                                <a href="/delete/${data.id}" class="btn btn-sm btn-danger">Delete</a>
                            </div>
                        </div>
                    </div>
                `;
                
                // Add the new card to the container
                taskListContainer.insertAdjacentHTML('beforeend', newTaskHtml);

                // 4. Clear the form inputs
                addTaskForm.reset();
            }
        })
        .catch(error => console.error('Error:', error));
    });
});