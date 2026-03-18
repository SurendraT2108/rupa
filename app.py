from flask import Flask, render_template, request
import pandas as pd
import os

app = Flask(__name__)

CSV_FILE = 'students.csv'

def load_data():
    if os.path.exists(CSV_FILE):
        return pd.read_csv(CSV_FILE)
    else:
        return pd.DataFrame(columns=["Name", "Department", "StudentID", "Course", "Grade", "Status"])

@app.route('/', methods=['GET', 'POST'])
def dashboard():
    students_data = load_data()
    filtered_data = None

    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        department = request.form.get('department', '').strip()

        filtered_data = students_data

        if name:
            filtered_data = filtered_data[
                filtered_data['Name'].str.contains(name, case=False, na=False)
            ]

        if department:
            filtered_data = filtered_data[
                filtered_data['Department'].str.contains(department, case=False, na=False)
            ]

        filtered_data = filtered_data.to_dict(orient='records')

    return render_template('dashboard.html', students=filtered_data)

if __name__ == '__main__':
    app.run(debug=True)
