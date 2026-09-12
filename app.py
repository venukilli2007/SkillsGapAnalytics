from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

app.secret_key = "skills-gap-secret-key"

DATABASE = "skillsgap.db"

def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS profiles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            college TEXT,
            course TEXT,
            career_goal TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS skills (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT,
            skill TEXT,
            level TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# =========================================================
# DATABASE CONNECTION
# =========================================================

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


# =========================================================
# HOME / LOGIN PAGE
# =========================================================

@app.route("/")
def home():
    return render_template("login.html")


# =========================================================
# REGISTER PAGE
# =========================================================

@app.route("/register")
def register_page():
    return render_template("register.html")


# =========================================================
# REGISTER USER
# =========================================================

@app.route("/register", methods=["POST"])
def register():

    name = request.form["name"]
    email = request.form["email"]
    password = request.form["password"]

    password_hash = generate_password_hash(password)

    conn = get_db()
    cursor = conn.cursor()

    try:

        cursor.execute(
            """
            INSERT INTO users (name, email, password)
            VALUES (?, ?, ?)
            """,
            (name, email, password_hash)
        )

        conn.commit()

    except sqlite3.IntegrityError:

        conn.close()

        return """
        <h1>Email already registered</h1>
        <br>
        <a href="/register">Try Again</a>
        """

    conn.close()

    return redirect(url_for("home"))


# =========================================================
# LOGIN
# =========================================================

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        conn = get_db()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT * FROM users
            WHERE email = ?
            """,
            (email,)
        )

        user = cursor.fetchone()

        conn.close()

        if user and check_password_hash(user["password"], password):

            session["user_email"] = user["email"]
            session["user_name"] = user["name"]

            return redirect(url_for("dashboard"))

        else:

            return """
            <h1>Invalid Email or Password</h1>
            <br>
            <a href="/">Back to Login</a>
            """

    return render_template("login.html")


# =========================================================
# DASHBOARD
# =========================================================

@app.route("/dashboard")
def dashboard():

    if "user_email" not in session:
        return redirect(url_for("home"))

    email = session["user_email"]

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT skill, level
        FROM skills
        WHERE email = ?
        """,
        (email,)
    )

    skills = cursor.fetchall()

    conn.close()

    total_skills = len(skills)

    beginner = sum(
        1 for skill in skills
        if skill["level"] == "Beginner"
    )

    intermediate = sum(
        1 for skill in skills
        if skill["level"] == "Intermediate"
    )

    advanced = sum(
        1 for skill in skills
        if skill["level"] == "Advanced"
    )

    # -----------------------------------------------------
    # CAREER READINESS SCORE
    # -----------------------------------------------------

    if total_skills == 0:

        skill_score = 0
        readiness = 0

    else:

        total_score = 0

        for skill in skills:

            if skill["level"] == "Beginner":
                total_score += 35

            elif skill["level"] == "Intermediate":
                total_score += 70

            elif skill["level"] == "Advanced":
                total_score += 100

        skill_score = round(total_score / total_skills)
        readiness = skill_score

    # -----------------------------------------------------
    # READINESS MESSAGE
    # -----------------------------------------------------

    if readiness >= 85:

        readiness_message = "Excellent! You are highly career ready."

    elif readiness >= 70:

        readiness_message = "Great progress! You are becoming career ready."

    elif readiness >= 50:

        readiness_message = "Good start! Keep developing your skills."

    elif readiness > 0:

        readiness_message = "You are getting started. Keep learning."

    else:

        readiness_message = "Add your first skill to begin your journey."

    return render_template(
        "dashboard.html",
        skills=skills,
        total_skills=total_skills,
        beginner=beginner,
        intermediate=intermediate,
        advanced=advanced,
        skill_score=skill_score,
        readiness=readiness,
        readiness_message=readiness_message
    )


# =========================================================
# PROFILE
# =========================================================

@app.route("/profile", methods=["GET", "POST"])
def profile():

    if "user_email" not in session:
        return redirect(url_for("home"))

    email = session["user_email"]

    if request.method == "POST":

        name = request.form["name"]
        college = request.form["college"]
        course = request.form["course"]
        career_goal = request.form["career_goal"]

        conn = get_db()
        cursor = conn.cursor()

        # Check whether profile already exists
        cursor.execute(
            """
            SELECT id
            FROM profiles
            WHERE email = ?
            """,
            (email,)
        )

        existing_profile = cursor.fetchone()

        if existing_profile:

            cursor.execute(
                """
                UPDATE profiles

                SET name = ?,
                    college = ?,
                    course = ?,
                    career_goal = ?

                WHERE email = ?
                """,
                (
                    name,
                    college,
                    course,
                    career_goal,
                    email
                )
            )

        else:

            cursor.execute(
                """
                INSERT INTO profiles
                (name, email, college, course, career_goal)

                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    name,
                    email,
                    college,
                    course,
                    career_goal
                )
            )

        conn.commit()
        conn.close()

        session["user_name"] = name

        return """
        <h1>Profile Saved Successfully!</h1>

        <br>

        <a href="/dashboard">
            Back to Dashboard
        </a>
        """

    # -----------------------------------------------------
    # GET PROFILE
    # -----------------------------------------------------

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM profiles
        WHERE email = ?
        """,
        (email,)
    )

    profile_data = cursor.fetchone()

    conn.close()

    return render_template(
        "profile.html",
        profile=profile_data
    )


