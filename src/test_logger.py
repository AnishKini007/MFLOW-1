"""
Test file for logger.py module
"""
import sys
import os

# Add the src directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from logger import get_logger

def test_logger():
    """Test the logger functionality"""
    
    # Create a logger instance
    logger = get_logger("test_logger")
    
    # Test different log levels
    logger.info("This is an info message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")
    logger.debug("This is a debug message (might not appear due to level)")
    
    # Test logging with variables
    test_variable = "test_value"
    logger.info(f"Testing with variable: {test_variable}")
    
    # Test logging exceptions
    try:
        result = 10 / 0
    except ZeroDivisionError as e:
        logger.error(f"Caught an exception: {e}")
    
    print("Logger test completed. Check the logs directory for output.")

if __name__ == "__main__":
    test_logger()
