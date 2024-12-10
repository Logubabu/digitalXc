import csv
import random
from typing import List, Dict
from flask import Flask, request, send_file
from io import BytesIO, StringIO, TextIOWrapper
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/generate", methods=["POST"])
def generate():
    employee_file = request.files.get("employeeFile")
    previous_file = request.files.get("previousFile")

    if not employee_file or not previous_file:
        return "Missing files", 400

    try:
        employees = list(csv.DictReader(StringIO(employee_file.read().decode("utf-8"))))
        previous_assignments = list(csv.DictReader(StringIO(previous_file.read().decode("utf-8"))))
    except Exception as e:
        return f"Error reading files: {str(e)}", 400

    if not employees:
        return "Employee file is empty or invalid.", 400

    try:
        assignments = generate_secret_santa_assignments(employees, previous_assignments)
    except ValueError as e:
        return str(e), 400

    output = BytesIO()
    text_output = TextIOWrapper(output, encoding='utf-8', newline='')
    writer = csv.DictWriter(text_output, fieldnames=["Employee_Name", "Employee_EmailID", "Secret_Child_Name", "Secret_Child_EmailID"])
    writer.writeheader()
    writer.writerows(assignments)
    text_output.flush()
    output.seek(0)
    text_output.detach()

    return send_file(output, mimetype="text/csv", as_attachment=True, download_name="secret_santa_assignments.csv")
    # return assignments


def generate_secret_santa_assignments(employees: List[Dict[str, str]], previous_assignments: List[Dict[str, str]] = None) -> List[Dict[str, str]]:
    """Generate Secret Santa assignments."""
    names = [employee["Employee_Name"] for employee in employees]
    emails = {employee["Employee_Name"]: employee["Employee_EmailID"] for employee in employees}

    previous_map = {
        assignment["Employee_Name"]: assignment["Secret_Child_Name"]
        for assignment in previous_assignments or []
    }

    secret_children = names[:]
    random.shuffle(secret_children)

    for _ in range(100):
        valid = True
        for i, giver in enumerate(names):
            if giver == secret_children[i] or previous_map.get(giver) == secret_children[i]:
                valid = False
                random.shuffle(secret_children)
                break
        if valid:
            break
    else:
        raise ValueError("Unable to find a valid Secret Santa assignment.")

    assignments = []
    for i, giver in enumerate(names):
        assignments.append({
            "Employee_Name": giver,
            "Employee_EmailID": emails[giver],
            "Secret_Child_Name": secret_children[i],
            "Secret_Child_EmailID": emails[secret_children[i]],
        })
    return assignments


if __name__ == "__main__":
    app.run(debug=True)
