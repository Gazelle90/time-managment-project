from datetime import date, time

import psycopg2

from src.data.database import get_connection


def list_customers() -> list[tuple]:
    con = None
    try:
        con = get_connection()
        cursor = con.cursor()
        cursor.execute("SELECT * FROM company")
        rows = cursor.fetchall()

    except Exception as error:
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
        cursor.execute("SELECT * FROM company WHERE id = %s", (company_id,))
        rows = cursor.fetchone()
    except Exception as error:
        if con is not None:
            con.rollback()
        raise
    finally:
        if con is not None:
            con.close()
    return rows


def list_consultants() -> list[tuple]:
    con = None
    try:
        con = get_connection()
        cursor = con.cursor()
        cursor.execute("SELECT * FROM person")
        rows = cursor.fetchall()

    except Exception as error:
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
        cursor.execute("SELECT * FROM person WHERE id = %s", (person_id,))
        rows = cursor.fetchone()
    except Exception as error:
        if con is not None:
            con.rollback()
        raise
    finally:
        if con is not None:
            con.close()
    return rows


# timeentries


def add_time_entry(
    person_id: int,
    company_id: int,
    date: date,
    start_time: time,
    end_time: time,
    lunch_break: time,
) -> tuple:
    con = None
    try:
        con = get_connection()
        cursor = con.cursor()
        cursor.execute(
            "INSERT INTO times_daily"
            " ( person_id, company_id, date, start_time, end_time, lunch_break) "
            "VALUES (%s,%s,%s,%s,%s,%s)"
            "RETURNING id",
            (person_id, company_id, date, start_time, end_time, lunch_break),
        )
        row = cursor.fetchone()
        con.commit()
        return row[0]
    except Exception as error:
        if con is not None:
            con.rollback()
        raise
    finally:
        if con is not None:
            con.close()


def find_time_entries(person_id: int, company_id: int) -> tuple:
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
            (person_id, company_id),
        )

        rows = cursor.fetchall()
        return rows
    except Exception as error:
        if con is not None:
            con.rollback()
        raise
    finally:
        if con is not None:
            con.close()


def delete_time_entries(person_id: int, company_id: int, work_date: date) -> int:
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
            (person_id, company_id, work_date),
        )
        rows = cursor.rowcount
        con.commit()
        return rows
    except Exception as error:
        if con is not None:
            con.rollback()
        raise
    finally:
        if con is not None:
            con.close()


def weekly_report_companies() -> tuple:
    con = None
    try:
        con = get_connection()
        cursor = con.cursor()
        cursor.execute(
            """
			SELECT
				company_name,
				total_hours
			FROM view_weekly
			WHERE week_start = DATE_TRUNC('week', CURRENT_DATE)::date
			ORDER BY total_hours DESC;
            """,
        )
        rows = cursor.fetchall()
    except Exception as error:
        if con is not None:
            con.rollback()
        raise
    finally:
        if con is not None:
            con.close()
    return rows


def weekly_report_consultants() -> tuple:
    con = None
    try:
        con = get_connection()
        cursor = con.cursor()
        cursor.execute(
            """
				SELECT
					p.name AS consultant_name,
					SUM(
						ROUND(EXTRACT(EPOCH FROM (t.end_time - t.start_time - t.lunch_break)) / 3600.0, 2)
					) AS total_hours,
					STRING_AGG(
						c.name || ' ' || TRIM(TO_CHAR(company_totals.company_hours, '990.0')),
						', ' ORDER BY c.name
					) AS company_breakdown
				FROM person p
				JOIN times_daily t ON t.person_id = p.id
				JOIN company c ON t.company_id = c.id
				JOIN (
					SELECT
						person_id,
						company_id,
						SUM(
							ROUND(EXTRACT(EPOCH FROM (end_time - start_time - lunch_break)) / 3600.0, 2)
						) AS company_hours
					FROM times_daily
					GROUP BY person_id, company_id
				) company_totals ON company_totals.person_id = t.person_id AND company_totals.company_id = t.company_id
				GROUP BY p.id, p.name
				ORDER BY p.name;
			""",
        )
        rows = cursor.fetchall()
    except (Exception, psycopg2.DatabaseError) as error:
        if con is not None:
            con.rollback()
        raise
    finally:
        if con is not None:
            con.close()
    return rows


def total_hours() -> tuple:
    con = None
    try:
        con = get_connection()
        cursor = con.cursor()
        cursor.execute(
            """
                SELECT SUM(total_hours)
                FROM view_weekly
                WHERE week_start = DATE_TRUNC('week', CURRENT_DATE)::date;
            """,
        )
        total = cursor.fetchone()[0]
    except (Exception, psycopg2.DatabaseError) as error:
        if con is not None:
            con.rollback()
        raise
    finally:
        if con is not None:
            con.close()
    return total
