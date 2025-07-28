# 🐍 Python Sample Application

A comprehensive Python web application demonstrating modern development practices, built with Flask and featuring a task management system.

## ✨ Features

- **Web Application**: Modern Flask-based web server with REST API
- **Task Management**: Create, read, update, and delete tasks with persistence
- **Beautiful UI**: Clean, responsive web interface with interactive JavaScript
- **Data Processing**: Advanced data manipulation and processing utilities
- **Testing Suite**: Comprehensive test coverage with unittest
- **Error Handling**: Robust error handling and logging throughout
- **Type Hints**: Modern Python with type annotations
- **Documentation**: Well-documented code with docstrings

## 🚀 Quick Start

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

### Installation

1. **Clone or navigate to the repository**
   ```bash
   cd /path/to/your/workspace
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python app.py
   ```

4. **Open your browser**
   Visit [http://localhost:5000](http://localhost:5000) to access the application

## 📚 Project Structure

```
.
├── app.py              # Main Flask application
├── utils.py            # Utility functions and data processing
├── tests.py            # Comprehensive test suite
├── requirements.txt    # Python dependencies
├── README.md          # This file
└── tasks.json         # Data persistence file (created automatically)
```

## 🔧 Usage

### Web Interface

The application provides a beautiful web interface at `http://localhost:5000` where you can:

- **Add Tasks**: Create new tasks with titles and descriptions
- **View Tasks**: See all your tasks in a clean, organized list
- **Complete Tasks**: Mark tasks as completed or incomplete
- **Delete Tasks**: Remove tasks you no longer need
- **View API Documentation**: See all available API endpoints

### REST API

The application exposes a RESTful API with the following endpoints:

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/tasks` | Get all tasks |
| POST | `/api/tasks` | Create a new task |
| GET | `/api/tasks/{id}` | Get a specific task |
| PUT | `/api/tasks/{id}` | Update a task |
| DELETE | `/api/tasks/{id}` | Delete a task |
| GET | `/api/stats` | Get application statistics |

#### Example API Usage

```bash
# Get all tasks
curl http://localhost:5000/api/tasks

# Create a new task
curl -X POST http://localhost:5000/api/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Learn Python", "description": "Study Python fundamentals"}'

# Update a task
curl -X PUT http://localhost:5000/api/tasks/1 \
  -H "Content-Type: application/json" \
  -d '{"completed": true}'

# Get statistics
curl http://localhost:5000/api/stats
```

### Command Line Usage

You can also run individual modules:

```bash
# Demonstrate utility functions
python utils.py

# Run the test suite
python tests.py
```

## 🧪 Testing

The application includes a comprehensive test suite covering:

- **Unit Tests**: Individual component testing
- **Integration Tests**: End-to-end workflow testing
- **Data Processing Tests**: Utility function validation
- **Error Handling Tests**: Edge case and error scenarios

Run the tests:

```bash
python tests.py
```

Expected output:
```
🧪 Running Python Sample App Tests
==================================================
test_add_task (tests.TestTaskManager) ... ok
test_delete_task (tests.TestTaskManager) ... ok
...
📊 Test Results:
   Tests run: 20
   Failures: 0
   Errors: 0
   Success rate: 100.0%
```

## 🎯 Key Python Concepts Demonstrated

### 1. Object-Oriented Programming
- Classes and inheritance
- Data classes with `@dataclass` decorator
- Instance and static methods

### 2. Modern Python Features
- Type hints with `typing` module
- Context managers with `@contextmanager`
- Decorators for validation and timing
- F-strings for string formatting

### 3. Web Development
- Flask web framework
- RESTful API design
- JSON data handling
- HTML templating

### 4. Data Handling
- File I/O operations
- JSON serialization/deserialization
- Data filtering and transformation
- Error handling with try/catch

### 5. Testing Best Practices
- Unit testing with `unittest`
- Test fixtures and cleanup
- Mocking external dependencies
- Integration testing

### 6. Code Quality
- Comprehensive logging
- Error handling
- Documentation with docstrings
- Code organization and modularity

## 🔧 Configuration

The application can be configured by modifying these settings in `app.py`:

```python
# Server configuration
app.run(debug=True, host='0.0.0.0', port=5000)

# Data file location
data_file = "tasks.json"

# Logging level
logging.basicConfig(level=logging.INFO)
```

## 📈 Architecture

The application follows a clean architecture pattern:

1. **Presentation Layer** (`app.py` routes): Handles HTTP requests and responses
2. **Business Logic Layer** (`TaskManager` class): Manages core application logic
3. **Data Layer** (`JSON file persistence`): Handles data storage and retrieval
4. **Utility Layer** (`utils.py`): Provides reusable functions and data processing

## 🛠️ Development

### Adding New Features

1. **Add business logic** to the `TaskManager` class or create new classes
2. **Create API endpoints** in `app.py` following RESTful conventions
3. **Add utility functions** in `utils.py` for data processing
4. **Write tests** in `tests.py` for new functionality
5. **Update documentation** in this README

### Code Style

The code follows Python best practices:

- PEP 8 style guidelines
- Type hints for better code clarity
- Comprehensive docstrings
- Error handling and logging
- Modular design with separation of concerns

## 🤝 Contributing

This is a sample application for learning purposes. Feel free to:

- Fork the repository and experiment
- Add new features and functionality
- Improve the UI/UX design
- Add more comprehensive tests
- Optimize performance

## 📄 License

This project is provided as-is for educational purposes. Feel free to use, modify, and distribute as needed.

## 🎓 Learning Resources

To learn more about the technologies used in this application:

- **Python**: [python.org](https://python.org)
- **Flask**: [flask.palletsprojects.com](https://flask.palletsprojects.com)
- **Type Hints**: [docs.python.org/3/library/typing.html](https://docs.python.org/3/library/typing.html)
- **Testing**: [docs.python.org/3/library/unittest.html](https://docs.python.org/3/library/unittest.html)

---

**Happy coding! 🐍✨**