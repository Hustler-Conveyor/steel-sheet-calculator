# sheet_calculator.py
import pandas as pd
import math
import streamlit as st

st.set_page_config(page_title="Steel Sheet Calculator", layout="centered")
st.title("🛠️ AR235 Steel Sheet Calculator")

st.markdown("""
This tool calculates how many **60\"x120\"** sheets of AR235 steel you need based on part sizes and quantities.
Upload an Excel file with the following columns:
- **Width (in)**
- **Height (in)**
- **Quantity**

📌 Example:
| Width (in) | Height (in) | Quantity |
|------------|-------------|----------|
| 8          | 120         | 4        |
| 11.625     | 32.8125     | 2        |
""")

uploaded_file = st.file_uploader("📥 Upload your Excel file (.xlsx)", type="xlsx")

SHEET_WIDTH = 60  # inches
SHEET_HEIGHT = 120  # inches
SHEET_AREA = SHEET_WIDTH * SHEET_HEIGHT

def calculate_sheets(df):
    total_area = 0
    for _, row in df.iterrows():
        part_area = row['Width (in)'] * row['Height (in)'] * row['Quantity']
        total_area += part_area
    sheets_needed = math.ceil(total_area / SHEET_AREA)
    return total_area, sheets_needed

if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file)
        st.write("### 📋 Your Uploaded Data:")
        st.dataframe(df)

        if {'Width (in)', 'Height (in)', 'Quantity'}.issubset(df.columns):
            total_area, sheets = calculate_sheets(df)
            st.success(f"✅ Total material area needed: {total_area:.2f} in²")
            st.success(f"📦 You will need **{sheets} full sheet(s)** of 60\" x 120\" AR235 steel.")
        else:
            st.error("❌ Your Excel file must contain columns: 'Width (in)', 'Height (in)', 'Quantity'")
    except Exception as e:
        st.error(f"❌ Error reading file: {e}")
else:
    st.info("Please upload an Excel file to begin.")
