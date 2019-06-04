# sail_lanier
this project contains the source for the sail-lanier.com website.

## to run locally
create a python venv
```bash
python3 -m venv venv
. venv/bin/activate
pip install -r sail_lanier/requirements.txt
```

note that you must run `. venv/bin/activate` before interacting with manage.py

## to run with docker
build your docker container
```bash
docker build -t sail_lanier .
```

set up an alias to easily launch the docker container:
```bash
alias sail_lanier-shell='docker run -ti -e AWS_PROFILE=sail_lanier -v ~/projects/sail_lanier/sail_lanier/:/var/task -v ~/.aws/:/root/.aws -p 127.0.0.1:8000:8000 --rm sail_lanier'
```

run the shell
```bash
sail_lanier-shell
```

## create a fresh database
create a database
```bash
./manage.py migrate --settings=sail_lanier.settings.base
```

add an admin user
```bash
./manage.py createsuperuser --settings=sail_lanier.settings.base
```

## start the server
```bash
cd sail_lanier
./manage.py runserver --settings=sail_lanier.settings.base
```

if everything goes as planned your site should be available on http://127.0.0.1:8000/

# useful URLs
technologies this project makes use of:

https://github.com/Miserlou/Zappa

https://edgarroman.github.io/zappa-django-guide/setup/


# things preventing us from upgrading
zappa-django-utils requires python 3.6
django 2.2.1 requires sqlite 3.8.2, the lambci docker image uses 3.7.17 (use django 2.1.8 for now)
