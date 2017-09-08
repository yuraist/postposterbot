import vk

from app.models import User, Group, Post


class Publisher:

    def __init__(self, group):

        self.group = group

        vk.set_access_token(self.group.access_token)
        self.group = vk.get_group(self.group.name)

    def publish(self, post):
        title = post.title
        url = post.url
        self.group.wall_post(message=title, attachments=url)
