# Log Analysis Project
The code takes the Los Angeles new databse and creates SQL queries that answer specific questions. 

# Requirements 
- python 3

# Setup

1. Download the newdata.zip and unzip the data to create newsdata.sql

```
$ wget https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip
```


2. Create vagrant machine and start

```
$ vagrant ssh
$ vagrant up
```

# RUN

This python script will read newsdata.sql and print a statement in result.txt file that answers the three questions.
1. What are the most popular three articles of all time?
2. Who are the most popular article authors of all time?
3. On which days did more than 1% of requests lead to errors?

Run with the following code. The question 3 needs views with error_count and all_count. 
They will be created if the code has never been run before. The code will skip if the view already exists.

```
cd into/the/current_dir
$ python project1.py
```


