import logging
import psycopg2

from flask import Flask

from utils.data import get_random_record

logging.basicConfig(filename='history.log', level=logging.DEBUG)
app = Flask(__name__)

master_connection, slave_connection = \
    (psycopg2.connect(
        host='postgresql-master',
        port=5432,
        database="my_database",
        user="repl_user",
        password="repl_password"
    ),
     psycopg2.connect(
         host='postgresql-slave',
         port=5432,
         database="my_database",
         user="repl_user",
         password="repl_password"
     ))


@app.route("/read/master")
def read_master():
    is_success = True
    try:
        cursor = master_connection.cursor()
        cursor.execute("""
            SELECT SUM(Survived)
            FROM public.Titanic
        """)
        [total_amount] = cursor.fetchone()
        app.logger.info(f"[Master]: total survived on Titanic: {total_amount}")
    except Exception as e:
        is_success = False
        app.logger.error(f"Error: {e}")
    return f"[Master]: read success = {is_success}"


@app.route("/read/slave")
def read_slave():
    is_success = True
    try:
        cursor = slave_connection.cursor()
        cursor.execute("""
            SELECT SUM(Survived)
            FROM public.Titanic
        """)
        [total_amount] = cursor.fetchone()
        app.logger.info(f"[Slave]: total survived on Titanic: {total_amount}")
    except Exception as e:
        is_success = False
        app.logger.error(f"Error: {e}")
    return f"[Slave]: read success = {is_success}"


@app.route("/write/master")
def write_master():
    is_success = True
    message = "ok"
    try:
        record = get_random_record()
        cursor = master_connection.cursor()
        cursor.execute(
            f"INSERT INTO Titanic (PassengerId,Survived,Pclass,Name,Sex,Age,Ticket) VALUES (%s,%s,%s,%s,%s,%s,%s);",
            list(record.values())
        )
        master_connection.commit()
    except Exception as e:
        app.logger.error(f"Error: {e}")
        master_connection.rollback()
        is_success = False
        message = "cannot execute INSERT in a read-only transaction"
    return f"[Master]: write success = {is_success}, message = {message}"

@app.route("/write/slave")
def write_slave():
    is_success = True
    message = "ok"
    try:
        record = get_random_record()
        cursor = slave_connection.cursor()
        cursor.execute(
            f"INSERT INTO Titanic (PassengerId,Survived,Pclass,Name,Sex,Age,Ticket) VALUES (%s,%s,%s,%s,%s,%s,%s);",
            list(record.values())
        )
        slave_connection.commit()
    except Exception as e:
        app.logger.error(f"Error: {e}")
        slave_connection.rollback()
        is_success = False
        message = "cannot execute INSERT in a read-only transaction"
    return f"[Slave]: write success = {is_success}, message = {message}"


@app.route("/database/init")
def database_init():
    cursor = master_connection.cursor()
    try:
        cursor.execute("CREATE TABLE Titanic (id serial PRIMARY KEY, PassengerId integer, Survived integer, Pclass integer, Name varchar, Sex varchar, Age integer, Ticket varchar);")
        return "Table Titanic was created successfully!"
    except:
        return "I can't create table Titanic!"


@app.route("/")
def index():
    return "Server is running on localhost:8080!"


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)
