Install all the required python modules from requirement.txt using the following command pip install -r requirements.txt
To run frontend
$ cd <your-project-name>
$ npm install
$ npm run dev
Run MailHog server on Ubuntu Terminal: ~/go/bin/MailHog
Run Celery Worker on Ubuntu Terminal: celery -A main.celery worker -l info
Run Celery beat Scheduler on Ubuntu Terminal: celery -A main.celery beat --max-interval 1 -l info