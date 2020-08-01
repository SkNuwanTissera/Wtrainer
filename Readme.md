# W- Trainer

## Schema

![Image](/wtrainer.png)

## Design

This ETL pipeline is used to extract data from JSON and seed relational database. 

This contains one fact table and 3 dimension tables. I have used primary keys and Surrogate keys here. Surrogate keys (SK) protect the system from sudden administrative changes. Another advantage of SK is, It enables us to add rows to dimensions that do not exist in the system now. SK’s can improve query processing. 

A fact table is a table that contains the measures of interest. Here the measure is Addictive type. We are mainly focussing on price and no of subscribers here in sales fact. 
Granularity is most important when it comes to facts. E.g: "Sales amounts, by product, by month.”

## Prerequisites
- install python
- install sqlite/sqlite3

## Setup
- git clone `https://github.com/SkNuwanTissera/Wtrainer.git`

## Run
- Run `python3 starschema.py`
- Check for file `star.db` 
- Open a terminal and type `sqlite3 star.db`
- Run the queries in the `queries.sql` one by one and check the results.

## Documentation

- Refer `Wtrainer.pdf`

## Improvements
- Row and page compression
    - Compression allows more rows to be stored on a page, but does not change the maximum row size of a table or index.
    Anyway, SQLalchemy library does not provide compression tools.
- Fact table partitioning
    - We can separate fact tables considering some fields to improve performance in large tables. 
- DB Indexing 
    - Using right and most wanted indexes in a data warehouse system can increase its speed and efficiency when it comes to a large dataset.
    E.g: 
    ````
   	CourseId_index001 = Index('CourseId_index001', Course.CourseId)
   	CourseId_index001.create(bind=engine)
- Invalidate JSON file
    - As a robust measure, we can validate the JSON whether the JSON contains the correct (amount and field) of keys. So if it's not so, We can give a proper error. So it makes more sense. 

## Analytical Queries
```
-- SQL QUERIES

-- 1. Course with highest number of subscribers which was published in 2015
select cd.CourseTitle, max(sf.NumOfSubscribers) as Subscribers
from sales_fact sf, course_dimension cd, date_dimension dd
where sf.CourseId = cd.CourseId and sf.DateId = dd.DateId and dd.Year='2015';

-- 2. The course with best sales so far
-- Sales amount is calculated by multiplying price of the course into number of subscribers. Only paid courses are taken into consideration here.
select cd.CourseTitle, max(sf.Price*sf.NumOfSubscribers) as Sales
from sales_fact sf, course_dimension cd
where sf.CourseId = cd.CourseId and  cd.IsPaid=1;

-- 3. Sales from levels of course such as All level, Beginner, Intermediate and Expert. Only paid courses are taken into consideration here.
select cd.Level, sum(sf.Price*sf.NumOfSubscribers) as Sales
from sales_fact sf, course_dimension cd
where sf.CourseId = cd.CourseId and  cd.IsPaid=1
group by cd.Level;

-- 4. The best 10 authors how has brought best sales descending sales amount. Only paid courses are taken into consideration here.
select ad.FirstName as Author , sum(sf.Price*sf.NumOfSubscribers) as Sales
from sales_fact sf, author_dimension ad, course_dimension cd
where sf.AuthorId = ad.Author and sf.CourseId = cd.CourseId and  cd.IsPaid=1
group by ad.Author
order by Sales desc limit 10;

-- 5. No of courses published in each year, descending No of courses. Paid courses and free courses are taken into consideration here.
select dd.Year, count(sf.CourseId) as NoofCourses
from sales_fact sf, course_dimension cd, date_dimension dd
where sf.CourseId = cd.CourseId and sf.DateId = dd.DateId
group by dd.Year
order by NoofCourses desc;
