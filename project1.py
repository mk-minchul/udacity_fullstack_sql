#!/usr/bin/env python3

import psycopg2


if __name__ == "__main__":


    # What are the most popular three articles of all time?
    # Present this information as a sorted list with the most popular article at the top.

    query = """
    SELECT title, count(*) as n_views FROM articles \n
    JOIN log ON articles.slug = substring(log.path, 10) \n
    GROUP BY title ORDER BY n_views DESC LIMIT 3;
    """


    try:
        db = psycopg2.connect(database="news")
    except psycopg2.Error as e:
        print ("Unable to connect!")
        print (e.pgerror)
        print (e.diag.message_detail)
        sys.exit(1)
    else:
        print ("Connected!")

    c = db.cursor()
    c.execute(query)
    results = c.fetchall()
    db.close()
    print("Q1")
    print(results)

    # Who are the most popular article authors of all time?
    query = """
    SELECT authors.name, count(*) as n_article FROM articles \n
    JOIN authors on articles.author = authors.id \n
    JOIN log on articles.slug = substring(log.path, 10)
    GROUP BY authors.name \n
    ORDER BY n_article DESC;
    """

    db = psycopg2.connect(database="news")
    c = db.cursor()
    c.execute(query)
    results = c.fetchall()
    db.close()
    print("Q2")
    print(results)

    # On which days did more than 1% of requests lead to errors?
    view_create = """
    CREATE VIEW error_count AS
    SELECT to_char(log.time, 'Mon DD, YYYY') as day, count(*) as sum FROM log \n
    where log.status NOT LIKE '200 OK' \n
    GROUP BY day;
    """
    try:
        # if the table doesnt exist
        db = psycopg2.connect(database="news")
        c = db.cursor()
        c.execute(view_create)
        db.commit()
        db.close()
    except:
        # print("error_count view exits")
        pass

    view_create = """
    CREATE VIEW all_count AS
    SELECT to_char(log.time, 'Mon DD, YYYY') as day, count(*) as sum FROM log \n
    GROUP BY day;
    """
    try:
        db = psycopg2.connect(database="news")
        c = db.cursor()
        c.execute(view_create)
        db.commit()
        db.close()
    except:
        # print("all_count view exitss")
        pass


    query = """
    SELECT CAST(error_count.sum as NUMERIC) / CAST(all_count.sum as NUMERIC) * 100 as result from all_count \n
    JOIN error_count on error_count.day = all_count.day \n
    ORDER BY result desc limit 1;
    """
    db = psycopg2.connect(database="news")
    c = db.cursor()
    c.execute(query)
    results = c.fetchall()
    db.close()
    print("Q3")
    print(results)


