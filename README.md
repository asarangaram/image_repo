# image_repo

How to start this server?

Create a virtual environment and install the packages from `requirement.txt`. set up mySQL server, create a database `image_repo_db` and associate it with a mysql user `image_repo_admin`. 

create a database `image_repo_db` and a user `image_repo_admin` on mysql.
give `image_repo_admin` permission to access `image_repo_db`
(you may use any name as long as they match environment variables below)

Setup the following environment variables. change the values as required.
```
export APP_NAME="Image Repo"
export MYSQL_IMAGE_REPO='image_repo_db'
export MYSQL_IMAGE_REPO_ADMIN='image_repo_admin'
export MYSQL_IMAGE_REPO_ADMIN_PW=<password>
# Do not use relative path
export FILE_STORAGE_LOCATION="/disks/data/image_repo"
```

# To start the server
```
source ~/.bashrc.image_repo
python src/wsgi.py
```

## To run tests

```
source ~/.bashrc.image_repo
cd test
python test_api.py
```

## DANGER ZONE, DON'T TRY ON DEPLOYED SERVER

to delete all the images from db, after starting the server,
```
http delete :5000/image/list
```
