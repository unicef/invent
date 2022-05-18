# Simple Feedback
Simple feedback is an [opensource library](https://github.com/pulilab/django-simple-feedback) that can be used as a simple ticketing system.
The plugin provides an API that can be utilized by the frontend application to create tickets.
When the ticket has been sent in, there are 2 ways to view them:

1. Django admin interface
2. Email notification

`settings.py` variable `SIMPLE_FEEDBACK_SEND_TO` can be set to an email address or a list of emails that will receive the tickets.

eg:
``` python
SIMPLE_FEEDBACK_SEND_TO = 'admin@example.org' 
or 
SIMPLE_FEEDBACK_SEND_TO = ['admin@example.org', 'another@example.org']
```
