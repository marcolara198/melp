# Melp

# 0.5 Install pre-commit
1. Install pre-commit https://pre-commit.com/#intro
2. Install the git hook scripts for docker
```bash
pre-commit install --config=.pre-commit-config.yaml
```
3. Run against all the files (optional)
```bash
pre-commit run --all-files --config=.pre-commit-config.yaml
```

### Rebuilding the docker image
```bash
docker compose build
docker compose run --rm django ./manage.py migrate;
docker compose run --rm django ./manage.py loaddata api/fixtures/initial_data.json;
docker compose run --rm django ./manage.py import_data;
```

### RUN
```bash
docker compose run --rm --service-ports django ./manage.py runserver 0.0.0.0:8000
```

### USERS
User basic authentication

superuser: admin admin

normal: test 123456

### Postman collection
melp.postman_collection
