# sail_lanier

this project contains the source for the sail-lanier.com website.

## to run locally

create a python venv

```bash
python3 -m venv venv
. venv/bin/activate
pip install -r requirements.txt
```

### if you want to use docker

```bash
docker build -t sail_lanier .  # add --no-cache to force a complete rebuild
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

note that you must run `. venv/bin/activate` before interacting with manage.py

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
./manage.py runserver --settings=sail_lanier.settings.base 0.0.0.0:8000  # remove 0.0.0.0:8000 to only listen on localhost
```

if everything goes as planned your site should be available on http://127.0.0.1:8000/

## managing the production instance

in order to manage the production and development instance, you must have AWS IAM credentials and the `prod.py` or
`dev.py` config file.

to update the lambda function

```bash
zappa update prod
```

to update static files

```bash
AWS_PROFILE=sail-lanier ./manage.py collectstatic --settings=sail_lanier.settings.dev
AWS_PROFILE=sail-lanier ./manage.py collectstatic --settings=sail_lanier.settings.prod
```

to vacuum sqlite

```bash
zappa manage prod s3_sqlite_vacuum
```

before upgrading Django version, run

```bash
python -Wa manage.py test --settings=sail_lanier.settings.base
```

## useful URLs

technologies this project makes use of:

* https://www.djangoproject.com/
* https://github.com/Miserlou/Zappa
* https://edgarroman.github.io/zappa-django-guide/setup/
