import os
import csv
import vk

from time import sleep
from tqdm import tqdm
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

    def get_group_follower_ids(self, group_id, v=True):
        """
        Returns user IDs for a specific group
        :param group_id: – an integer group id
        :param v: – verbose mode. True by default
        :return: – an array of integer follower IDs
        """
        follower_ids = self.API.groups.getMembers(group_id=group_id, sort='id_asc')['users']

        # We are provided only to get 1000 IDs by one request, so we need to make more than one request
        while len(follower_ids) % 1000 == 0:
            new_ids = self.API.groups.getMembers(group_id=group_id, sort='id_asc', count=1000, offset=len(follower_ids))
            follower_ids += new_ids

        if not v:
            print(f'Total number of users: {len(follower_ids)}')
        return follower_ids

    def get_user_groups(self, user_id, v=True):
        """
        Returns group IDs for a specific user
        :param user_id: – an integer user ID
        :param v: – verbose mode. True by default
        :return: – an array of integer group IDs
        """
        group_ids = self.API.groups.get(user_id=user_id)

        if not v:
            print(f'User <id{user_id}> has {len(group_ids)} groups')
        return group_ids

    def get_most_similar_groups(self, group_id):

        # A dictionary with group id as key and count of common users as value
        groups = {}

        # An array of user IDs
        user_ids = self.get_group_follower_ids(group_id, v=False)

        # Find groups with common users
        for user_id in user_ids:
            # Wait for a some time to avoid the flood exception
            sleep(0.5)

            # Get user groups
            try:
                group_ids = self.get_user_groups(user_id, v=False)
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

    def save_group_and_count_to_file(self, group_id, count, filename='tmp/groups.csv'):
        """
        Creates a new file or open existing one and save extended group information into it
        :param group_id: – an integer group ID
        :param count: – an integer number of common users in the group
        :param filename: – a string name of file
        """

        # Create a new file if it doesn't exist
        if not os.path.exists(filename):
            with open(filename, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['Name', 'Common users', 'ID', 'URL'])

        # Get group by ID (returns an integer array)
        groups = self.API.groups.getById(group_id=group_id)

        with open(filename, 'a', newline='') as file:
            for group in groups:
                # Get extended group info
                group_name = group['name']
                url = f'https://vk.com/club{group_id}'
                group_data = [group_name, count, group_id, url]

                # Write the info into the file
                writer = csv.writer(file)
                writer.writerow(group_data)

    def create_file_with_similar_groups(self, group_id, v=True):
        """
        Selects the most similar groups for a group with group_id and creates csv file with the groups
        :param group_id: – an integer ID of a specific group
        :param v: – a boolean value for a verbose mode
        """

        # Get a dictionary with group IDs as keys and number of common users as values
        groups = self.get_most_similar_groups(group_id)

        # Save only the groups when the number of common users is more than 2
        filtered_groups = {k: v for (k, v) in groups.items() if v > 2}
        if not v:
            print(f'Total number of filtered groups is {len(filtered_groups)}')

        for id, count in tqdm(filtered_groups.items()):
            # Anti-flood
            sleep(0.3)
            self.save_group_and_count_to_file(group_id=id, count=count)

    @staticmethod
    def save_similar_groups_into_database(filename='tmp/groups.csv'):
        """
        Saves the group data from a .csv file into the database.
        :param filename: – a string name of .csv file with group information
        """
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            groups = list(reader)

            # An array of groups to save into the database
            group_instances = []

            # Fill the list of groups
            for group in tqdm(groups[1:]):
                name = group[0]
                common = group[1]
                gid = group[2]

                group_instance = Group(gid=gid)
                group_instance.name = name
                group_instance.common_users = common

                group_instances.append(group_instance)

            # Add all into the database
            db.session.add_all(group_instances)
            db.session.commit()
