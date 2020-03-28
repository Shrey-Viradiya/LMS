release: python manage.py process_task
web: gunicorn LMS.wsgi:application --log-file - --log-level debug
python manage.py collectstatic --noinput
manage.py migrate
