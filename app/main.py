# main.py is the entry point for the application
# Streamlit will run this file when you run the command streamlit run main.py
import os

def main():
    current_pythonpath = os.environ.get('PYTHONPATH', '')  # Get the current PYTHONPATH or an empty string if not set
    new_path = "O:\\Documents\\Python_Projects\\stock_valuation"

    # Only add the new path if it's not already in PYTHONPATH
    if new_path not in current_pythonpath.split(os.pathsep):
        os.environ['PYTHONPATH'] = new_path + os.pathsep + current_pythonpath

    print(os.environ['PYTHONPATH'])

if __name__ == "__main__":
    main()