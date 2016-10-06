# Predictive Analysis of Football Data
### Overview
This repo hosts the data and code involved in my final year project for DIT's Computer Science course, titled _Predictive Analysis of Football Data_.

It is set up as a Django project as I plan on making (where possible) the data collected available via an API for further research.

### Setup for local development
This repo can be cloned for local development if desired. I am using an Anaconda environment as this project involves data analysis, so I would recommend doing the same. Once the project is set up to use an Anaconda environment simply activate the environment and run `pip install -r requirements.txt` to install the Django requirements.

Run `python manage.py runscript populate_from_raw_data` to add data from the `raw_data` folder into the database.

### Data sources
The data used in this project has been sourced from

- [www.football-data.co.uk](www.football-data.co.uk/data.php)
- [www.sportinglife.com](www.sportinglife.com)
- [https://github.com/jokecamp/FootballData](https://github.com/jokecamp/FootballData)
- [https://www.kaggle.com/hugomathien/soccer](https://www.kaggle.com/hugomathien/soccer)

