import datetime
from peewee import *
import discord
from discord.ext import commands
from discord import utils
import random
import time
import requests
from VenvData import *


class Report:
    def __init__(self, state, data, note):
        self.state = state
        self.data = data
        self.note = note

    def print(self):
        print(f"{self.state} {self.data} {self.note} {datetime.datetime.now()}")


class DataBase:
    def __init__(self, name):
        self.name = name

    def generate(self):
        return SqliteDatabase(f'{self.name}.db')

    # создание базы данных
    def create(self, *args):
        with self.generate() as db:
            db.create_tables([*args])

    # управление директориями
    def set_directory(self, server_id: int, server_name: str, console_id: int, log_id: int, info_id: int):
        with self.generate() as db:
            try:
                current_dirs = Directory.get(Directory.server_id == server_id)
                current_dirs.server_name = server_name
                current_dirs.console_id = console_id
                current_dirs.log_id = log_id
                current_dirs.info_id = info_id
                current_dirs.save()
                return Report(True, None, 'set_directory [update]')
            except:
                Directory.create(server_id=server_id, server_name=server_name, console_id=console_id, log_id=log_id,
                                 info_id=info_id)
                return Report(True, None, 'set_directory [insert]')

    def get_directory(self, server_id: int):
        with self.generate() as db:
            try:
                current_dirs = Directory.get(Directory.server_id == server_id)
                return Report(True, (current_dirs.console_id, current_dirs.log_id, current_dirs.info_id),
                              'get_directory [exists]')
            except:
                return Report(True, (-1, -1, -1), 'get_directory [None]')

    # управление рейтингом
    def set_rating(self, server_id: int, user_id: int, score: int):
        with self.generate() as db:
            try:
                current_user = User.get(User.server_id == server_id, User.user_id == user_id)
                current_user.score = score
                current_user.save()
                return Report(True, None, 'set_rating [id]')
            except:
                return Report(False, None, 'set_rating [no user!]')

    def new_user(self, server_id: int, server_name: str, user_id: int, user_name: str, score: int):
        with self.generate() as db:
            try:
                current_user = User.get(User.server_id == server_id, User.user_id == user_id)
                current_user.server_name = server_name
                current_user.user_name = user_name
                current_user.save()
                return Report(True, None, 'set_rating [update]')
            except:
                User.create(server_id=server_id, server_name=server_name, user_id=user_id, user_name=user_name,
                            score=score)
                return Report(True, None, 'set_rating [new user]')

    def add_rating(self, server_id: int, user_id: int, score: int):
        with self.generate() as db:
            try:
                current_rating = User.get(User.server_id == server_id, User.user_id == user_id)
                current_rating.score = current_rating.score + score
                current_rating.save()
                return Report(True, None, 'add_rating [update]')
            except:
                return Report(False, None, 'add_rating [No User!]')

    def get_rating(self, server_id: int, user_id: str):
        def rating_callback_data(array):
            rating_data = {}
            for element in array:
                rating_data.update({element.user_id: (element.user_name, element.score)})
            return rating_data

        with self.generate() as db:
            if user_id == '*':
                try:
                    current_rating = User.select().where(User.server_id == server_id)
                    return Report(True, rating_callback_data(current_rating), 'get_rating [*]')
                except:
                    return Report(False, None, 'get_rating [*]')
            else:
                try:
                    user_id = int(user_id)
                    current_rating = User.get(User.server_id == server_id, User.user_id == user_id)
                    return Report(True, {current_rating.user_id: (current_rating.user_name, current_rating.score)},
                                  'get_rating [id]')
                except:
                    return Report(False, None, 'get_rating [id]')

    # управление ролями
    def set_role(self, server_id: int, server_name: str, role_id: int, role_name: str, lower_limit: int,
                 upper_limit: int):
        with self.generate() as db:
            try:
                current_role = Role.get(Role.server_id == server_id, Role.role_id == role_id)
                current_role.server_name = server_name
                current_role.role_name = role_name
                current_role.lower_limit = lower_limit
                current_role.upper_limit = upper_limit
                current_role.save()
                return Report(True, None, 'set_role [update]')
            except:
                Role.create(server_id=server_id, server_name=server_name, role_id=role_id, role_name=role_name,
                            lower_limit=lower_limit, upper_limit=upper_limit)
                return Report(True, None, 'set_role [new role]')

    def get_roles(self, server_id: int):
        def role_callback_data(array):
            rating_data = {}
            for element in array:
                rating_data.update({element.role_id: (element.role_name, (element.lower_limit, element.upper_limit))})
            return rating_data

        with self.generate() as db:
            try:
                current_roles = Role.select().where(Role.server_id == server_id)
                return Report(True, role_callback_data(current_roles), 'get_roles [id]')
            except:
                return Report(False, None, 'get_roles [id]')

    def clr_role(self, server_id: int, role_id: int):
        with self.generate() as db:
            try:
                current_role = Role.get(Role.server_id == server_id, Role.role_id == role_id)
                current_role.delete_instance()
                return Report(True, None, 'clr_role [id]')
            except:
                return Report(False, None, 'clr_role [id]')

    # работа с опросами
    def set_survey(self, server_id: int, server_name: str, message_id: int, message_text: str, results: str):
        with self.generate() as db:
            try:
                Survey.create(server_id=server_id, server_name=server_name, message_id=message_id,
                              message_text=message_text, results=results)
                return Report(True, None, 'set_survey [id]')
            except:
                return Report(False, None, 'set_survey [id]')

    def add_survey(self, server_id: int, message_id: int, results: str):
        with self.generate() as db:
            try:
                current_survey = Survey.get(Survey.server_id == server_id, Survey.message_id == message_id)
                current_survey.results = results
                current_survey.save()
                return Report(True, None, 'add_survey [id]')
            except:
                return Report(False, None, 'add_survey [id]')

    def chk_survey(self, server_id: int, message_id: int):
        with self.generate() as db:
            try:
                current_survey = Survey.get(Survey.server_id == server_id, Survey.message_id == message_id)
                return Report(True, current_survey.results, 'chk_survey [id]')
            except:
                return Report(False, None, 'chk_survey [id]')

    def get_survey(self, server_id: int):
        def survey_callback_data(arr):
            rating_data = {}
            for element in arr:
                rating_data.update({element.message_id: (element.message_text, element.results)})
            return rating_data

        with self.generate() as db:
            try:
                current_survey = Survey.select().where(Survey.server_id == server_id)
                return Report(True, survey_callback_data(current_survey), 'get_survey [id]')
            except:
                return Report(False, None, 'get_survey [id]')

    def clr_survey(self, server_id: int, message_id: int):
        with self.generate() as db:
            try:
                current_survey = Survey.get(Survey.server_id == server_id, Survey.message_id == message_id)
                current_survey.delete_instance()
                return Report(True, None, 'clr_survey [id]')
            except:
                return Report(False, None, 'clr_survey [id]')


