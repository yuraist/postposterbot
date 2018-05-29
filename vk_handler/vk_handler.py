import os
import csv
import vk

from time import sleep
from app import db
from app.models import User, Group
from vk.exceptions import VkAPIError

class VkHandler:
    def __init__(self, username=None, password=None):
        """
        Creates a new instance of VkHandler with the API property.
        If the username and password are provided, an authorized session is created. If no – non authorized session.
        :param username: – a string username
        :param password: – a string password
        """
        if username and password:
            session = vk.AuthSession(os.environ['APP_ID'],
                                     user_login=username,
                                     user_password=password,
                                     scope='wall, photos, stats, groups, offline')

            self.API = vk.API(session=session, version='5.78')
        elif os.environ['VK_LOGIN'] and os.environ['VK_PASSWORD']:
            session = vk.AuthSession(os.environ['APP_ID'],
                                     user_login=os.environ['VK_LOGIN'],
                                     user_password=os.environ['VK_PASSWORD'],
                                     scope='wall, photos, stats, groups, offline')

            self.API = vk.API(session=session, version='5.78')
        else:
            self.API = vk.API(session=vk.Session())

    def get_group_follower_ids(self, group_id):
        """
        Returns user IDs for a specific group
        :param group_id: – an integer group id
        :return: – an array of integer follower IDs
        """

        # TODO: max count of users is 1000, so we need to upgrade the method to return more than 1000 follower IDs
        follower_ids = self.API.groups.getMembers(group_id=group_id, sort='id_asc')['users']
        return follower_ids

    def get_user_groups(self, user_id):
        """
        Returns group IDs for a specific user
        :param user_id: – an integer user ID
        :return: – an array of integer group IDs
        """
        group_ids = self.API.groups.get(user_id=user_id)
        return group_ids

    def get_most_similar_groups(self, group_id):

        # A dictionary with group id as key and count of common users as value
        groups = {}

        # An array of user IDs
        user_ids = self.get_group_follower_ids(group_id)

        print(f'There are {len(user_ids)} followers of your group.')

        # Find groups with common users
        for user_id in user_ids:
            # Wait for a some time to avoid the flood exception
            sleep(0.5)

            # Get user groups
            try:
                group_ids = self.get_user_groups(user_id)
                print(f'User {user_id} has {len(group_ids)} groups.\n')
            except:
                print('An error was acquired.')
                continue

            for gid in group_ids:
                if gid != group_ids:
                    # Increment the count of common users if the group already exists or create a new one
                    if gid in groups.keys():
                        groups[gid] += 1
                    else:
                        groups[gid] = 1

        return groups

    def save_group_and_count_to_file(self, group_id, count, filename='groups.csv'):
        if not os.path.exists(filename):
            with open(filename, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['Name', 'Common users', 'ID', 'URL'])

        group = self.API.groups.getById(group_id=str(group_id))[0]
        group_name = group['name']
        url = f'https://vk.com/club{group_id}'
        group_data = [group_name, count, group_id, url]

        with open(filename, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(group_data)

    def create_file_with_similar_groups(self, group_id):
        # TODO: get group id list, split it by 500 IDs, get extended information and save it into the file
        groups = self.get_most_similar_groups(group_id)
