import json
from datetime import datetime, timedelta
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import *

engine = create_engine('sqlite:///demo30.db')
Base = declarative_base()

# read file
with open('course_data.json', 'r') as myfile:
    data = myfile.read()

# parse file
obj = json.loads(data)


# Defining the schemas

class Course(Base):
    __tablename__ = "course_fact"
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
    AuthorId = Column(String)

Course.__table__.create(bind=engine, checkfirst=true)

# Data transformation

course_fact = []

for i, result in enumerate(obj['course_id']):
    # print(str(result['course_id']['0']))
    row = {}

    row['Id'] = i + 1
    row['CourseId'] = str(obj['course_id'][str(i)])
    row['CourseTitle'] = str(obj['course_title'][str(i)])
    row['IsPaid'] = bool(obj['is_paid'][str(i)])
    row['Price'] = float(obj['price'][str(i)])
    row['NumOfSubscribers'] = int(obj['num_subscribers'][str(i)])
    row['NumOfReviews'] = int(obj['num_reviews'][str(i)])
    row['NumOfLectures'] = int(obj['num_lectures'][str(i)])
    row['Level'] = str(obj['level'][str(i)])
    row['ContentDuration'] = float(obj['content_duration'][str(i)])
    date = datetime.strptime(obj['published_timestamp'][str(i)][:19], '%Y-%m-%dT%H:%M:%S')
    row['PublishedTimestamp'] = date.date()
    row['Subject'] = str(obj['subject'][str(i)])
    row['AuthorId'] = str(obj['author'][str(i)])

    course_fact.append(row)

# Load

Session = sessionmaker(bind=engine)
session = Session()

for course in course_fact:
    row = Course(**course)
    session.add(row)

session.commit()
