from flask import Flask, request , jsonify 

from src.data.queries import (
    list_customers, find_consultant_by_id ,list_consultants, find_customer_by_id,
      add_time_entry, find_time_entries,delete_time_entries,reporting_balance)

app = Flask(__name__)

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
    row = find_time_entries(person_id, company_id)
    if row is None:
        return jsonify({"error": "time entry not found"}), 404
    return jsonify({
    "id": row[0],
    "person_id": row[1],
    "company_id": row[2],
    "date": row[3],
    "start_time": row[4],
    "end_time": row[5],
    "lunch_break": row[6],
    "hours": row[7]
})


@app.route("/time/<int:id>", methods=["DELETE"])
def http_delete_time_entries(id: int):
    rows = delete_time_entries(id)
    if rows == 0:
        return jsonify({"error": "person not found"}), 404
    return ("", 204)

@app.route("/time/", methods=["POST"])
def http_add_time_entry():
    data = request.get_json(silent=True)

    if not data or "person_id" not in data or "company_id" not in data or "start_time" not in data or "end_time" not in data :
        return jsonify({"error": "person, company id, start time and end time  are required"}), 400

    new_id = add_time_entry(data["person_id"], data["company_id"],
                             data["start_time"] , data["end_time"], data.get("lunch_break", 0))
    return jsonify({"id": new_id, **data}), 201

####reporting_balance app #####



if __name__ == "__main__":
    app.run(debug=True, port=3000)