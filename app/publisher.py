import vk
import os

from time import sleep

from app import db
from app.models import Post


class Publisher:

    def __init__(self, user, group_id):

        self.user = user
        self.session = vk.AuthSession(os.environ['APP_ID'], self.user.username, self.user.password,
                                      scope='wall, photos, offline')
        self.api = vk.API(self.session)

        try:
            self.group_id = self.api.groups.getById(group_id=group_id)[0]['gid'] * -1
        except Exception as e:
            print(str(e))

    def publish(self, post):
        title = post.title
        url = post.url

        try:
            self.api.wall.post(owner_id=self.group_id, from_group=1, message=title, attachments=url)
            post.is_published = True
        except Exception as e:
            print(str(e))

        if post.is_published:
            db.session.add(post)
            db.session.commit()

    def post_loop(self):
        while True:
            posts = Post.query.filter_by(is_published=False).all()
            for post in posts:
                self.publish(post)
                # sleep for 30 minutes
                #sleep(60*30)
                sleep(60)
            else:
                sleep(60*30)

    def post_last(self):
        posts = Post.query.filter_by(is_published=False).all()
        if len(posts) > 0:
            post = posts[0]
            self.publish(post)
