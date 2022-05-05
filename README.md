# api-django
### Steps required to get up and running after cloning the repository.

- Create a new virtual environment.
  ```bash
  python3 -m venv env
  ```
- Activate the virtual envinronment.
  ```bash
  source env/bin/activate
  ```
- Install requirements form requirements.txt
- ```bash
  pip3 install -r requirements.txt
  ```
- Bash into the api_django_web container and run migrations.
  ```bash 
  docker exec -it containerid bash
  ```
- Run the migrations.
- ```bash
  python manage.py migrate
  ```
- Finally run the docker-compose file to spin up.
  ```bash
  docker-compose up
  ```