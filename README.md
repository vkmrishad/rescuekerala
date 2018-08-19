# keralarescue

[![Build Status - Travis][0]][1] [![Open Source Helpers](https://www.codetriage.com/ieeekeralasection/rescuekerala/badges/users.svg)](https://www.codetriage.com/ieeekeralasection/rescuekerala)

The Website for coordinating the rehabilitation of the people affected in the 2018 Kerala Floods.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.


### Using Docker

- Only pre-requisite is having docker and docker-compose installed
- Execute `sh docker.sh` in this directory (if you do not have permissions on the `docker.sh`, do `chmod +x docker.sh`)
- Server will start running at `localhost:8000`
- `Ctrl+C` to stop

#### troubleshooting docker
* Incompatible docker version

 > ERROR: Version in "./docker-compose.yaml" is unsupported. You might be seeing this error because you're using the wrong Compose file version. Either specify a version of "2" (or "2.0") and place your service definitions under the `services` key, or omit the `version` key and place your service definitions at the root of the file to use version 1.
For more on the Compose file format versions, see https://docs.docker.com/compose/compose-file/


**Fix**

Update your docker toolkit

* Insufficient permissions
> ERROR: Couldn't connect to Docker daemon at http+docker://localunixsocket - is it running?
If it's at a non-standard location, specify the URL with the DOCKER_HOST environment variable.


**Fix**

Run it with sudo - `sudo sh docker.sh`


## Running natively
### Prerequisites

You will need to have following softwares in your system:

- [Python 3](https://www.python.org/downloads/)
- [Postgres](https://www.postgresql.org/download/)
- [Git](https://git-scm.com/downloads)
- [Redis](https://redis.io/)

### Installing

#### Setting up a development environment

1. Create database and user in Postgres for keralarescue and give privileges.

```
psql user=postgres
Password:
psql (10.4 (Ubuntu 10.4-0ubuntu0.18.04))
Type "help" for help.

postgres=# CREATE DATABASE rescuekerala;
CREATE DATABASE
postgres=# CREATE USER rescueuser WITH PASSWORD 'password';
CREATE ROLE
postgres=# GRANT ALL PRIVILEGES ON DATABASE rescuekerala TO rescueuser;
GRANT
postgres=# \q

```

2. Clone the repo.
```
git clone https://github.com/IEEEKeralaSection/rescuekerala.git
cd rescuekerala
```

3. Copy the sample environment file and configure it as per your local settings.

```
cp .env.example .env
```

Note: If you cannot copy the environment or you're facing any difficulty in starting the server, copy the settings file from
https://github.com/vigneshhari/keralarescue_test_settings for local testing.

3. Install dependencies.

```
pip3 install -r requirements.txt
```

4. Run database migrations.

```
python3 manage.py migrate
```

5. Setup static files.
```
python3 manage.py collectstatic
```


6. Run the server.

```
python3 manage.py runserver
```
7. Now open localhost:8000 in the browser

## Running tests

When running tests, Django creates a test replica of the database in order for the tests not to change the data on the real database. Because of that, you need to alter the Postgres user that you created and add to it the `CREATEDB` privilege:

```
ALTER USER rescueuser CREATEDB;
```

To run the tests, run this command:

```
python3 manage.py test --settings=floodrelief.test_settings
```

### Enable HTTPS connections

Certain features (example: GPS location collection) only work with HTTPS connections.  To enable HTTPS connections,follow the below steps.

Create self-signed certificate with openssl

```
$openssl req -x509 -newkey rsa:4096 -keyout key.key -out certificate.crt -days 365 -subj '/CN=localhost' -nodes
```
[https://stackoverflow.com/questions/10175812/how-to-create-a-self-signed-certificate-with-openssl#10176685]

Install django-sslserver

```
$pip3 install django-sslserver
```

Update INSTALLED_APPS with sslserver by editing the file floodrelief/settings.py (diff below)

```diff
 INSTALLED_APPS = [
+    'sslserver',
     'mainapp.apps.MainappConfig',
     'django.contrib.admin',
```
#### Note: Make sure that this change is removed before pushing your changes back to git
Run the server

```
python3 manage.py runsslserver 10.0.0.131:8002  --certificate /path/to/certificate.crt --key /path/to/key.key
```
In the above example the server is being run on a local IP address on port 8002 to enable HTTPS access from mobile/laptop/desktop for testing.

## How can you help?

### Contribution Guidelines
[Wiki](https://github.com/IEEEKeralaSection/rescuekerala/wiki/Contribution-Guidelines)

### By testing

We have a lot of [Pull Requests](https://github.com/IEEEKeralaSection/rescuekerala/pulls) that requires testing. Pick any PR that you like, try to reproduce the original issue and fix. Also join `#testing` channel in our slack and drop a note that you
are working on it.

## Testing Pull Requests
Note: If you have cloned a fork of IEEEKeralaSection/rescuekerala, replace ```origin``` with ```upstream```

1. Checkout the Pull Request you would like to test by
      ```
      git fetch origin pull/ID/head:BRANCHNAME`
      git checkout BRANCHNAME
     ```
2. Example
    ```
    git fetch origin pull/406/head:jaseem
    git checkout jaseem1
    ```
3. Run Migration

### Submitting Pull Requests

Please find issues that we need help [here](https://github.com/IEEEKeralaSection/rescuekerala/issues?q=is%3Aissue+is%3Aopen+label%3A%22help+wanted%22). Go through the comments in the issue to check if someone else is already working on it. Don't forget to drop a comment when you start working on it.

Always start your work in a new git branch. **Don't start to work on the
master branch**. Before you start your branch make sure you have the most
up-to-date version of the master branch then, make a branch that ideally
has the bug number in the branch name.

1. Before you begin, Fork the repository. This is needed as you might not have permission to push to the main repository

2. If you have already clone this repository, create a remote to track your fork by
     ```
     git remote add origin2 git@github.com:tessie/rescuekerala.git
     ```
3. If you have not yet cloned, clone your fork
    ```
    git clone git@github.com:tessie/rescuekerala.git
    ```
4. Checkout a new branch by
     ```
     git checkout -b issues_442
     ```
4. Make your changes.

5. Ensure your feature is working as expected.

6. Push your code.
      ```
      git push origin2 issues_442
      ```
7. Compare and create your pull request.

[0]: https://travis-ci.org/IEEEKeralaSection/rescuekerala.svg?branch=master
[1]: https://travis-ci.org/IEEEKeralaSection/rescuekerala


### Setting up s3 Account

- Follow https://django-storages.readthedocs.io/en/latest/backends/amazon-S3.html and https://www.caktusgroup.com/blog/2014/11/10/Using-Amazon-S3-to-store-your-Django-sites-static-and-media-files/ to setup s3 bucket, and download access keys.
