import streamlit as st
st.title("Vehicle Owner Detector")
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
     st.write('The vehicle Number entered is', plate)