import subprocess

def run_module(module_path):
    try:
        print(f"Running module at: {module_path}")
        subprocess.run(['python', module_path], check=True)
        print("Module completed.")
    except subprocess.CalledProcessError as e:
        print(f"Error running {module_path}:")
        print(e)

glass = "red"

if __name__ == "__main__":
    # Define paths to each module script
    module_paths = [
        '/Users/yanatsapalova/hci_lab/restarted/m1.py',
        '/Users/yanatsapalova/hci_lab/restarted/m2.py',
        '/Users/yanatsapalova/hci_lab/restarted/m3.py',
        '/Users/yanatsapalova/hci_lab/restarted/m5.1.py',
        '/Users/yanatsapalova/hci_lab/restarted/m5.py',
        '/Users/yanatsapalova/hci_lab/restarted/m8.py',
        '/Users/yanatsapalova/hci_lab/restarted/m7.py',
        '/Users/yanatsapalova/hci_lab/restarted/m6.py',
        '/Users/yanatsapalova/hci_lab/restarted/m9.py',
        '/Users/yanatsapalova/hci_lab/restarted/m11.py',
        '/Users/yanatsapalova/hci_lab/restarted/m10.py',
    ]

    # Run each module sequentially
    for module_path in module_paths:
        run_module(module_path)

    if (glass == "red"):
        run_module('/Users/yanatsapalova/hci_lab/restarted/angry.py')
    else:
        run_module('/Users/yanatsapalova/hci_lab/restarted/happy.py')

    print("All modules completed successfully.")
