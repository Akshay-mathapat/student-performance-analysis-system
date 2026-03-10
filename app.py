import streamlit as st
import pandas as pd
import math

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(
    page_title="Student Performance System",
    page_icon="🎓",
    layout="wide"
)

# -----------------------------
# Session Storage
# -----------------------------
if "students" not in st.session_state:
    st.session_state.students = []

subjects = [
    "Mathematics",
    "Physics",
    "Programming",
    "Electronics",
    "Signal Processing"
]

# -----------------------------
# Helper Functions
# -----------------------------
def calculate_grade(avg):

    if avg >= 90:
        return "A"
    elif avg >= 80:
        return "B"
    elif avg >= 70:
        return "C"
    elif avg >= 60:
        return "D"
    else:
        return "F"

def student_dataframe():

    data = []

    for s in st.session_state.students:

        avg = sum(s["marks"])/len(s["marks"])

        row = {
            "ID": s["id"],
            "Name": s["name"],
            "Branch": s["branch"],
            "Math": s["marks"][0],
            "Physics": s["marks"][1],
            "Programming": s["marks"][2],
            "Electronics": s["marks"][3],
            "Signal Processing": s["marks"][4],
            "Average": round(avg,2),
            "Grade": calculate_grade(avg)
        }

        data.append(row)

    return pd.DataFrame(data)

# -----------------------------
# Title
# -----------------------------
st.title("🎓 Student Performance Analysis System")

# -----------------------------
# Sidebar
# -----------------------------
menu = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Add Student",
        "Student Records",
        "Search Student",
        "Statistics"
    ]
)

# -----------------------------
# Dashboard
# -----------------------------
if menu == "Dashboard":

    st.header("📊 Dashboard Overview")

    df = student_dataframe()

    col1,col2,col3 = st.columns(3)

    col1.metric("Total Students", len(st.session_state.students))

    if not df.empty:

        topper = df.loc[df["Average"].idxmax()]
        col2.metric("Topper", topper["Name"])
        col3.metric("Top Score", round(topper["Average"],2))

    else:
        col2.metric("Topper","N/A")
        col3.metric("Top Score","N/A")

    st.divider()

    if not df.empty:
        st.subheader("Student Performance Table")
        st.dataframe(df,use_container_width=True)

# -----------------------------
# Add Student
# -----------------------------
elif menu == "Add Student":

    st.header("➕ Add Student")

    with st.form("student_form"):

        col1,col2,col3 = st.columns(3)

        sid = col1.text_input("Student ID")
        name = col2.text_input("Name")
        branch = col3.text_input("Branch")

        marks = []

        st.subheader("Enter Marks")

        for subject in subjects:
            marks.append(st.number_input(subject,0,100))

        submitted = st.form_submit_button("Add Student")

        if submitted:

            student = {
                "id":sid,
                "name":name,
                "branch":branch,
                "marks":marks
            }

            st.session_state.students.append(student)

            st.success("Student Added Successfully!")

# -----------------------------
# Student Records
# -----------------------------
elif menu == "Student Records":

    st.header("📋 Student Records")

    df = student_dataframe()

    if df.empty:
        st.warning("No student records available")
    else:
        st.dataframe(df,use_container_width=True)

# -----------------------------
# Search Student
# -----------------------------
elif menu == "Search Student":

    st.header("🔎 Search Student")

    search_id = st.text_input("Enter Student ID")

    if st.button("Search"):

        found = None

        for s in st.session_state.students:

            if s["id"] == search_id:
                found = s

        if found:

            avg = sum(found["marks"])/len(found["marks"])

            st.success("Student Found")

            st.write("Name:",found["name"])
            st.write("Branch:",found["branch"])
            st.write("Marks:",found["marks"])
            st.write("Average:",round(avg,2))
            st.write("Grade:",calculate_grade(avg))

        else:
            st.error("Student not found")

# -----------------------------
# Statistics
# -----------------------------
elif menu == "Statistics":

    st.header("📈 Statistical Analysis")

    df = student_dataframe()

    if df.empty:
        st.warning("No data available")
    else:

        st.subheader("Subject Average")

        subject_avg = {}

        for i,sub in enumerate(subjects):
            subject_avg[sub] = df.iloc[:,3+i].mean()

        st.bar_chart(subject_avg)

        st.subheader("Grade Distribution")

        grade_counts = df["Grade"].value_counts()

        st.bar_chart(grade_counts)

        st.subheader("Standard Deviation")

        all_marks = []

        for s in st.session_state.students:
            all_marks.extend(s["marks"])

        mean = sum(all_marks)/len(all_marks)

        variance = sum((x-mean)**2 for x in all_marks)/len(all_marks)

        std = math.sqrt(variance)

        st.metric("Standard Deviation", round(std,2))