## Going Live

* Configure project settings for a production environment

* Use a PostgreSQL database

* Set up a web server with uWSGI and NGINX

* Serve static assets through NGINX

* Secure connections using SSL

* Use Daphne to serve Django Channels



### Multiple environment setting

#### Step 01:

Create a settings/ directory next to the `settings.py` file. Rename the `settings.py` file to `base.py`and move it into the new `settings/ `directory.

```
settings/
    __init__.py
    base.py
    local.py
    pro.py
```

These files are as follows:

* base.py : The base settings file that contains common settings (previously settings.py )
* local.py : Custom settings for your local environment
* pro.py : Custom settings for the production environment

#### Step 02:

Edit `settings/base.py`

```python
BASE_DIR = Path(__file__).resolve().parent.parent.parent
```

Edit `settings/local.py`

```python
from .base import *

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'test',
        'USER': 'test',
        'PASSWORD': 'test',
    }
    # 'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': BASE_DIR / 'db.sqlite3',
    # }
}
```

Edit `settings/pro.py`

```python
from .base import *

DEBUG = False
ADMINS = (
    ('sandeep', 'sandeep@gmail.com'),
)
ALLOWED_HOSTS = ['*']
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'test',
        'USER': 'test',
        'PASSWORD': 'test',
    }
}
```

Running with production ready setting 

`python manage.py runserver --settings=myblog.settings.pro`

OR

`export DJANGO_SETTINGS_MODULE=my_blog.settings.pro`



#### Step 03:

Checking project

`python manage.py check --deploy`



### Serving Django through WSGI

Django's primary deployment platform is WSGI. WSGI stands for **Web Server Gateway Interface** and it is the standard for serving Python applications on the web.

#### Step 01: Installing uWSGI

uWSGI is an extremely fast Python application server. It communicates with your Python application using the WSGI specification. uWSGI translates web requests into a format that your Django project can process.

In order to build uWSGI, you will need a C compiler, such as gcc or clang.

`apt-get install build-essential python3.8-dev` 

`pip install uwsgi==2.0.18`



#### Step 02: Configuring uWSGI

```bash
sudo uwsgi --module=my_blog.wsgi:application --env=DJANGO_SETTINGS_MODULE=my_blog.settings.pro --master --pidfile=/tmp/project-master.pid --http=127.0.0.1:8000 --uid=1000 --virtualenv=/home/sandeep/projects/django/env/d3be_blog/
```

**NOTE:** 

* If you are not running the command within the project directory, include the option
  `--chdir=/path/to/educa/` with the path to your project.
* You might have to prepend sudo to this command if you don't have the required permissions. 
* You might also need to add the `--plugin=python3`option if the module is not loaded by default.

#### Step 03: uWSGI custom configuration

uWSGI allows you to define a custom configuration in a .ini file. This is more convenient than passing options through the command line.

Create the following file structure inside the global my_blog/ directory:

```
config/
    uwsgi.ini
logs/
```

Edit the `config/uwsgi.ini`

```python
[uwsgi]
# variables
projectname = my_blog
base = /home/sandeep/projects/django/d3byexample/my_blog
# configuration
master = true
virtualenv = /home/sandeep/projects/django/env/d3be_blog
pythonpath = %(base)
chdir = %(base)
env = DJANGO_SETTINGS_MODULE=%(projectname).settings.pro
module = %(projectname).wsgi:application
socket = /tmp/%(projectname).sock
chmod-socket = 666
```

You can run uWSGI with your custom configuration using this command:
`uwsgi --ini config/uwsgi.ini`

**NOTE:** You will not be able to access your uWSGI instance from your browser now, since it's running through a socket. Let's complete the production environment.



### NGINX

When you are serving a website, you have to serve dynamic content, but you also need to serve static files, such as CSS style sheets, JavaScript files, and images. While uWSGI is capable of serving static files, it adds an unnecessary overhead to HTTP requests and therefore, it is encouraged to set up a web server, such as NGINX, in front of it.
NGINX is a web server focused on high concurrency, performance, and low memory usage. NGINX also acts as a reverse proxy, receiving HTTP requests and routing them to different backends. As mentioned, generally, you will use a web server, such as NGINX, in front of uWSGI for serving static files efficiently and quickly, and you will forward dynamic requests to uWSGI workers. By using NGINX, you can also apply rules and benefit from its reverse proxy capabilities.

#### Step 01: Installing NGINX

`sudo apt-get install nginx`

#### Step 02: Running NGINX

`sudo nginx`

#### Step 03: Configuring NGINX

Create a new file inside the config/ directory and name it `nginx.conf` .

```python
# the upstream component nginx needs to connect to
upstream my_blog {
    server          unix:///tmp/my_blog.sock;
}
server {
    listen          80;
    server_name     www.myblog.com myblog.com;
    access_log      off;
    error_log       /home/sandeep/projects/django/d3byexample/my_blog/logs/nginx_error.log;
    location / {
        include         /etc/nginx/uwsgi_params;
        uwsgi_pass      my_blog;
    }
}
```

You include the default uWSGI configuration parameters that come with NGINX. These are located next to the default configuration file for NGINX.
You can usually find them in any of these three locations: `/usr/local/nginx/conf/usgi_params` , `/etc/nginx/usgi_params` , or `/usr/local/etc/nginx/usgi_params` .

#### Step 04: Configuring NGINX

The default configuration file for NGINX is named nginx.conf and it usually resides in any of these three directories: 

`/usr/local/nginx/conf` , `/etc/nginx `, or `/usr/local/etc/nginx `.

Locate your `nginx.conf`configuration file and add the following include directive inside the http block:

`sudo nano /etc/nginx/nginx.conf`

```python
http {
    include /home/sandeep/projects/django/d3byexample/my_blog/config/nginx.conf;
}
```
#### Step 05: Run uWSGI

`uwsgi --ini config/uwsgi.ini`

#### Step 06: 

Open a second shell and reload NGINX with the following command:

`sudo nginx -s reload`

`sudo nginx -s quit`

#### Step 07: 

Since you are using a sample domain name, you need to redirect it to your local host. Edit your `/etc/hosts` file and add the following line to it:
`127.0.0.1 myblog.com www.myblog.com`
By doing so, you are routing both hostnames to your local server. In a production server, you won't need to do this, since you will have a fixed IP address and you will point your hostname to your server in your domain's DNS configuration.

#### Step 08:

Now you can restrict the hosts that can serve your Django project. Edit the production settings file settings/pro.py of your project and change the 	`ALLOWED_HOSTS` setting, as follows:

`ALLOWED_HOSTS = ['myblog.com', 'www.myblog.com']`

### Some Basic Commands

Checking port available or not

```
apt install net-tools
sudo netstat -plant | grep 80
```

```
systemctl status nginx
```

```
systemctl start nginx
```

```
systemctl enable nginx
```

```
systemctl restart nginx
```