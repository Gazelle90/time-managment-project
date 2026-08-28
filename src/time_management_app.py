from flask import Flask, request , jsonify
from datetime import date 
from psycopg2.errors import ForeignKeyViolation

from src.data.queries import (
    list_customers, find_consultant_by_id ,list_consultants, find_customer_by_id,
      add_time_entry, find_time_entries,delete_time_entries,reporting_balance)

app = Flask(__name__)

@app.route("/", methods=["GET"])
def hello():
    return jsonify({"message": "Skillio person API up and running"})


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})


#consultants

@app.route("/consultants", methods=["GET"])
def http_list_consultants():
    rows = list_consultants()
    return jsonify([
        {"id": r[0], "name": r[1], "email": r[2]}
        for r in rows
    ])


@app.route("/consultants/<int:person_id>", methods=["GET"])
def http_get_consultants(person_id :int):
    row = find_consultant_by_id(person_id)
    if row is None:
        return jsonify({"error": "person not found"}), 404
    return jsonify({"id": row[0], "name": row[1], "email": row[2]})

# companies deact

@app.route("/companies", methods=["GET"])
def http_list_customers():
    rows = list_customers()
    return jsonify([
        {"id": r[0], "name": r[1]}
        for r in rows
    ])

@app.route("/companies/<int:id>", methods=["GET"])
def http_get_customer(id :int):
    row = find_customer_by_id(id)
    if row is None:
        return jsonify({"error": "person not found"}), 404
    return jsonify({"id": row[0], "name": row[1]})


# time entry 

@app.route("/time/<int:person_id>/<int:company_id>", methods=["GET"])
def http_find_time_entries(person_id: int,company_id: int):
    rows = find_time_entries(person_id, company_id)
    if not rows:
        return jsonify({"error": "time entry not found"}), 404
    return jsonify([
    {
        "id": row[0],
        "person_id": row[1],
        "company_id": row[2],
        "date": row[3].isoformat(),
        "start_time": row[4].isoformat(),
        "end_time": row[5].isoformat(),
        "hours": row[6].isoformat() if row[6] is not None else None,
        "lunch_break": row[7]
        }
    for row in rows
])


@app.route("/time/delete/<int:person_id>/<int:company_id>/<work_date>", methods=["DELETE"])
def http_delete_time_entries(person_id: int , company_id: int, work_date: date ):
    rows = delete_time_entries(person_id, company_id, work_date)
    if rows == 0:
        return jsonify({"error": "person not found"}), 404
    return ("", 204)

@app.route("/time/add/", methods=["POST"])
def http_add_time_entry():
    data = request.get_json(silent=True)
    print(data)
    try:
        if not data or "person_id" not in data or "company_id" not in data or "date" not in data or "start_time" not in data or "end_time" not in data:
         return jsonify({"error": "person id , company id, date , start time and end time  are required"}), 400

        new_id = add_time_entry(data["person_id"], data["company_id"],data["date"],
                             data["start_time"] , data["end_time"], data.get("lunch_break", 0))
        return jsonify({"id": new_id, **data}), 201
    except ForeignKeyViolation:
        return jsonify({
            "error": "Person or company does not exist"
        }), 404

 

####reporting_balance app #####



if __name__ == "__main__":
    app.run(debug=True, port=3000)