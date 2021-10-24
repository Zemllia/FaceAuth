How to run:  
Open shell   
Go to project dir  
Run next commands:  
```shell
sudo chmod u+s run_doker.sh
./run_docker.sh
```

Then create new superuser:
```shell
docker-compose exec face_auth_web python manage.py createsuperuser
```
And follow instructions
