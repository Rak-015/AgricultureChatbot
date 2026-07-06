import mysql.connector
from flask import current_app
from mysql.connector import Error


def get_connection(database=True):
    cfg = current_app.config
    params = {"host": cfg["MYSQL_HOST"], "user": cfg["MYSQL_USER"], "password": cfg["MYSQL_PASSWORD"], "port": cfg["MYSQL_PORT"], "autocommit": False}
    if database:
        params["database"] = cfg["MYSQL_DATABASE"]
    return mysql.connector.connect(**params)


def init_database():
    db_name = current_app.config["MYSQL_DATABASE"]
    schema_path = current_app.root_path + "/../database/schema.sql"
    with open(schema_path, "r", encoding="utf-8") as file:
        statements = [part.strip() for part in file.read().split(";") if part.strip()]
    try:
        conn = get_connection(database=False)
        cursor = conn.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{db_name}`")
        cursor.execute(f"USE `{db_name}`")
        for statement in statements:
            upper = statement.upper()
            if upper.startswith("CREATE DATABASE") or upper.startswith("USE "):
                continue
            cursor.execute(statement)
        conn.commit()
        cursor.close()
        conn.close()
        return True, "Database is ready."
    except Error as exc:
        return False, str(exc)


def execute(query, params=None, fetchone=False, fetchall=False):
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, params or ())
        result = None
        if fetchone:
            result = cursor.fetchone()
        elif fetchall:
            result = cursor.fetchall()
        conn.commit()
        cursor.close()
        conn.close()
        return result
    except Error as e:
        print("MYSQL Error:", e)
        return None


def count_rows(table):
    row = execute(f"SELECT COUNT(*) AS total FROM {table}", fetchone=True)
    return row["total"] if row else 0
