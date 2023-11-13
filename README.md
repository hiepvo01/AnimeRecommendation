# Anime-Recommender-System

This project uses Angular, FLask Python and SQLite to create a user friendly anime website.

Since the SQLite data file is too big for github repo (> 1 Gb), here is the source code pushed to gitlab that includes SQLite database:

https://gitlab.com/hiep.vo/animeangular

## Demo

https://www.youtube.com/watch?v=AAU1WYZCmIs&t=120s&ab_channel=HiepVo

## Run Angular frontend
cd anime-app
npm install
ng serve

## Run flask backend
cd flask_backend

### Create environment
python -m venv anime_env

### Activate Environment
Windows: anime_env\Scripts\activate 

Mac/Linux: source anime_env_linux/bin/activate

### Install Packages
pipenv install -r requirements.txt

### Run flask backend
python run.py
