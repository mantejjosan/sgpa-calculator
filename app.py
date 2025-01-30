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

# Credits for both Chemistry and Physics groups
credits_chemistry = {
    "English": 3,
    "Math": 3,
    "BEEE": 4,
    "Chemistry": 3,
    "PPS": 3
}

credits_physics = {
    "Physics": 5,
    "Edg": 3,
    "Economics": 3,
    "Workshops": 2
}

# Total marks for the respective subjects
total_marks_list = {
    "Math": 100,
    "Edg": 100,
    "Economics": 100,
    "Workshops": 50,
    "Physics": 150
}

@app.route("/", methods=["GET", "POST"])
def sgpa_calculator():
    if request.method == "POST":
        group = request.form.get("group")
        
        # Choose the correct subjects and credits based on the group
        if group == "chemistry":
            credits = credits_chemistry
        elif group == "physics":
            credits = credits_physics
        else:
            return "Invalid group selected"
        
        # Collect marks for the selected group
        marks = {subject: int(request.form.get(subject)) for subject in credits.keys()}

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
    app.run()

