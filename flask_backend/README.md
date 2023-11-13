# Create Virtual Environment for installation
python -m venv anime_env

# Activate Virtual Environment
Windows: anime_env\Scripts\activate
Mac/Linux: source anime_env_linux/bin/activate

# Install packages
pipenv install -r requirements.txt

# Run Flask application
$env:FLASK_APP = "anime_flask"
flask run

# Basic commands for test database manipulation
flask db_create
flask db_seed
flask db_drop
