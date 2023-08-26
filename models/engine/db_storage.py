#!/usr/bin/python3
"""This module defines a class to manage db storage for hbnb clone"""
import os
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import BaseModel, Base
# the entity import is necessary so that
# sqlalchemy can find them on create_all
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review



class DBStorage:
    """This class manages storage of hbnb models in database"""
    __engine = None
    __session = None

    def __init__(self):
        """Initializes database storage manager"""
        self.__engine = create_engine(self.__connectionstring, pool_pre_ping=True)
        self.__drop_db_for_test()
        self.__session = self.__create_session()

    @property
    def __connectionstring(self):
        """Builds a database connectionstring"""
        mysql_user = os.environ.get('HBNB_MYSQL_USER')
        mysql_pwd = os.environ.get('HBNB_MYSQL_PWD')
        mysql_host = os.environ.get('HBNB_MYSQL_HOST')
        mysql_db = os.environ.get('HBNB_MYSQL_DB')
        return f'mysql+mysqldb://{mysql_user}:{mysql_pwd}@{mysql_host}/{mysql_db}'
    
    def __drop_db_for_test(self):
        """Drops database if environment is test"""
        if os.environ.get('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

    def __build_dic_key(self, obj):
        """Builds a dictionary key for returning objects"""
        return obj.to_dict()['__class__'] + '.' + obj.id
    
    def __create_session(self):
        """Creates a session with specific options"""
        session_factory = sessionmaker(
            bind=self.__engine,
            expire_on_commit=False
        )
        return scoped_session(session_factory)

    def all(self, cls=None):
        """Returns a dictionary of models currently in storage"""
        result = {}
        if cls:
            cls_res = self.__session.query(cls).all()
            result.update({self.__build_dic_key(obj): obj for obj in cls_res})
        else:
            types = [State, City, User, Place]
            for tp in types:
                tp_res = self.__session.query(tp).all() 
                result.update({self.__build_dic_key(obj): obj for obj in tp_res})
        return result 

    def new(self, obj):
        """Adds new object to storage"""
        self.__session.add(obj)

    def delete(self, obj=None):
        """Deletes an object from storage"""
        if obj:
            self.__session.delete(obj)

    def save(self):
        """Saves storage dictionary to file"""
        self.__session.commit()

    def reload(self):
        """Load all types"""
        Base.metadata.create_all(self.__engine)
