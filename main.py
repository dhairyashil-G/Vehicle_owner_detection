import streamlit as st
from gsheetsdb import connect
st.title("Vehicle Owner Detector")

# Use this for nav bar generation
st.markdown('''HTML CODE ''',unsafe_allow_html=True)

conn=connect()

# Perform SQL query on the Google Sheet.
# Uses st.cache to only rerun when the query changes or after 10 min.
def run_query(query):
    rows = conn.execute(query, headers=1)
    rows = rows.fetchall()
    return rows

sheet_url = st.secrets["public_gsheets_url"]
rows = run_query(f'SELECT * FROM "{sheet_url}"')

genre = st.radio(
     "Which process would you use:",
     ('Camera through Detection','Manual Entry'))

if genre == 'Camera through Detection':
    st.write('Opening Camera')
    img_file_buffer = st.camera_input("Take a picture")

    if img_file_buffer is not None:
        # To read image file buffer as bytes:
        bytes_data = img_file_buffer.getvalue()
        # Check the type of bytes_data:
        # Should output: <class 'bytes'>
        st.write(type(bytes_data))
else:
     st.write("Enter manually")
     plate = st.text_input('Number plate', '')
     # st.write('The vehicle Number entered is', plate)
     st.info(f'Vehicle number : {plate}')

# Print results.
for row in rows:
    # st.write(f"{row.Name} has a :{row.VehicleNumberPlate}:")
    if(str(row.Vehicle_Number_Plate)==plate):
        st.write(f"Name : {row.Name}")
        st.write(f" Phone : {row.Mobile}")
        st.write(f" Entry time : {row.Timestamp}")
        st.write(f" College Name : {row.College_Name}")
    else:
        st.write("No Owner Found")