# =========================================================
# SKILLS PAGE
# =========================================================

@app.route("/skills", methods=["GET", "POST"])
def skills():

    if "user_email" not in session:
        return redirect(url_for("home"))

    email = session["user_email"]

    # =====================================================
    # ADD NEW SKILL
    # =====================================================

    if request.method == "POST":

        skill = request.form["skill"]
        level = request.form["level"]

        conn = get_db()
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO skills
            (email, skill, level)

            VALUES (?, ?, ?)
            """,
            (
                email,
                skill,
                level
            )
        )

        conn.commit()
        conn.close()

        return redirect(url_for("skills"))

    # =====================================================
    # GET USER SKILLS
    # =====================================================

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id, skill, level
        FROM skills
        WHERE email = ?
        ORDER BY id DESC
        """,
        (email,)
    )

    user_skills = cursor.fetchall()

    conn.close()

    # =====================================================
    # SKILL ANALYTICS
    # =====================================================

    total_skills = len(user_skills)

    beginner = 0
    intermediate = 0
    advanced = 0

    for skill in user_skills:

        if skill["level"] == "Beginner":
            beginner += 1

        elif skill["level"] == "Intermediate":
            intermediate += 1

        elif skill["level"] == "Advanced":
            advanced += 1

    # =====================================================
    # CAREER READINESS
    # =====================================================

    if total_skills == 0:

        readiness = 0

    else:

        total_score = 0

        for skill in user_skills:

            if skill["level"] == "Beginner":
                total_score += 35

            elif skill["level"] == "Intermediate":
                total_score += 70

            elif skill["level"] == "Advanced":
                total_score += 100

        readiness = round(
            total_score / total_skills
        )

    # =====================================================
    # READINESS STATUS
    # =====================================================

    if readiness >= 85:

        readiness_status = "Excellent"

    elif readiness >= 70:

        readiness_status = "Strong"

    elif readiness >= 50:

        readiness_status = "Developing"

    elif readiness > 0:

        readiness_status = "Getting Started"

    else:

        readiness_status = "No Skills Yet"

    # =====================================================
    # RECOMMENDATION
    # =====================================================

    if total_skills == 0:

        recommendation = (
            "Add your first skill to start building "
            "your professional profile."
        )

    elif beginner > intermediate and beginner > advanced:

        recommendation = (
            "Focus on improving your beginner-level "
            "skills through projects and practice."
        )

    elif intermediate >= beginner and intermediate >= advanced:

        recommendation = (
            "You have a solid foundation. Build "
            "real-world projects to reach advanced level."
        )

    else:

        recommendation = (
            "Excellent skill development. Continue "
            "building advanced projects and specialization."
        )

    # =====================================================
    # SEND EVERYTHING TO SKILLS.HTML
    # =====================================================

    return render_template(
        "skills.html",

        skills=user_skills,

        total_skills=total_skills,

        beginner=beginner,

        intermediate=intermediate,

        advanced=advanced,

        readiness=readiness,

        readiness_status=readiness_status,

        recommendation=recommendation
    )


# =========================================================
# SKILL GAP RESULTS
# =========================================================

@app.route("/skill-gap-results")
def skill_gap_results():

    if "user_email" not in session:
        return redirect(url_for("home"))

    email = session["user_email"]

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT skill, level
        FROM skills
        WHERE email = ?
        """,
        (email,)
    )

    skills = cursor.fetchall()

    conn.close()

    results = []

    for skill in skills:

        skill_name = skill["skill"]
        level = skill["level"]

        if level == "Beginner":

            gap = "High"

            recommendation = (
                "Learn the fundamentals, practice basic "
                "exercises and complete beginner-level projects."
            )

        elif level == "Intermediate":

            gap = "Medium"

            recommendation = (
                "Build real-world projects, improve problem "
                "solving and learn advanced concepts."
            )

        elif level == "Advanced":

            gap = "Low"

            recommendation = (
                "Work on advanced projects, optimize your "
                "solutions and explore expert-level concepts."
            )

        else:

            gap = "Unknown"

            recommendation = (
                "Please select a valid skill level."
            )

        results.append(
            {
                "skill": skill_name,
                "level": level,
                "gap": gap,
                "recommendation": recommendation
            }
        )

    return render_template(
        "skill_gap_results.html",
        results=results
    )


# =========================================================
# DELETE SKILL
# =========================================================

@app.route(
    "/delete-skill/<int:skill_id>",
    methods=["POST"]
)
def delete_skill(skill_id):

    if "user_email" not in session:
        return redirect(url_for("home"))

    email = session["user_email"]

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        """
        DELETE FROM skills

        WHERE id = ?
        AND email = ?
        """,
        (
            skill_id,
            email
        )
    )

    conn.commit()
    conn.close()

    return redirect(url_for("skills"))


# =========================================================
# LOGOUT
# =========================================================

@app.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("home"))


# =========================================================
# RUN APPLICATION
# =========================================================

if __name__ == "__main__":

    app.run(
        debug=True
    )