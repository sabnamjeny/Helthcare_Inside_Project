import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import sqlite3
import warnings
warnings.filterwarnings("ignore")

# Database connection
conn = sqlite3.connect('healthcare.db')
cursor = conn.cursor()

st.title("Healthcare Insights Dashboard")
# main.py

# SQLite Connection
conn = sqlite3.connect("healthcare.db")  
cursor = conn.cursor()

# Load Data
@st.cache_data
def load_data():
    query = "SELECT * FROM healthcare_data"
    df = pd.read_sql_query(query, conn)
    return df

df = load_data()
st.write("### Sample Data", df.head())

# Diagnosis-wise Patient Count Section
st.subheader("Diagnosis-wise Patient Count")

query_diagnosis = """
SELECT Diagnosis, COUNT(Patient_ID) AS Total_Patients
FROM healthcare_data
GROUP BY Diagnosis
ORDER BY Total_Patients DESC;
"""

diagnosis_data = pd.read_sql_query(query_diagnosis, conn)

# Plot
fig, ax = plt.subplots(figsize=(10, 5))
ax.bar(diagnosis_data['Diagnosis'], diagnosis_data['Total_Patients'], color='purple')
ax.set_xlabel("Diagnosis")
ax.set_ylabel("Number of Patients")
ax.set_title("Diagnosis-wise Patient Count")
plt.xticks(rotation=45, ha='right')
st.pyplot(fig)



st.subheader("Bed Occupancy Type Distribution")

query_bed = """
SELECT Bed_Occupancy, COUNT(Patient_ID) AS Total_Patients
FROM healthcare_data
GROUP BY Bed_Occupancy
ORDER BY Total_Patients DESC;
"""

bed_data = pd.read_sql_query(query_bed, conn)

fig, ax = plt.subplots()
ax.bar(bed_data['Bed_Occupancy'], bed_data['Total_Patients'], color='purple')
ax.set_xlabel("Bed Occupancy Type")
ax.set_ylabel("Number of Patients")
ax.set_title("Bed Occupancy Type Distribution")
st.pyplot(fig)


st.subheader("Billing Amount Distribution")

query_billing = """
SELECT [Billing Amount], COUNT(Patient_ID) AS Total_Patients
FROM healthcare_data
GROUP BY [Billing Amount]
ORDER BY [Billing Amount];
"""

billing_data = pd.read_sql_query(query_billing, conn)

# Visualization
fig1, ax1 = plt.subplots()
ax1.bar(billing_data['Billing Amount'], billing_data['Total_Patients'], color='orange')
ax1.set_xlabel("Billing Amount")
ax1.set_ylabel("Number of Patients")
ax1.set_title("Billing Amount Distribution")
st.pyplot(fig1)

st.subheader("Health Insurance Amount Distribution")

query_insurance = """
SELECT [Health Insurance Amount], COUNT(Patient_ID) AS Total_Patients
FROM healthcare_data
GROUP BY [Health Insurance Amount]
ORDER BY [Health Insurance Amount];
"""

insurance_data = pd.read_sql_query(query_insurance, conn)

# Visualization
fig2, ax2 = plt.subplots()
ax2.bar(insurance_data['Health Insurance Amount'], insurance_data['Total_Patients'], color='green')
ax2.set_xlabel("Health Insurance Amount")
ax2.set_ylabel("Number of Patients")
ax2.set_title("Health Insurance Amount Distribution")
st.pyplot(fig2)


# Sidebar with options
st.sidebar.title("Select Analysis")
options = [
    "Doctor-wise Count"
]
selection = st.sidebar.selectbox("Select an analysis", options)

# Display selected analysis
if selection == "Doctor-wise Count":
    st.subheader("Doctor-wise Count")
    
    # Group by Doctor and count the number of patients (using 'Patient_ID')
    doctor_count = df.groupby('Doctor')['Patient_ID'].count()
    
    # Display the result in a table
    st.write(doctor_count)

# Sidebar with options
st.sidebar.title("Select Analysis")
options = [
    "Test Frequency"
]
selection = st.sidebar.selectbox("Select an analysis", options)

# Display selected analysis
if selection == "Test Frequency":
    st.subheader("Test Frequency")
    
    # Calculate the frequency of each test
    test_freq = df['Test'].value_counts()
    
    # Display the result
    st.write(test_freq)


# 📅 Follow-up Date Distribution Section
st.subheader("📅 Follow-up Date Distribution (Monthly)")

# 📊 SQL Query
query_followup_date_distribution = """
SELECT strftime('%Y-%m', [Followup Date]) AS Followup_Month, COUNT(Patient_ID) AS Total_Patients
FROM healthcare_data
GROUP BY Followup_Month
ORDER BY Followup_Month;
"""

cursor.execute(query_followup_date_distribution)
followup_data = cursor.fetchall()

# 🧾  Make DataFrame 
df_followup = pd.DataFrame(followup_data, columns=['Followup_Date', 'Total_Patients'])
df_followup['Followup_Date'] = pd.to_datetime(df_followup['Followup_Date'])

# 📈 Plot with matplotlib
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(df_followup['Followup_Date'], df_followup['Total_Patients'], marker='o', color='teal')
ax.set_xlabel('Follow-up Month')
ax.set_ylabel('Number of Patients')
ax.set_title('Monthly Follow-up Date Distribution')
plt.xticks(rotation=45)
plt.tight_layout()
st.pyplot(fig)
conn.close()

# Connect to the database
conn = sqlite3.connect("healthcare.db")
cursor = conn.cursor()

# SQL Query to get feedback distribution
query_feedback = """
SELECT Feedback, COUNT(Patient_ID) AS Total_Patients
FROM healthcare_data
GROUP BY Feedback
ORDER BY Feedback DESC;
"""

try:
    # Execute query
    cursor.execute(query_feedback)
    feedback_data = cursor.fetchall()

    # Create a DataFrame
    df_feedback = pd.DataFrame(feedback_data, columns=['Feedback', 'Total_Patients'])

    # Display in Streamlit
    st.subheader(" Patient Feedback Score Distribution")
    st.write(df_feedback)

    # Create a bar chart using matplotlib
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(df_feedback['Feedback'], df_feedback['Total_Patients'], color='lightgreen')
    ax.set_xlabel('Feedback Rating')
    ax.set_ylabel('Number of Patients')
    ax.set_title('Patient Feedback Distribution')
    plt.xticks(rotation=45)
    st.pyplot(fig)

except Exception as e:
    st.error(f" Error loading data: {e}")

# Close the database connection
conn.close()

