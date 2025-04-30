
import sys
import os

# Add 'code' folder to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), "code"))

# Now import your main function
import main

# Run the CLI-style prompt or pass arguments directly
if __name__ == "__main__":
    main.main()

