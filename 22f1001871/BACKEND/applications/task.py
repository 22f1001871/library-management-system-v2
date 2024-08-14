from applications.workers import celery
from applications.user_datastore import user_datastore
from celery.schedules import crontab
from datetime import datetime, timedelta
from applications.models import *
from flask import url_for
from applications.send_mail import format_message, send_email
from sqlalchemy import desc
import requests
from jinja2 import Template
from weasyprint import HTML
from datetime import datetime
import csv, os
import logging


@celery.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
   sender.add_periodic_task(crontab(hour=1,minute=0,day_of_month=1), engagement.s(), name='Monthly Report')
   sender.add_periodic_task(crontab(hour=16,minute=0), daily_reminder.s(), name='daily reminders')


@celery.task()
def daily_reminder():
    now = datetime.now()
    
    # Query all users except those with id = 1
    users = USER.query.filter(USER.id != 1).all()
    
    for user in users:
        # Query books borrowed by the user
        books = BOOKS.query.filter_by(user_id=user.id).all()
        
        # Check if the user has not logged in for a day
        if user.last_login_at and (now - user.last_login_at).days >= 1:
            data = {'username': user.username}
            message = format_message('../FRONTEND/daily_reminder.html', data=data)
            send_email(user.email, subject="Reminder: Please check your e-books", message=message, content="html")
        
        # Check if any book is approaching its return date or overdue
        for book in books:
            if book.return_date and (book.return_date - now).days <= 1:
                data = {
                    'username': user.username,
                    'bookname': book.name,
                    'return_date': book.return_date
                }
                message = format_message('../FRONTEND/book_reminder.html', data=data)
                send_email(user.email, subject="Reminder: Return your book soon", message=message, content="html")


@celery.task()
def send_welcome_msg(data):
    message = format_message(
        "../FRONTEND/welcome_email.html", data=data
    )
    send_email(
        data['email_address'],
        subject="Welcome to the E-LIBRARY website",
        message=message,
        content="html",
    )



def format_report(template_file, user, month, books, year, filtered_book):
    with open(template_file) as file:
        template = Template(file.read())
        return template.render(user=user, month=month, books=books, year=year, filtered_book=filtered_book)

@celery.task
def engagement():
    logging.info("Starting engagement task")
    users = USER.query.filter(USER.id != 1).all()
    
    if not users:
        logging.warning("No users found in the database")
        return

    for user in users:
        logging.info(f"Processing user: {user.id} - {user.username}")
        result = monthly_engagement.delay(user.id)
        logging.info(f"Task for user {user.id} - {user.username} dispatched with result: {result}")

    logging.info("Engagement task completed")

@celery.task
def monthly_engagement(user_id):
    user = USER.query.filter_by(id=user_id).first()
    history = HISTORY.query.filter_by(user_id=user.id).all()
    rating = RATING.query.filter_by(uid=user.id).all()

    now = datetime.now()
    month = now.month
    year = now.year

    filtered_books = []
    for book in history:
        if book.date_requested.month == month and book.date_requested.year == year:
            ebook = BOOKS.query.filter_by(id=book.book_id).first()  # Ensure correct field reference
            section = SECTIONS.query.filter_by(id=ebook.section_id).first()
            filtered_books.append({'section': section, 'ebook': ebook, 'book': book})
            
    file_html = format_report('../FRONTEND/monthly_report.html', user=user, month=month, books=filtered_books, year=year, filtered_book=rating)
    html = HTML(string=file_html)
    filename = f'{user.username}_{month}_{year}.pdf'
    html.write_pdf(target=filename)

    data = {
        'username': user.username,
        'month': month,
        'year': year,
    }
    
    message = format_message("../FRONTEND/engagement_mail.html", data=data)
    send_email(
        user.email,
        subject=f"Monthly Engagement Report - {month}/{year}",
        message=message,
        content="html",
        attachment_file=filename
    )


@celery.task()
def webhook_message(message):
    url = "https://chat.googleapis.com/v1/spaces/AAAAkFHZRH0/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=6axDTGmldc81bT2AG6NzlNBY9cbyWngf2MukvZs4CvM%3D"
    payload = {"text": message}
    headers = {"Content-Type": "application/json; charset=UTF-8"}
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code != 200:
        print("Something went wrong")

        

@celery.task()
def export_csv(user_id):
    user = USER.query.filter_by(id = user_id).first()
    history = HISTORY.query.filter_by(user_id=user.id).all()
    with open(f"report_{user_id}.csv", "w", newline="") as csvfile:
        count=1
        csvwriter = csv.writer(csvfile, delimiter=",")
        csvwriter.writerow(["Sr No", "Book Id", "Description", "Date Requested","Date Accessed","Date Returned"])
        for i in history:
            csvwriter.writerow([count, i.book_id,i.description,i.date_requested,i.date_accessed,i.date_returned])
            count+=1

