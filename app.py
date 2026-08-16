from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)

app.secret_key = "skills-gap-secret-key"


@app.route("/")
def home():
    return render_template("login.html")


@app.route("/register")
def register_page():
    return render_template("register.html")


@app.route("/register", methods=["POST"])
def register():
    name = request.form["name"]
    email = request.form["email"]
    password = request.form["password"]

    conn = sqlite3.connect("skillsgap.db")
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
            (name, email, password)
        )
        conn.commit()
    except sqlite3.IntegrityError:
        conn.close()
        return "Email already registered. <a href='/register'>Try again</a>"

    conn.close()

    return redirect(url_for("home"))


@app.route("/login", methods=["POST"])
def login():
    email = request.form["email"]
    password = request.form["password"]

    conn = sqlite3.connect("skillsgap.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE email=? AND password=?",
        (email, password)
    )

    user = cursor.fetchone()
    conn.close()

    if user:
        session["user_email"] = user[2]
        session["user_name"] = user[1]

        return redirect(url_for("dashboard"))
    else:
        return "Invalid Email or Password"

@app.route("/dashboard")
def dashboard():
    if "user_email" not in session:
        return redirect(url_for("home"))

    email = session["user_email"]

    conn = sqlite3.connect("skillsgap.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT skill, level FROM skills WHERE email = ?",
        (email,)
    )

    skills = cursor.fetchall()
    conn.close()

    total_skills = len(skills)
    beginner = sum(1 for skill in skills if skill[1] == "Beginner")
    intermediate = sum(1 for skill in skills if skill[1] == "Intermediate")
    advanced = sum(1 for skill in skills if skill[1] == "Advanced")

    return render_template(
        "dashboard.html",
        skills=skills,
        total_skills=total_skills,
        beginner=beginner,
        intermediate=intermediate,
        advanced=advanced
    )

@app.route("/profile", methods=["GET", "POST"])
def profile():

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        college = request.form["college"]
        course = request.form["course"]
        career_goal = request.form["career_goal"]

        conn = sqlite3.connect("skillsgap.db")
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO profiles
            (name, email, college, course, career_goal)
            VALUES (?, ?, ?, ?, ?)
        """, (name, email, college, course, career_goal))

        conn.commit()
        conn.close()

        return """
        <h1>Profile Saved Successfully!</h1>
        <a href="/dashboard">Back to Dashboard</a>
        """

    return render_template("profile.html")

@app.route("/skills", methods=["GET", "POST"])
def skills():

    if "user_email" not in session:
        return redirect(url_for("home"))

    if request.method == "POST":

        skill = request.form["skill"]
        level = request.form["level"]

        email = session["user_email"]

        conn = sqlite3.connect("skillsgap.db")
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO skills (email, skill, level)
            VALUES (?, ?, ?)
        """, (email, skill, level))

        print("SAVING:", email, skill, level)

        conn.commit()
        conn.close()

        return """
        <h1>Skill Added Successfully!</h1>
        <br>
        <a href="/skills">Add Another Skill</a>
        <br><br>
        <a href="/dashboard">Back to Dashboard</a>
        """

    return render_template("skills.html")

@app.route("/skill-gap-results")
def skill_gap_results():

    if "user_email" not in session:
        return redirect(url_for("home"))

    email = session["user_email"]

    conn = sqlite3.connect("skillsgap.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT skill, level FROM skills WHERE email = ?",
        (email,)
    )

    skills = cursor.fetchall()
    conn.close()

    results = []

    for skill, level in skills:

        if level == "Beginner":
            gap = "High"
            recommendation = (
                "Learn the fundamentals, practice basic exercises, "
                "and complete beginner-level projects."
            )

        elif level == "Intermediate":
            gap = "Medium"
            recommendation = (
                "Build real-world projects, improve problem-solving, "
                "and learn advanced concepts."
            )

        elif level == "Advanced":
            gap = "Low"
            recommendation = (
                "Work on advanced projects, optimize your solutions, "
                "and explore expert-level concepts."
            )

        else:
            gap = "Unknown"
            recommendation = "Please select a valid skill level."

        results.append({
            "skill": skill,
            "level": level,
            "gap": gap,
            "recommendation": recommendation
        })

    return render_template(
        "skill_gap_results.html",
        results=results
    )

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))

@app.route("/delete-skill/<int:skill_id>", methods=["POST"])
def delete_skill(skill_id):
    if "user_email" not in session:
        return redirect(url_for("home"))

    email = session["user_email"]

    conn = sqlite3.connect("skillsgap.db")
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM skills WHERE id = ? AND email = ?",
        (skill_id, email)
    )

    conn.commit()
    conn.close()

    return redirect(url_for("skills"))


if __name__ == "__main__":
    app.run(debug=True)