class BaseModel(Model):
    class Meta:
        database = DataBase(database_name).generate()


class User(BaseModel):
    server_id = IntegerField()
    server_name = CharField()
    user_id = IntegerField()
    user_name = CharField()
    score = IntegerField()


class Role(BaseModel):
    server_id = IntegerField()
    server_name = CharField()
    role_id = IntegerField()
    role_name = CharField()
    lower_limit = IntegerField()
    upper_limit = IntegerField()


class Directory(BaseModel):
    server_id = IntegerField()
    server_name = CharField()
    console_id = IntegerField()
    log_id = IntegerField()
    info_id = IntegerField()


class Survey(BaseModel):
    server_id = IntegerField()
    server_name = CharField()
    message_id = IntegerField()
    message_text = CharField()
    results = CharField()


intents = discord.Intents.all()
intents.members = True
bot = commands.Bot(command_prefix='$', intents=intents)
db = DataBase(database_name)


if __name__ == "__main__":
    pass
    # DataBase(database_name).create(User, Role, Directory, Survey)
    # print(DataBase(database_name).set_rating(567365734, 'a', 543757645, 'boba', 500).note)
    # print(DataBase(database_name).add_rating(567365734, 543757345, 250).note)
    # print(DataBase(database_name).new_user(567365734, 'hueta', 543757345, 'Mr.Pipis', 0).note)
    # print(DataBase(database_name).get_rating(567365734, '543757345').data)
    print(DataBase(database_name).set_role(123, 'enclave', 456, 'king', 1, 2).data)
    print(DataBase(database_name).clr_role(123, 456).state)
    print(DataBase(database_name).get_roles(123).data)
    # print(DataBase(database_name).set_survey(123, 'test_zone', 456, 'text', '^_^').state)
    # print(DataBase(database_name).set_survey(123, 'test_zone', 654, 'text', '_^_').state)
    # print(DataBase(database_name).add_survey(123, 456, '))))))00000').state)
    # print(DataBase(database_name).chk_survey(123, 456).data)
    # print(DataBase(database_name).get_survey(123).data)
    # print(DataBase(database_name).clr_survey(123, 456).state)
