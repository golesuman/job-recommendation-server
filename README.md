# Job-recommendation-server
Backend for job recommendation algorithm and training

## Steps to run the project
1. Clone the repo 
2. Install all the requirements for the project by using the following command
    ```
    pip install -r requirements/requirements.txt
    ```
3. Change the directory to ```src``` by using ```cd src```

4. If you have made any changes to the models then run the command
    ```
    python manage.py makemigrations
    ```
5. Run the following command to migrate the changes to db
    ```
    python manage.py migrate
    ```
6. If you want to make the superuser use this command
   ```
      python manage.py createsuperuser
   ```
7. To start the server
    ```
    python manage.py runserver
    ```