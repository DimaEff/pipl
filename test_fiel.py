from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from sqlalchemy import Table, Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
basedir = os.path.abspath(os.path.dirname(__file__))


app = Flask(__name__)
db = SQLAlchemy(app)

app.config.update(
    SQLALCHEMY_DATABASE_URI=os.path.join(basedir, 'app.db'),
    SQLALCHEMY_TRACK_MODIFICATIONS=False
)


class Association(Base):
    # __tablename__ = 'association'
    left_id = Column(Integer, ForeignKey('parent.id'), primary_key=True)
    right_id = Column(Integer, ForeignKey('child.id'), primary_key=True)
    extra_data = Column(String(50))
    child = relationship("Child", back_populates="parents")
    parent = relationship("Parent", back_populates="children")


class Parent(Base):
    # __tablename__ = 'left'
    id = Column(Integer, primary_key=True)
    children = relationship("Association", back_populates="parent")

    def __repr__(self):
        return 'Parent {}'.format(self.id)


class Child(Base):
    # __tablename__ = 'right'
    id = Column(Integer, primary_key=True)
    parents = relationship("Association", back_populates="child")

    def __repr__(self):
        return 'Child {}'.format(self.id)