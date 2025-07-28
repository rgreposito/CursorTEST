#!/usr/bin/env python3
"""
Test suite for the Python Sample App
Demonstrates testing best practices with unittest
"""

import unittest
import json
import tempfile
import os
from unittest.mock import patch, MagicMock
from app import TaskManager, Task
from utils import DataProcessor, generate_sample_data, create_person

class TestTaskManager(unittest.TestCase):
    """Test cases for TaskManager class"""
    
    def setUp(self):
        """Set up test fixtures before each test method"""
        # Create a temporary file for testing
        self.temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json')
        self.temp_file.close()
        
        # Initialize TaskManager with temporary file
        self.task_manager = TaskManager()
        self.task_manager.data_file = self.temp_file.name
        self.task_manager.tasks = []
        self.task_manager.next_id = 1
    
    def tearDown(self):
        """Clean up after each test method"""
        # Remove temporary file
        if os.path.exists(self.temp_file.name):
            os.unlink(self.temp_file.name)
    
    def test_add_task(self):
        """Test adding a new task"""
        task = self.task_manager.add_task("Test Task", "Test Description")
        
        self.assertIsInstance(task, Task)
        self.assertEqual(task.title, "Test Task")
        self.assertEqual(task.description, "Test Description")
        self.assertFalse(task.completed)
        self.assertEqual(task.id, 1)
        self.assertEqual(len(self.task_manager.tasks), 1)
    
    def test_get_tasks(self):
        """Test getting all tasks"""
        # Add some tasks
        self.task_manager.add_task("Task 1", "Description 1")
        self.task_manager.add_task("Task 2", "Description 2")
        
        tasks = self.task_manager.get_tasks()
        self.assertEqual(len(tasks), 2)
        self.assertEqual(tasks[0].title, "Task 1")
        self.assertEqual(tasks[1].title, "Task 2")
    
    def test_get_task_by_id(self):
        """Test getting a specific task by ID"""
        task = self.task_manager.add_task("Test Task", "Test Description")
        
        retrieved_task = self.task_manager.get_task(task.id)
        self.assertIsNotNone(retrieved_task)
        self.assertEqual(retrieved_task.title, "Test Task")
        
        # Test non-existent task
        non_existent = self.task_manager.get_task(999)
        self.assertIsNone(non_existent)
    
    def test_update_task(self):
        """Test updating a task"""
        task = self.task_manager.add_task("Original Title", "Original Description")
        
        updated_task = self.task_manager.update_task(
            task.id, 
            title="Updated Title", 
            completed=True
        )
        
        self.assertIsNotNone(updated_task)
        self.assertEqual(updated_task.title, "Updated Title")
        self.assertTrue(updated_task.completed)
        self.assertEqual(updated_task.description, "Original Description")  # Unchanged
    
    def test_delete_task(self):
        """Test deleting a task"""
        task = self.task_manager.add_task("Task to Delete", "Description")
        task_id = task.id
        
        # Verify task exists
        self.assertIsNotNone(self.task_manager.get_task(task_id))
        
        # Delete task
        success = self.task_manager.delete_task(task_id)
        self.assertTrue(success)
        
        # Verify task is deleted
        self.assertIsNone(self.task_manager.get_task(task_id))
        self.assertEqual(len(self.task_manager.tasks), 0)
    
    def test_save_and_load_tasks(self):
        """Test saving and loading tasks from file"""
        # Add some tasks
        task1 = self.task_manager.add_task("Task 1", "Description 1")
        task2 = self.task_manager.add_task("Task 2", "Description 2")
        
        # Create new TaskManager instance with same file
        new_manager = TaskManager()
        new_manager.data_file = self.temp_file.name
        new_manager.load_tasks()
        
        # Verify tasks were loaded
        self.assertEqual(len(new_manager.tasks), 2)
        self.assertEqual(new_manager.tasks[0].title, "Task 1")
        self.assertEqual(new_manager.tasks[1].title, "Task 2")
        self.assertEqual(new_manager.next_id, 3)

