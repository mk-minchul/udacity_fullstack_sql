#!/usr/bin/env python3

import psycopg2
import sys


def connect(database_name="news"):
    try:
        db = psycopg2.connect("dbname={}".format(database_name))
        cursor = db.cursor()
        return db, cursor
    except psycopg2.Error, e:
        print("Unable to connect!")
        print(e.pgerror)
        print(e.diag.message_detail)
        sys.exit(1)


def execute_query(db, cursor, query):
    cursor.execute(query)
    results = c.fetchall()
    db.close()
    return results


def formatted_print(results, type="views"):
    for result in results:
        first, second = result
        if type == "views":
            print("    {} - {} views".format(first, second))
        elif type == "error":
            print("    {} - {} % error".format(first, second))
        else:
            raise ValueError
    print("-" * 70)


if __name__ == "__main__":
    # What are the most popular three articles of all time?
    # Present this information as a sorted list with the most popular article at the top.

    query = """
    SELECT title, count(*) as n_views FROM articles \n
    JOIN log ON articles.slug = substring(log.path, 10) \n
    GROUP BY title ORDER BY n_views DESC LIMIT 3;
    """

    db, c = connect()
    results = execute_query(db, c, query)

    print("Q1: What are the most popular three articles of all time?")
    formatted_print(results)

    # Who are the most popular article authors of all time?
    query = """
    SELECT authors.name, count(*) as n_article FROM articles \n
    JOIN authors on articles.author = authors.id \n
    JOIN log on articles.slug = substring(log.path, 10)
    GROUP BY authors.name \n
    ORDER BY n_article DESC;
    """

    db, c = connect()
    results = execute_query(db, c, query)

    print("Q2: Who are the most popular article authors of all time?")
    formatted_print(results)

    # On which days did more than 1% of requests lead to errors?
    query = """
    SELECT all_count.day, CAST(error_count.sum as NUMERIC) / CAST(all_count.sum as NUMERIC) * 100 as result from all_count \n
    JOIN error_count on error_count.day = all_count.day \n
    ORDER BY result desc limit 1;
    """

    db, c = connect()
    results = execute_query(db, c, query)

    print("Q3: On which days did more than 1% of requests lead to errors?")
    formatted_print(results, type="error")
