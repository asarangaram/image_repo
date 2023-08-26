# image_repo

## How to start this server?

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

now start the server, on a terminal window.
```
python -m src.wsgi
```

Note
:   we can run this as a service later

## How to start service?
as this is going to run on intranet, to help the clients to detect services
we need to broadcast with `avahi`.

If `avahi`` is not installed, install it

```
sudo apt install avahi-daemon avahi-utils
sudo systemctl restart avahi-daemon
```

The config file for avahi will be present at `/etc/avahi/avahi-daemon.conf`. As of now, there is no need to change anything.

Now publish the service, run the following in a terminal.
```
avahi-publish-service -s "CL IMAGE REPO" _image_repo_api._tcp 5000 "CL Image Repo Service"

```
To confirm this service is running, try the following in another terminal.
```
$ avahi-browse -r _image_repo_api._tcp
+ enp3s0 IPv4 CL IMAGE REPO                                 _image_repo_api._tcp local
+     lo IPv4 CL IMAGE REPO                                 _image_repo_api._tcp local
= enp3s0 IPv4 CL IMAGE REPO                                 _image_repo_api._tcp local
   hostname = [udesktop.local]
   address = [192.168.1.35]
   port = [5000]
   txt = ["CL Image Repo Service"]
=     lo IPv4 CL IMAGE REPO                                 _image_repo_api._tcp local
   hostname = [udesktop.local]
   address = [127.0.0.1]
   port = [5000]
   txt = ["CL Image Repo Service"]

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

# Client services
httpie's http can be used to interact.

## to upload a file
```
http -f POST :5000/image/upload image@<ImagePath>
```

## To upload a directory
```
find . -type f -exec echo "{}" \; -exec http -f POST :5000/image/upload image@"{}" \; |& tee ../upload4.log
```

## DANGER ZONE, DON'T TRY ON DEPLOYED SERVER

to delete all the images from db, after starting the server,
```
http delete :5000/image/list
```