class TestDataProcessor(unittest.TestCase):
    """Test cases for DataProcessor class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.processor = DataProcessor()
        self.sample_numbers = [1, 2, 3, 4, 5]
        self.sample_data = [
            {"name": "Alice", "department": "Engineering", "salary": 75000},
            {"name": "Bob", "department": "Marketing", "salary": 65000},
            {"name": "Charlie", "department": "Engineering", "salary": 80000},
        ]
    
    def test_process_list_sum(self):
        """Test list processing with sum operation"""
        result = self.processor.process_list(self.sample_numbers, "sum")
        self.assertEqual(result, 15)
    
    def test_process_list_average(self):
        """Test list processing with average operation"""
        result = self.processor.process_list(self.sample_numbers, "average")
        self.assertEqual(result, 3.0)
    
    def test_process_list_max(self):
        """Test list processing with max operation"""
        result = self.processor.process_list(self.sample_numbers, "max")
        self.assertEqual(result, 5)
    
    def test_process_list_min(self):
        """Test list processing with min operation"""
        result = self.processor.process_list(self.sample_numbers, "min")
        self.assertEqual(result, 1)
    
    def test_process_list_count(self):
        """Test list processing with count operation"""
        result = self.processor.process_list(self.sample_numbers, "count")
        self.assertEqual(result, 5)
    
    def test_process_list_unique(self):
        """Test list processing with unique operation"""
        data_with_duplicates = [1, 2, 2, 3, 3, 3]
        result = self.processor.process_list(data_with_duplicates, "unique")
        self.assertEqual(sorted(result), [1, 2, 3])
    
    def test_process_list_empty(self):
        """Test list processing with empty list"""
        result = self.processor.process_list([], "sum")
        self.assertIsNone(result)
    
    def test_filter_data(self):
        """Test data filtering"""
        filters = {"department": "Engineering"}
        result = self.processor.filter_data(self.sample_data, filters)
        
        self.assertEqual(len(result), 2)
        self.assertTrue(all(item["department"] == "Engineering" for item in result))
    
    def test_filter_data_no_filters(self):
        """Test data filtering with no filters"""
        result = self.processor.filter_data(self.sample_data, {})
        self.assertEqual(len(result), 3)
        self.assertEqual(result, self.sample_data)
    
    def test_transform_data(self):
        """Test data transformation"""
        transformations = {"salary": lambda x: x * 1.1}  # 10% increase
        result = self.processor.transform_data(self.sample_data.copy(), transformations)
        
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0]["salary"], 82500)  # 75000 * 1.1
        self.assertEqual(result[1]["salary"], 71500)  # 65000 * 1.1

class TestUtilityFunctions(unittest.TestCase):
    """Test cases for utility functions"""
    
    def test_generate_sample_data(self):
        """Test sample data generation"""
        data = generate_sample_data(5)
        
        self.assertEqual(len(data), 5)
        self.assertTrue(all("id" in item for item in data))
        self.assertTrue(all("name" in item for item in data))
        self.assertTrue(all("department" in item for item in data))
        self.assertTrue(all("salary" in item for item in data))
    
    def test_create_person_valid_data(self):
        """Test person creation with valid data"""
        person_data = {"name": "John", "age": 30}
        person = create_person(person_data)
        
        self.assertEqual(person["name"], "John")
        self.assertEqual(person["age"], 30)
        self.assertIn("id", person)
        self.assertIn("created_at", person)
    
    def test_create_person_missing_fields(self):
        """Test person creation with missing required fields"""
        with self.assertRaises(ValueError):
            create_person({"name": "John"})  # Missing age
        
        with self.assertRaises(ValueError):
            create_person({"age": 30})  # Missing name

class TestIntegration(unittest.TestCase):
    """Integration tests for the complete application"""
    
    def setUp(self):
        """Set up integration test fixtures"""
        self.temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json')
        self.temp_file.close()
        
        self.task_manager = TaskManager()
        self.task_manager.data_file = self.temp_file.name
        self.task_manager.tasks = []
        self.task_manager.next_id = 1
    
    def tearDown(self):
        """Clean up integration test fixtures"""
        if os.path.exists(self.temp_file.name):
            os.unlink(self.temp_file.name)
    
    def test_complete_workflow(self):
        """Test a complete task management workflow"""
        # 1. Add multiple tasks
        task1 = self.task_manager.add_task("Learn Python", "Study Python fundamentals")
        task2 = self.task_manager.add_task("Build Web App", "Create a Flask application")
        task3 = self.task_manager.add_task("Write Tests", "Add comprehensive test coverage")
        
        # 2. Verify all tasks were added
        self.assertEqual(len(self.task_manager.get_tasks()), 3)
        
        # 3. Complete some tasks
        self.task_manager.update_task(task1.id, completed=True)
        self.task_manager.update_task(task3.id, completed=True)
        
        # 4. Verify task states
        updated_task1 = self.task_manager.get_task(task1.id)
        updated_task2 = self.task_manager.get_task(task2.id)
        updated_task3 = self.task_manager.get_task(task3.id)
        
        self.assertTrue(updated_task1.completed)
        self.assertFalse(updated_task2.completed)
        self.assertTrue(updated_task3.completed)
        
        # 5. Delete a task
        self.task_manager.delete_task(task2.id)
        self.assertEqual(len(self.task_manager.get_tasks()), 2)
        
        # 6. Verify persistence
        new_manager = TaskManager()
        new_manager.data_file = self.temp_file.name
        new_manager.load_tasks()
        
        self.assertEqual(len(new_manager.get_tasks()), 2)
        remaining_tasks = new_manager.get_tasks()
        completed_tasks = [task for task in remaining_tasks if task.completed]
        self.assertEqual(len(completed_tasks), 2)

def run_tests():
    """Run all tests and display results"""
    print("🧪 Running Python Sample App Tests")
    print("=" * 50)
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test classes
    suite.addTests(loader.loadTestsFromTestCase(TestTaskManager))
    suite.addTests(loader.loadTestsFromTestCase(TestDataProcessor))
    suite.addTests(loader.loadTestsFromTestCase(TestUtilityFunctions))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegration))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print(f"\n📊 Test Results:")
    print(f"   Tests run: {result.testsRun}")
    print(f"   Failures: {len(result.failures)}")
    print(f"   Errors: {len(result.errors)}")
    print(f"   Success rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%")
    
    return result.wasSuccessful()

if __name__ == "__main__":
    success = run_tests()
    exit(0 if success else 1)