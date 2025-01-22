import os

def check_structure():
    required_paths = [
        'templates',
        'templates/index.html',
        'static',
        'static/css',
        'static/css/style.css',
        'static/js',
        'static/js/game.js',
        'app.py'
    ]
    
    missing = []
    for path in required_paths:
        if not os.path.exists(path):
            missing.append(path)
    
    if missing:
        print("Missing files/folders:")
        for item in missing:
            print(f"- {item}")
        print("\nPlease create these files/folders to fix the error.")
    else:
        print("All required files and folders are present!")
        
if __name__ == "__main__":
    check_structure()