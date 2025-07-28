#!/usr/bin/env python3
"""
Sample Python Application
A simple web application demonstrating various Python features including:
- Flask web framework
- JSON APIs
- Data processing
- File operations
- Error handling
"""

from flask import Flask, jsonify, request, render_template_string
import json
import os
from datetime import datetime
from dataclasses import dataclass
from typing import List, Dict, Any
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

@dataclass
class Task:
    """Simple task data structure"""
    id: int
    title: str
    description: str
    completed: bool
    created_at: str

class TaskManager:
    """Simple task management class"""
    
    def __init__(self):
        self.tasks: List[Task] = []
        self.next_id = 1
        self.data_file = "tasks.json"
        self.load_tasks()
    
    def load_tasks(self):
        """Load tasks from JSON file"""
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r') as f:
                    data = json.load(f)
                    self.tasks = [Task(**task) for task in data.get('tasks', [])]
                    self.next_id = data.get('next_id', 1)
                logger.info(f"Loaded {len(self.tasks)} tasks from {self.data_file}")
        except Exception as e:
            logger.error(f"Error loading tasks: {e}")
            self.tasks = []
    
    def save_tasks(self):
        """Save tasks to JSON file"""
        try:
            data = {
                'tasks': [task.__dict__ for task in self.tasks],
                'next_id': self.next_id
            }
            with open(self.data_file, 'w') as f:
                json.dump(data, f, indent=2)
            logger.info(f"Saved {len(self.tasks)} tasks to {self.data_file}")
        except Exception as e:
            logger.error(f"Error saving tasks: {e}")
    
    def add_task(self, title: str, description: str = "") -> Task:
        """Add a new task"""
        task = Task(
            id=self.next_id,
            title=title,
            description=description,
            completed=False,
            created_at=datetime.now().isoformat()
        )
        self.tasks.append(task)
        self.next_id += 1
        self.save_tasks()
        return task
    
    def get_tasks(self) -> List[Task]:
        """Get all tasks"""
        return self.tasks
    
    def get_task(self, task_id: int) -> Task:
        """Get a specific task by ID"""
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None
    
    def update_task(self, task_id: int, **kwargs) -> Task:
        """Update a task"""
        task = self.get_task(task_id)
        if task:
            for key, value in kwargs.items():
                if hasattr(task, key):
                    setattr(task, key, value)
            self.save_tasks()
        return task
    
    def delete_task(self, task_id: int) -> bool:
        """Delete a task"""
        for i, task in enumerate(self.tasks):
            if task.id == task_id:
                del self.tasks[i]
                self.save_tasks()
                return True
        return False

# Initialize task manager
task_manager = TaskManager()

