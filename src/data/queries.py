import psycopg2
from data.queries import load_db_config
from datetime import date, time

#functions related to customers or comanies 
def list_customers() -> list[tuple]:
    con = None
    try:
        con = psycopg2.connect(**load_db_config())
        cursor = con.cursor()
        cursor.execute( "SELECT * FROM company")
        rows = cursor.fetchall()

    except (Exception, psycopg2.DatabaseError) as error:
        if con is not None:
            con.rollback()
        raise
    finally:
        if con is not None:
            con.close()
    return rows
    
def find_customer_by_id(company_id: int) -> tuple | None:

    con = None
    try:
        con = psycopg2.connect(**load_db_config())
        cursor = con.cursor()
        cursor.execute("SELECT * FROM company WHERE id = %s" , (company_id,))
        rows = cursor.fetchone()
    except (Exception, psycopg2.DatabaseError) as error:
        if con is not None:
            con.rollback()
        raise
    finally:
        if con is not None:
            con.close()
    return rows

#functions for consultants 

def list_consultants() -> list[tuple]:
    con = None
    try:
        con = psycopg2.connect(**load_db_config())
        cursor = con.cursor()
        cursor.execute( "SELECT * FROM person")
        rows = cursor.fetchall()

    except (Exception, psycopg2.DatabaseError) as error:
        if con is not None:
            con.rollback()
        raise
    finally:
        if con is not None:
            con.close()
    return rows


def find_consultant_by_id(person_id: int) -> tuple | None:
    con = None
    try:
        con = psycopg2.connect(**load_db_config())
        cursor = con.cursor()
        cursor.execute("SELECT * FROM person WHERE id = %s" , (person_id,))
        rows = cursor.fetchone()
    except (Exception, psycopg2.DatabaseError) as error:
        if con is not None:
            con.rollback()
        raise
    finally:
        if con is not None:
            con.close()
    return rows


# timeentries 

def add_time_entry(person_id: int, company_id: int ,date : date ,start_time: time,
                   end_time: time, lunch_break: int) -> tuple:
    con = None
    try:
        con = psycopg2.connect(**load_db_config())
        cursor = con.cursor()
        cursor.execute("INSERT INTO times_daily"
        " ( person_id, company_id,date, start_time, end_time, lunch_break) " \
        "VALUES (%s,%s,%s,%s,%s,%s)",
        (person_id, company_id,date, start_time, end_time, lunch_break))

        row = cursor.fetchone()
    except (Exception, psycopg2.DatabaseError) as error:
        if con is not None:
            con.rollback()
        raise
    finally:
        if con is not None:
            con.close()
    return row

def find_time_entries() -> tuple:
    pass 

def delete_time_entries(person_id: int,company_id: int, work_date: date, start_time: time
) -> int:
    con = None
    try:
        con = psycopg2.connect(**load_db_config())
        cursor = con.cursor()
        cursor.execute(
            """
            DELETE FROM times_daily
            WHERE person_id = %s
              AND company_id = %s
              AND date = %s
              AND start_time = %s
            """,
            (person_id, company_id, work_date, start_time)
        )
        rows = cursor.rowcount
        con.commit()
        return rows
    except psycopg2.DatabaseError:
        if con is not None:
            con.rollback()
        raise
    finally:
        if con is not None:
            con.close()


def reporting_balance(person_id: int, company_id: int ,date : date) -> tuple:
    con = None
    try:
        con = psycopg2.connect(**load_db_config())
        cursor = con.cursor()
        #TODO : fill in the query
        cursor.execute("")
        rows = cursor.fetchall()
    except (Exception, psycopg2.DatabaseError) as error:
        if con is not None:
            con.rollback()
        raise
    finally:
        if con is not None:
            con.close()
    return rows