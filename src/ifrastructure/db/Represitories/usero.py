from src.domain.menu.dto.all_schemas import BaseUser
from src.ifrastructure.db.Represitories.Base_repo import MongoRepo

from src.ifrastructure.db import database


class OrderRepo(MongoRepo):
    def __init__(self,db = database ):
        super().__init__(db.users, BaseUser)