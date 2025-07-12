"""
Test file for custom_exception.py module
"""
import sys
import os

# Add the src directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from custom_exception import CustomException
from logger import get_logger

def test_custom_exception():
    """Test the custom exception functionality"""
    
    # Create a logger instance for testing
    logger = get_logger("test_custom_exception")
    
    # Test 1: Basic exception handling
    try:
        # This will cause a ZeroDivisionError
        result = 10 / 0
    except Exception as e:
        custom_exc = CustomException("Division by zero occurred", sys)
        logger.error(str(custom_exc))
    
    # Test 2: FileNotFoundError
    try:
        with open("nonexistent_file.txt", "r") as f:
            content = f.read()
    except Exception as e:
        custom_exc = CustomException("File not found error", sys)
        logger.error(str(custom_exc))
    
    # Test 3: Index error
    try:
        test_list = [1, 2, 3]
        value = test_list[10]  # Index out of range
    except Exception as e:
        custom_exc = CustomException("Index out of range error", sys)
        logger.error(str(custom_exc))
    
    # Test 4: Type error
    try:
        result = "string" + 5  # Type error
    except Exception as e:
        custom_exc = CustomException("Type error occurred", sys)
        logger.error(str(custom_exc))
    
    # Test 5: Custom function that raises exception
    def divide_numbers(a, b):
        try:
            return a / b
        except Exception as e:
            raise CustomException("Error in divide_numbers function", sys)
    
    try:
        result = divide_numbers(10, 0)
    except CustomException as e:
        logger.error(str(e))

if __name__ == "__main__":
    test_custom_exception()
