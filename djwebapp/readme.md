# Django iCloud Distance checker web app


## Start

```

python djwebapp\manage.py makemigrations
python djwebapp\manage.py migrate
python djwebapp\manage.py createsuperuser
```


### UNDER DEVELOP

```

python djwebapp\manage.py start -i admin


```
echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'pass')" | python manage.py shell
