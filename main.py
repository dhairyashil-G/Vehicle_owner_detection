import streamlit as st
import smtplib
import requests
from gsheetsdb import connect
from streamlit_option_menu import option_menu
st.title("Vehicle Owner Detector")

# # Use this for nav bar generation
# st.markdown('''
#     <div class="topnav">
#       <a class="active" href="#home">Home</a>
#       <a href="#contact">Contact</a>
#       <a href=about()>About</a>
#     </div>
#     <style>
#         .topnav {
#           background-color: #333;
#           overflow: hidden;
#         }
#
#         /* Style the links inside the navigation bar */
#         .topnav a {
#           float: left;
#           color: #f2f2f2;
#           text-align: center;
#           padding: 14px 16px;
#           text-decoration: none;
#           font-size: 17px;
#         }
#
#         /* Change the color of links on hover */
#         .topnav a:hover {
#           background-color: #ddd;
#           color: black;
#         }
#
#         /* Add a color to the active/current link */
#         .topnav a.active {
#           background-color: black;
#           color: white;
#         }
#     </style>
# ''',unsafe_allow_html=True)
st.write("Designed by the students of Sinhgad College of Engineering.")

selected=option_menu(
    menu_title=None,
    options=["Home","Feedback","Download","About"],
    icons=["house","inboxes","cloud-download","envelope"],
    orientation="horizontal"
)

conn=connect()

# Perform SQL query on the Google Sheet.
# Uses st.cache to only rerun when the query changes or after 10 min.
@st.cache(ttl=600)
def run_query(query):
    rows = conn.execute(query, headers=1)
    rows = rows.fetchall()
    return rows
sheet_url = st.secrets["public_gsheets_url"]
rows = run_query(f'SELECT * FROM "{sheet_url}"')

if selected=="Home":
    # genre = st.radio(
    #     "Which process would you use:",
    #     ('Manual Entry','Camera through Detection (Feature Coming Soon)'))
    #
    # if genre == 'Camera through Detection (Feature Coming Soon)':
    #     st.write('Opening Camera')
    #     img_file_buffer = st.camera_input("Take a picture")
    #
    #     if img_file_buffer is not None:
    #         # To read image file buffer as bytes:
    #         bytes_data = img_file_buffer.getvalue()
    #         # Check the type of bytes_data:
    #         # Should output: <class 'bytes'>
    #         st.write(type(bytes_data))
    #
    # else:
    # st.write("Enter manually")
    plate = st.text_input('Number plate', '')
    # st.write('The vehicle Number entered is', plate)
    # cleaning plate
    clean_plate = ""
    for ch in plate:
        if ch!=' ':
            clean_plate = clean_plate + ch
    st.info(f'Vehicle number : {clean_plate.upper()}')


    # Print results.
    for row in rows:
        # st.write(f"{row.Name} has a :{row.VehicleNumberPlate}:")
        if (str(row.Vehicle_Number_Plate) == clean_plate.upper()):
            st.success("Record Found...")
            st.text(f"Name : {row.Name}")
            st.text(f"Phone : {int(row.Mobile)}")
            st.text(f"Email : {(row.email)}")
            st.text(f"Entry time : {row.Timestamp}")
            st.text(f"College Name : {row.College_Name}")
            st.info("You can send a text message to the owner by clicking the button below.")

            # Sending text message on phone using textbelt not working in our country(India)
            # if st.button("Send Message"):
            #     num="+91"+str(int(row.Mobile))
            #     resp = requests.post('https://textbelt.com/text', {
            #         'phone': num,
            #         'message': 'This is a message from Sinhgad college Security. Your vehicle is parked at a wrong position. Please contact College security as soon as possible on 020-XXXXXX',
            #         'key': 'textbelt',
            #     })
            #     st.write(resp.json())

            if st.button("Send Mail"):
                s = smtplib.SMTP('smtp.gmail.com', 587)
                s.ehlo()
                s.starttls()
                s.ehlo()
                --------------Changed for security reasons---------------------
                s.login('sender mail id','sender mail password')
                ---------------------------------------------------------------
                message = "This is a message from Sinhgad college Security. Your vehicle is parked at a wrong position. Please contact College security as soon as possible on 020-XXXXXX"
                s.sendmail("dhairyashil.ghatage31@gmail.com", row.email.strip(), message)
                st.info("Mail Sent")
                s.quit()

            break
    else:
        st.error("No Record Found...")

elif selected=="Feedback":
    # st.write("This is Feedback section")
    with st.form(key='my_form'):
        feedback_email = st.text_input('Email Id')
        feedback_text = st.text_input('Your Experience')
        but=st.form_submit_button('Submit')
        if but:
            s = smtplib.SMTP('smtp.gmail.com', 587)
            s.ehlo()
            s.starttls()
            s.ehlo()
            s.login('dhairyashil.ghatage31@gmail.com', 'dhiru2002')
            message = f"Feedback Mail from :{feedback_email}\nFeedback Details:\n{feedback_text}"
            s.sendmail("dhairyashil.ghatage31@gmail.com", 'dhairyasheel.ghatage@gmail.com', message)
            st.info("Mail Sent")
            s.quit()
elif selected=="Download":
    st.write('''Here you can download the records till date by clicking the "Download CSV" Button. ''')
    data=""
    for r in rows:
        data=data+str(r)+"\n"
    st.download_button('Download CSV',data, 'Record.txt')
elif selected=="About":
    st.subheader("This project was part of our Project Based Learning Course and is prepared by a group of members namely :")
    st.text("Hansika Gaidhani(205A036)")
    st.text("Sahil Gannarapwar(205A037)")
    st.text("Shrutika Ganvir(205A038)")
    st.text("Dhairyashil Ghatage(205A039)")
    st.text("Abhishek Ghodke(205A040)")


