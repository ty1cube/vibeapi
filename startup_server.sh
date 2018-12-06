export DJANGO_SETTINGS_MODULE=vibespot.settings

sudo systemctl restart gunicorn.socket gunicorn.service
sudo systemctl restart nginx
