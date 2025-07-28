"""
Utility functions for the Python Sample App
Demonstrates various Python features and best practices
"""

import time
import functools
from contextlib import contextmanager
from typing import Callable, Any, Dict, List
import json
from datetime import datetime

def timer(func: Callable) -> Callable:
    """
    Decorator to measure function execution time
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"⏱️  {func.__name__} executed in {end_time - start_time:.4f} seconds")
        return result
    return wrapper

def validate_data(required_fields: List[str]) -> Callable:
    """
    Decorator to validate that required fields are present in function arguments
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Check if first argument is a dict (common pattern for data validation)
            if args and isinstance(args[0], dict):
                data = args[0]
                missing_fields = [field for field in required_fields if field not in data]
                if missing_fields:
                    raise ValueError(f"Missing required fields: {missing_fields}")
            return func(*args, **kwargs)
        return wrapper
    return decorator

@contextmanager
def file_operations(filename: str, mode: str = 'r'):
    """
    Context manager for safe file operations
    """
    file_handle = None
    try:
        print(f"📂 Opening file: {filename}")
        file_handle = open(filename, mode)
        yield file_handle
    except FileNotFoundError:
        print(f"❌ File not found: {filename}")
        raise
    except Exception as e:
        print(f"❌ Error with file {filename}: {e}")
        raise
    finally:
        if file_handle:
            file_handle.close()
            print(f"✅ Closed file: {filename}")

class DataProcessor:
    """
    Class demonstrating various data processing capabilities
    """
    
    @staticmethod
    @timer
    def process_list(data: List[Any], operation: str = "sum") -> Any:
        """
        Process a list of data with different operations
        """
        if not data:
            return None
            
        if operation == "sum" and all(isinstance(x, (int, float)) for x in data):
            return sum(data)
        elif operation == "average" and all(isinstance(x, (int, float)) for x in data):
            return sum(data) / len(data)
        elif operation == "max":
            return max(data)
        elif operation == "min":
            return min(data)
        elif operation == "count":
            return len(data)
        elif operation == "unique":
            return list(set(data))
        else:
            return data
    
    @staticmethod
    def filter_data(data: List[Dict], filters: Dict[str, Any]) -> List[Dict]:
        """
        Filter a list of dictionaries based on provided filters
        """
        if not filters:
            return data
        
        filtered_data = []
        for item in data:
            match = True
            for key, value in filters.items():
                if key not in item or item[key] != value:
                    match = False
                    break
            if match:
                filtered_data.append(item)
        
        return filtered_data
    
    @staticmethod
    def transform_data(data: List[Dict], transformations: Dict[str, Callable]) -> List[Dict]:
        """
        Apply transformations to data fields
        """
        transformed_data = []
        for item in data.copy():
            for field, transformation in transformations.items():
                if field in item:
                    try:
                        item[field] = transformation(item[field])
                    except Exception as e:
                        print(f"⚠️  Error transforming {field}: {e}")
            transformed_data.append(item)
        
        return transformed_data

def generate_sample_data(count: int = 10) -> List[Dict]:
    """
    Generate sample data for testing
    """
    import random
    
    names = ["Alice", "Bob", "Charlie", "Diana", "Eve", "Frank", "Grace", "Henry"]
    departments = ["Engineering", "Marketing", "Sales", "HR", "Finance"]
    
    data = []
    for i in range(count):
        data.append({
            "id": i + 1,
            "name": random.choice(names),
            "department": random.choice(departments),
            "salary": random.randint(40000, 120000),
            "experience": random.randint(1, 15),
            "created_at": datetime.now().isoformat()
        })
    
    return data

@validate_data(['name', 'age'])
def create_person(data: Dict) -> Dict:
    """
    Create a person record (demonstrates decorator usage)
    """
    return {
        **data,
        "id": hash(data['name']),
        "created_at": datetime.now().isoformat()
    }

def demonstrate_features():
    """
    Demonstrate various Python features implemented in this module
    """
    print("🎯 Demonstrating Python Features:")
    print("=" * 50)
    
    # 1. Data processing
    print("\n1. Data Processing:")
    sample_data = generate_sample_data(5)
    processor = DataProcessor()
    
    salaries = [person['salary'] for person in sample_data]
    print(f"   Average salary: ${processor.process_list(salaries, 'average'):,.2f}")
    print(f"   Max salary: ${processor.process_list(salaries, 'max'):,.2f}")
    
    # 2. Data filtering
    print("\n2. Data Filtering:")
    engineers = processor.filter_data(sample_data, {"department": "Engineering"})
    print(f"   Engineers found: {len(engineers)}")
    
    # 3. Data transformation
    print("\n3. Data Transformation:")
    transformed = processor.transform_data(
        sample_data,
        {"salary": lambda x: x * 1.1}  # 10% salary increase
    )
    print(f"   Applied 10% salary increase to {len(transformed)} records")
    
    # 4. Decorator usage
    print("\n4. Decorator Usage:")
    try:
        person = create_person({"name": "John", "age": 30})
        print(f"   Created person: {person['name']} (ID: {person['id']})")
    except ValueError as e:
        print(f"   Validation error: {e}")
    
    # 5. Context manager usage
    print("\n5. Context Manager Usage:")
    try:
        with file_operations("sample_data.json", "w") as f:
            json.dump(sample_data, f, indent=2)
        print("   Successfully wrote sample data to file")
    except Exception as e:
        print(f"   Error: {e}")

if __name__ == "__main__":
    demonstrate_features()