#######################################################################
# READ THIS BEFORE EXECUTION
#######################################################################
# This script will delete the current db file and create a new db file
# with all new data in JSON. This has an limitation when it comes to
# adding more data that needs to be append to the database.
########################################################################

import json
import os
from datetime import datetime
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import *

# Removing current DB file
os.remove("star.db")
print("\nCurrent DB File Removed!")

engine = create_engine('sqlite:///star.db')
Base = declarative_base()

# read file
print('\nReading JSON ...')
with open('course_data.json', 'r') as myfile:
    data = myfile.read()

# parse file
obj = json.loads(data)


# Defining the schemas

# Course Dimension
class Course(Base):
    __tablename__ = "course_dimension"
    Id = Column(Integer, primary_key=True)
    CourseId = Column(String)
    CourseTitle = Column(String)
    IsPaid = Column(Boolean)
    Price = Column(Float)
    NumOfSubscribers = Column(Integer)
    NumOfReviews = Column(Integer)
    NumOfLectures = Column(Integer)
    Level = Column(String)
    ContentDuration = Column(Float)
    PublishedTimestamp = Column(DateTime)
    Subject = Column(String)

# Author Dimension
class Author(Base):
    __tablename__ = "author_dimension"
    AuthorId = Column(Integer, primary_key=True)
    Author = Column(String)
    FirstName = Column(String)
    LastName = Column(String)
    AuthorCode = Column(String)


# Date Dimension
class Date(Base):
    __tablename__ = "date_dimension"
    DateId = Column(Integer, primary_key=True)
    Month = Column(Integer)
    Year = Column(Integer)
    Timestamp = Column(TIMESTAMP)


# Fact Table
# Sales Fact Table
class Sales(Base):
    __tablename__ = "sales_fact"
    SalesId = Column(Integer, primary_key=true)
    CourseId = Column(Integer)
    AuthorId = Column(Integer)
    DateId = Column(Integer)
    NumOfSubscribers = Column(Integer)
    Price = Column(Float)


# Drop current tables

# Course.__table__.drop(engine)
# Author.__table__.drop(engine)
# Date.__table__.drop(engine)
# Sales.__table__.drop(engine)

# Create new tables
print('Creating new tables ...')

Course.__table__.create(bind=engine, checkfirst=true)
Author.__table__.create(bind=engine, checkfirst=true)
Date.__table__.create(bind=engine, checkfirst=true)
Sales.__table__.create(bind=engine, checkfirst=true)

# Data transformation
print('Data Transformation on Process ...')

sales_fact, date_dimension, author_dimension, course_dimension = [], [], [], []

for i, result in enumerate(obj['course_id']):
    course_row = {}
    author_row = {}
    date_row = {}
    sales_row = {}

    course_row['Id'] = i + 1
    course_row['CourseId'] = str(obj['course_id'][str(i)])
    course_row['CourseTitle'] = str(obj['course_title'][str(i)])
    course_row['IsPaid'] = bool(obj['is_paid'][str(i)])
    course_row['Price'] = float(obj['price'][str(i)])
    course_row['NumOfSubscribers'] = int(obj['num_subscribers'][str(i)])
    course_row['NumOfReviews'] = int(obj['num_reviews'][str(i)])
    course_row['NumOfLectures'] = int(obj['num_lectures'][str(i)])
    course_row['Level'] = str(obj['level'][str(i)])
    course_row['ContentDuration'] = float(obj['content_duration'][str(i)])
    date = datetime.strptime(obj['published_timestamp'][str(i)], '%Y-%m-%dT%H:%M:%SZ')
    course_row['PublishedTimestamp'] = date.date()
    course_row['Subject'] = str(obj['subject'][str(i)])

    sales_row['SalesId'] = i + 1
    sales_row['CourseId'] = str(obj['course_id'][str(i)])
    sales_row['AuthorId'] = str(obj['author'][str(i)])
    sales_row['DateId'] = i + 1
    sales_row['NumOfSubscribers'] = int(obj['num_subscribers'][str(i)])
    sales_row['Price'] = float(obj['price'][str(i)])

    date_row['DateId'] = i + 1
    month = str(date).split(' ')[0].split('-')[1]
    year = str(date).split(' ')[0].split('-')[0]
    date_row['Month'] = str(month)
    date_row['Year'] = str(year)
    date_row['Timestamp'] = date.date()

    author_row['AuthorId'] = i + 1
    author_row['Author'] = str(obj['author'][str(i)])
    author_row['FirstName'] = str(obj['author'][str(i)]).split('_')[0]
    author_row['LastName'] = str(obj['author'][str(i)]).split('_')[1]  # split
    author_row['AuthorCode'] = str(obj['author'][str(i)]).split('_')[2]  # split

    course_dimension.append(course_row)
    sales_fact.append(sales_row)
    date_dimension.append(date_row)
    author_dimension.append(author_row)

# Load to database - seeding
print('Loading data to database ...')

Session = sessionmaker(bind=engine)
session = Session()

for course in course_dimension:
    row = Course(**course)
    session.add(row)

for dateData in date_dimension:
    row = Date(**dateData)
    session.add(row)

for authorData in author_dimension:
    row = Author(**authorData)
    session.add(row)

for salesData in sales_fact:
    row = Sales(**salesData)
    session.add(row)

session.commit()

print("\nSuccessfully Completed The Process !!")
