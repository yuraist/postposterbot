# Post Poster Bot

### About

The Post Poster Bot helps you to automatically search content for your projects, such a Facebook page, or website. It'll also provide scheduled publications and analyzis services for your media. 

Now Post Poster Bot is only looking for a content on the websites you choose. We're developing and testing it 
on the mobile developers community ([The Real Talk](https://vk.com/therealtalkme)). The application looks for thematic articles for our community and automatically posts them onto the page.

### What we use

 + In the core of the Post Poster Bot is Python-microframework for web application - [Flask](https://github.com/pallets/flask).
It makes possible to deploy online app very fast.
 + The [Beautiful Soup 4](https://pypi.python.org/pypi/beautifulsoup4) library helps to parse the data received from websites. 
 + PostgreSQL + [Flask-SQLAlchemy](https://github.com/mitsuhiko/flask-sqlalchemy) is used for data storing and management.
 + We use the [Flask-Security](https://github.com/mattupstate/flask-security) library to quickly add secure features 
(like user authorization) in our service. We need this funcitonality for our CMS.
 + Post publishing and community analytics require access to group information. Access is via VK API. For quick work with the API
   we user the [vk](https://github.com/dimka665/vk) python library. 
 + Redis Queue used for async tasks like content searching and post publishing.
 + We use [Heroku](heroku.com) cloud-service for running our application.

#### [Our website](https://postposterbot.herokuapp.com/) (Now is unavailable)
