import streamlit as st
import pymupdf
import fitz
import io
from PIL import Image
import pdfminer
from pdfminer.high_level import extract_text_to_fp
from io import BytesIO


st.title("Demo Pdf extract to xml")

# File upload
uploaded_file = st.file_uploader("Choose a file")

#open_file = fitz.open(uploaded_file)
open_file = fitz.open(stream=uploaded_file.read(), filetype='pdf')

# File information
st.write("Number of pages of the uploaded document", len(open_file))

# Text extract
st.subheader("Text extract")

# Use interface to ask the page to extract the text
#number = st.number_input("Which page do you want to extract ?", min_value=1, max_value=len(open_file), step=1)
number = st.number_input("Which page do you want to extract ?", min_value=1, max_value=len(open_file), step=1)


if st.button("Click to process", key=1):
    st.write("The requested page to extract is", number)
    text = open_file[number-1].get_text()
    st.write(text)

# XML creation with PDF miner 6

st.subheader("XML creation")

if st.button("Click to process", key=3):  
    # Convert the PDF to XML and write it to the BytesIO object
    xml_output = BytesIO()
    extract_text_to_fp(uploaded_file, xml_output, output_type='xml')

    # Seek to the beginning of the BytesIO object
    xml_output.seek(0)

    # Read the XML content from the BytesIO object
    xml_content = xml_output.read()

    # Save the XML content in a file
    with open('output.xml', 'wb') as output_file:
        output_file.write(xml_content)

    # Close the BytesIO object
    xml_output.close()

    st.write("XML file created")

# Pictures extract
st.subheader("Pictures extract")

# Use interface to ask the page to extract the text
number_image = st.number_input("Which page do you want to extract pictures ?", min_value=1, max_value=len(open_file), step=1)

# Display of the pictures in the webpage
if st.button("Click to process", key=2):
    st.write("The requested page to extract pictures is", number_image)
    xref = open_file.get_page_images(number_image-1)
    images = []
    for i in range(len(xref)):
        fitz.Pixmap(open_file, xref[i][0]).save("picture_{}.png".format(i))
        st.image(["picture_{}.png".format(i)], caption=["picture_{}.png".format(i)])

