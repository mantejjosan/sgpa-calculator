from flask import Flask, request, render_template

app = Flask(__name__)

def getPercentage(obtained, total):
    return obtained / total * 100

def getGradePoint(percentage):
    if percentage > 100:
        return None
    if percentage >= 90:
        return 10
    elif percentage >= 80:
        return 9
    elif percentage >= 70:
        return 8
    elif percentage >= 60:
        return 7
    elif percentage >= 50:
        return 6
    else:
        return 0

def calculate(gradepoints_credits):
    total_weighted_points = 0
    total_credits = 0
    for grade_point, credit in gradepoints_credits:
        total_weighted_points += grade_point * credit
        total_credits += credit
    return total_weighted_points / total_credits

credits = {"BEEE": 4, "default": 3}
total_marks_list = {"Math": 100, "default": 150}

@app.route("/", methods=["GET", "POST"])
def sgpa_calculator():
    if request.method == "POST":
        marks = {
            "Math": int(request.form.get("Math")),
            "Chemistry": int(request.form.get("Chemistry")),
            "BEEE": int(request.form.get("BEEE")),
            "PPS": int(request.form.get("PPS")),
            "English": int(request.form.get("English")),
        }

        gradepoints_credits = []
        for subject, obtained in marks.items():
            percentage = getPercentage(obtained, total_marks_list.get(subject, 150))
            grade_point = getGradePoint(percentage)
            credit = credits.get(subject, 3)
            gradepoints_credits.append((grade_point, credit))

        sgpa = calculate(gradepoints_credits)
        return render_template("result.html", sgpa=sgpa)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
