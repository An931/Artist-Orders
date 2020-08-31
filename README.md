# Artist Orders


## Install requirements
```shell script
$ pip install -r requirements/development.txt
```

## Run a database
```shell script
$ docker-compose up -d postgres
```

## Apply migrations
```shell script
$ python3 manage.py migrate
```

### Create Superuser
```shell script
$ python3 manage.py createsuperuser
```

### Fill database
```shell script
$ python3 manage.py runscript fill_data
```

### Run server
```shell script
$ python3 manage.py runserver
```

### Run celery
```shell script
$ celery -A config worker -l info -B
```
