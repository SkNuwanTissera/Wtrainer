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