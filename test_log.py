import logging
import os

# Get the full path for the log file
log_file_path = os.path.join(os.getcwd(), 'test.log')
print(f"Attempting to write to: {log_file_path}")

try:
    # Configure logging to write to 'test.log'
    logging.basicConfig(
        level=logging.INFO,
        filename='test.log',
        filemode='w', # 'w' forces it to create a new file
        format='%(message)s'
    )

    # Write a single message
    logging.info("Hello, this is a test.")

    # Force the logger to write and close everything
    logging.shutdown()

    print("---")
    print("✅ Test complete. Please check the 'test.log' file.")

except Exception as e:
    print(f"\n❌ An error occurred during the logging test: {e}")
    print("This likely means a security setting or antivirus is blocking the script.")