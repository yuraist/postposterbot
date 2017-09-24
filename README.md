# Post Poster Bot

### About the service

The content search automation, scheduled publications and analytics service for communities in social media.
Post Poster is just looking for a content on the websites you choose. Today our service is in development and testing 
on the iOS developers community ([iOStory](https://vk.com/iostory)).
The bot is searching for articles and publish them into the group. 

### Frameworks, libraries and other technologies we use

 + In core of the Post Poster Bot is Python-microframework for web application - [Flask](https://github.com/pallets/flask).
It makes possible to deploy online app very fast.
 + The [Beautiful Soup 4](https://pypi.python.org/pypi/beautifulsoup4) library helps to parse the data received from websites. 
 + PostgreSQL + [Flask-SQLAlchemy](https://github.com/mitsuhiko/flask-sqlalchemy) is used for data storing and management.
 + We use the [Flask-Security](https://github.com/mattupstate/flask-security) library to quickly add secure features 
(like user authorization) in our service. We need this funcitonality for our CMS.
 + Post publishing and community analytics requires access to group information. Access is via VK API. For quick work with the API
   we user the [vk](https://github.com/dimka665/vk) python library. 
 + Redis Queue is used for async tasks like content searching and post publishing.
 + We use [Heroku](heroku.com) cloud-service for running our application.

#### [Our website](https://postposterbot.herokuapp.com/) 
