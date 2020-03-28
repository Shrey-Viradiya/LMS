release: python manage.py migrate && python manage.py process_tasks
web: gunicorn LMS.wsgi:application --log-file - --log-level debug
python manage.py collectstatic --noinput
manage.py migrate
