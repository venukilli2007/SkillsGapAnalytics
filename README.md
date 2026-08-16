# SkillsGapAnalytics

## Project Overview

SkillsGapAnalytics is a Flask-based web application designed to help users understand their current technical skills and identify skill gaps.

Users can create an account, maintain their professional profile, add technical skills with proficiency levels, and receive personalized recommendations based on their current skill level.

## Objective

The main objective of SkillsGapAnalytics is to provide a simple platform where users can:

- Create and manage an account
- Maintain their professional profile
- Add technical skills
- Select their current proficiency level
- Analyze skill gaps
- Receive learning recommendations
- View their overall skill summary

## Key Features

### 1. User Registration
Users can create an account using their name, email, and password.

### 2. User Login
Registered users can securely log in and access their dashboard.

### 3. Dashboard
The dashboard provides a visual summary of the user's skills, including:

- Total skills
- Beginner skills
- Intermediate skills
- Advanced skills

### 4. Profile Management
Users can enter:

- Name
- Email
- College
- Course
- Career Goal

### 5. Skill Management
Users can add technical skills and select their current level:

- Beginner
- Intermediate
- Advanced

### 6. Skill Gap Analysis

The application analyzes the selected skill level and determines the corresponding skill gap.

The system provides:

- Current skill level
- Skill gap
- Personalized recommendation

### 7. Logout
Users can securely end their session using the Logout option.

## Skill Gap Logic

The current analysis system works as follows:

| Skill Level | Skill Gap | Recommendation |
|-------------|-----------|----------------|
| Beginner | High | Learn fundamentals and complete beginner projects |
| Intermediate | Medium | Build real-world projects and learn advanced concepts |
| Advanced | Low | Work on advanced projects and expert-level concepts |

## Technologies Used

### Frontend

- HTML5
- CSS3
- Responsive Web Design

### Backend

- Python
- Flask

### Database

- SQLite

### Development Environment

- Visual Studio Code

## Project Structure

```text
SkillsGapAnalytics/
│
├── app.py
├── skillsgap.db
├── requirements.txt
├── README.md
│
├── templates/
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── profile.html
│   ├── skills.html
│   └── skill_gap_results.html
│
└── static/
    └── style.css