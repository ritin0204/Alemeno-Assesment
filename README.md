# Assesment Set Up

1. SetUp the project using github link in your local repo/system by cloning/downloading the code.
2. Make sure your Docker, Python is installed on your system, it it's nnot installed, please refer to the official document to do so.
3. Start the container services with command.

   ```bash
   docker compose up -d
   ```
4. Perform the migrations to setup the database and load the initial data into the database.
5. ```bash
   docker compose exec web python manage.py makemigrations
   docker compose exec web python manage.py migrate
   docker compose exec web python manage.py import_data
   ```