# HTML template for the web interface
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Python Sample App - Task Manager</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; background-color: #f5f5f5; }
        .container { max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        h1 { color: #333; text-align: center; margin-bottom: 30px; }
        .task-form { background: #f9f9f9; padding: 20px; border-radius: 5px; margin-bottom: 30px; }
        .task-form input, .task-form textarea { width: 100%; padding: 10px; margin: 5px 0; border: 1px solid #ddd; border-radius: 4px; box-sizing: border-box; }
        .task-form button { background: #007bff; color: white; padding: 10px 20px; border: none; border-radius: 4px; cursor: pointer; }
        .task-form button:hover { background: #0056b3; }
        .task { background: white; border: 1px solid #ddd; margin: 10px 0; padding: 15px; border-radius: 5px; }
        .task.completed { background: #f8f9fa; opacity: 0.7; }
        .task h3 { margin: 0 0 10px 0; color: #333; }
        .task p { margin: 0 0 10px 0; color: #666; }
        .task .meta { font-size: 12px; color: #999; }
        .task .actions { margin-top: 10px; }
        .task .actions button { margin-right: 10px; padding: 5px 15px; border: none; border-radius: 3px; cursor: pointer; }
        .complete-btn { background: #28a745; color: white; }
        .delete-btn { background: #dc3545; color: white; }
        .api-section { margin-top: 40px; padding-top: 20px; border-top: 2px solid #eee; }
        .endpoint { background: #f8f9fa; padding: 15px; margin: 10px 0; border-radius: 5px; border-left: 4px solid #007bff; }
        .method { font-weight: bold; color: #007bff; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🐍 Python Sample App - Task Manager</h1>
        
        <div class="task-form">
            <h2>Add New Task</h2>
            <form id="taskForm">
                <input type="text" id="title" placeholder="Task title" required>
                <textarea id="description" placeholder="Task description (optional)" rows="3"></textarea>
                <button type="submit">Add Task</button>
            </form>
        </div>
        
        <div id="tasks">
            <!-- Tasks will be loaded here -->
        </div>
        
        <div class="api-section">
            <h2>🔗 API Endpoints</h2>
            <div class="endpoint">
                <span class="method">GET</span> /api/tasks - Get all tasks
            </div>
            <div class="endpoint">
                <span class="method">POST</span> /api/tasks - Create a new task
            </div>
            <div class="endpoint">
                <span class="method">GET</span> /api/tasks/{id} - Get specific task
            </div>
            <div class="endpoint">
                <span class="method">PUT</span> /api/tasks/{id} - Update task
            </div>
            <div class="endpoint">
                <span class="method">DELETE</span> /api/tasks/{id} - Delete task
            </div>
            <div class="endpoint">
                <span class="method">GET</span> /api/stats - Get application statistics
            </div>
        </div>
    </div>

    <script>
        // Load tasks when page loads
        document.addEventListener('DOMContentLoaded', loadTasks);
        
        // Handle form submission
        document.getElementById('taskForm').addEventListener('submit', function(e) {
            e.preventDefault();
            const title = document.getElementById('title').value;
            const description = document.getElementById('description').value;
            
            fetch('/api/tasks', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ title: title, description: description })
            })
            .then(response => response.json())
            .then(data => {
                document.getElementById('title').value = '';
                document.getElementById('description').value = '';
                loadTasks();
            });
        });
        
        function loadTasks() {
            fetch('/api/tasks')
                .then(response => response.json())
                .then(tasks => {
                    const tasksDiv = document.getElementById('tasks');
                    tasksDiv.innerHTML = '<h2>📋 Tasks</h2>';
                    
                    if (tasks.length === 0) {
                        tasksDiv.innerHTML += '<p>No tasks yet. Add one above!</p>';
                        return;
                    }
                    
                    tasks.forEach(task => {
                        const taskDiv = document.createElement('div');
                        taskDiv.className = 'task' + (task.completed ? ' completed' : '');
                        taskDiv.innerHTML = `
                            <h3>${task.title}</h3>
                            <p>${task.description}</p>
                            <div class="meta">Created: ${new Date(task.created_at).toLocaleString()}</div>
                            <div class="actions">
                                <button class="complete-btn" onclick="toggleTask(${task.id}, ${!task.completed})">
                                    ${task.completed ? 'Mark Incomplete' : 'Mark Complete'}
                                </button>
                                <button class="delete-btn" onclick="deleteTask(${task.id})">Delete</button>
                            </div>
                        `;
                        tasksDiv.appendChild(taskDiv);
                    });
                });
        }
        
        function toggleTask(id, completed) {
            fetch(`/api/tasks/${id}`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ completed: completed })
            })
            .then(response => response.json())
            .then(data => loadTasks());
        }
        
        function deleteTask(id) {
            if (confirm('Are you sure you want to delete this task?')) {
                fetch(`/api/tasks/${id}`, { method: 'DELETE' })
                    .then(response => response.json())
                    .then(data => loadTasks());
            }
        }
    </script>
</body>
</html>
"""

# Routes
@app.route('/')
def index():
    """Main page with web interface"""
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    """Get all tasks"""
    try:
        tasks = task_manager.get_tasks()
        return jsonify([task.__dict__ for task in tasks])
    except Exception as e:
        logger.error(f"Error getting tasks: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/tasks', methods=['POST'])
def create_task():
    """Create a new task"""
    try:
        data = request.get_json()
        if not data or 'title' not in data:
            return jsonify({'error': 'Title is required'}), 400
        
        task = task_manager.add_task(
            title=data['title'],
            description=data.get('description', '')
        )
        return jsonify(task.__dict__), 201
    except Exception as e:
        logger.error(f"Error creating task: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    """Get a specific task"""
    try:
        task = task_manager.get_task(task_id)
        if not task:
            return jsonify({'error': 'Task not found'}), 404
        return jsonify(task.__dict__)
    except Exception as e:
        logger.error(f"Error getting task {task_id}: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    """Update a task"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        task = task_manager.update_task(task_id, **data)
        if not task:
            return jsonify({'error': 'Task not found'}), 404
        
        return jsonify(task.__dict__)
    except Exception as e:
        logger.error(f"Error updating task {task_id}: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    """Delete a task"""
    try:
        success = task_manager.delete_task(task_id)
        if not success:
            return jsonify({'error': 'Task not found'}), 404
        
        return jsonify({'message': 'Task deleted successfully'})
    except Exception as e:
        logger.error(f"Error deleting task {task_id}: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get application statistics"""
    try:
        tasks = task_manager.get_tasks()
        completed_tasks = [task for task in tasks if task.completed]
        
        stats = {
            'total_tasks': len(tasks),
            'completed_tasks': len(completed_tasks),
            'pending_tasks': len(tasks) - len(completed_tasks),
            'completion_rate': len(completed_tasks) / len(tasks) * 100 if tasks else 0,
            'app_info': {
                'name': 'Python Sample App',
                'version': '1.0.0',
                'description': 'A sample Python web application demonstrating Flask, data processing, and REST APIs'
            }
        }
        return jsonify(stats)
    except Exception as e:
        logger.error(f"Error getting stats: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("🐍 Starting Python Sample App...")
    print("📱 Features included:")
    print("   • Flask web server")
    print("   • REST API endpoints")
    print("   • Task management system")
    print("   • Data persistence (JSON)")
    print("   • Modern web interface")
    print("   • Error handling & logging")
    print("\n🌐 Access the app at: http://localhost:5000")
    print("📚 API documentation available at: http://localhost:5000")
    
    app.run(debug=True, host='0.0.0.0', port=5000)