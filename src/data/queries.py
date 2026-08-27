
from datetime import date, time
from src.data.database import get_connection

#functions related to customers or comanies 
def list_customers() -> list[tuple]:
    con = None
    try:
        con = get_connection()
        cursor = con.cursor()
        cursor.execute( "SELECT * FROM company")
        rows = cursor.fetchall()

    except (Exception) as error:
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
        con = get_connection()
        cursor = con.cursor()
        cursor.execute("SELECT * FROM company WHERE id = %s" , (company_id,))
        rows = cursor.fetchone()
    except (Exception) as error:
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
        con = get_connection()
        cursor = con.cursor()
        cursor.execute( "SELECT * FROM person")
        rows = cursor.fetchall()

    except (Exception) as error:
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
        con = get_connection()
        cursor = con.cursor()
        cursor.execute("SELECT * FROM person WHERE id = %s" , (person_id,))
        rows = cursor.fetchone()
    except (Exception) as error:
        if con is not None:
            con.rollback()
        raise
    finally:
        if con is not None:
            con.close()
    return rows


# timeentries 

def add_time_entry(person_id: int, company_id: int ,date : date ,start_time: time,
                   end_time: time, lunch_break: time) -> tuple:
    con = None
    try:
        con = get_connection()
        cursor = con.cursor()
        cursor.execute("INSERT INTO times_daily"
        " ( person_id, company_id, date, start_time, end_time, lunch_break) " \
        "VALUES (%s,%s,%s,%s,%s,%s)"\
            "RETURNING id",
        (person_id, company_id,date, start_time, end_time, lunch_break))
        row = cursor.fetchone()
        con.commit()
        return row[0]
    except (Exception) as error:
        if con is not None:
            con.rollback()
        raise
    finally:
        if con is not None:
            con.close()
    

def find_time_entries(person_id: int,company_id: int) -> tuple:
    con = None
    try:
        con = get_connection()
        cursor = con.cursor()
        cursor.execute(
        """
        SELECT
            id,
            person_id,
            company_id,
            date,
            start_time,
            end_time,
            lunch_break,
            hours
        FROM times_daily
        WHERE person_id = %s AND company_id = %s
        """,
    (person_id, company_id)
)

        rows = cursor.fetchall()
        return rows
    except (Exception) as error:
        if con is not None:
            con.rollback()
        raise
    finally:
        if con is not None:
            con.close()


     

def delete_time_entries(person_id: int,company_id: int, work_date: date) -> int:
    con = None
    try:
        con = get_connection()
        cursor = con.cursor()
        cursor.execute(
            """
            DELETE FROM times_daily
            WHERE person_id = %s
              AND company_id = %s
              AND date = %s

            """,
            (person_id, company_id, work_date)
        )
        rows = cursor.rowcount
        con.commit()
        return rows
    except (Exception) as error:
        if con is not None:
            con.rollback()
        raise
    finally:
        if con is not None:
            con.close()


def reporting_balance(person_id: int, company_id: int ,date : date) -> tuple:
    con = None
    try:
        con = get_connection()
        cursor = con.cursor()
        #TODO : fill in the query
        cursor.execute("")
        rows = cursor.fetchall()
    except (Exception) as error:
        if con is not None:
            con.rollback()
        raise
    finally:
        if con is not None:
            con.close()
    return rows