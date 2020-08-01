# W- Trainer

## Design

This contains one fact table and 3 dimension tables. I have used primary keys and Surrogate keys here. Surrogate keys (SK) protect the system from sudden administrative changes. Another advantage of SK is, It enables us to add rows to dimensions that do not exist in the system now. SK’s can improve query processing. 

A fact table is a table that contains the measures of interest. Here the measure is Addictive type. We are mainly focussing on price and no of subscribers here in sales fact. 
Granularity is most important when it comes to facts. E.g: "Sales amounts, by product, by month.”

## Schema

![Image](/wtrainer.png)

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
