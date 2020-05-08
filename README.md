### How To Serve Flask Applications with Gunicorn and Nginx on Ubuntu 18.04
Create a virtual environment to store your Flask project’s Python requirements by typing:

#### Installation
<code>python3.6 -m venv myprojectenv</code>

Activate env source env/bin/activate

<code>source env/bin/activate</code>

Install required libraries

<code>pip install -r requirements.txt</code>

Install Flask and Gunicorn:

<code>pip install gunicorn flask</code>

##Configuring Gunicorn

Create a unit file ending in .service within the /etc/systemd/system directory to begin:

```
[Unit]
Description=Gunicorn instance to serve myproject
After=network.target

[Service]
User=bek
Group=www-data
WorkingDirectory=/home/bek/myproject
Environment="PATH=/home/bek/myproject/env/bin"
ExecStart=/home/bek/myproject/env/bin/gunicorn --workers 3 --bind unix:app.sock -m 007 wsgi:app

[Install]
WantedBy=multi-user.target
```

We can now start the Gunicorn service we created and enable it so that it starts at boot:

```
sudo systemctl start myproject
sudo systemctl enable myproject
```


