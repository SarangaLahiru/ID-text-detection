import streamlit as st
from PIL import Image
import pytesseract

# Function to extract details from ID card image
def extract_id_card_details(img):
    text = pytesseract.image_to_string(img)
    details = {"Name": "", "Date of Birth": "", "Address": "", "ID Number": ""}
    address_lines = []

    for line in text.split('\n'):
        if "First Name:" in line:
            # Assume that the name follows the "First Name:" field
            name_field = line.split(":")[1].strip()
            if "Last Name:" in name_field:
                details["Name"] = name_field.split("Last Name:")[0].strip()
            else:
                details["Name"] = name_field

        elif "Dos:" in line:  # Assuming "Dos:" indicates Date of Birth
            details["Date of Birth"] = line.split(":")[1].strip()
        elif "Address:" in line:
            # Collect all lines that start with "Address:" until a new field is encountered
            address_lines.append(line.split(":")[1].strip())
            next_line = text[text.find(line) + len(line):].split('\n')[0]
            while ":" not in next_line and next_line.strip() != "":
                address_lines.append(next_line.strip())
                next_line = text[text.find(next_line) + len(next_line):].split('\n')[0]
        elif "ID Number:" in line:
            details["ID Number"] = line.split(":")[1].strip()

    details["Address"] = "\n".join(address_lines)
    return text, details

# Streamlit App
st.title("ID Card Details Extraction")

# File uploader widget
uploaded_file = st.file_uploader("Choose an ID card image", type=["jpg", "jpeg", "png"])

# Input fields
if uploaded_file is not None:
    # Display the uploaded image
    st.image(uploaded_file, caption="Uploaded ID Card Image", use_column_width=True)

    # Extract details on button click
    if st.button("Extract Details"):
        img = Image.open(uploaded_file)
        extracted_text, details = extract_id_card_details(img)

        # Show the extracted text
        st.text("Extracted Text:")
        st.text(extracted_text)

        # Auto-fill input fields
        name_input = st.text_input("Name", details["Name"])
        dob_input = st.text_input("Date of Birth", details["Date of Birth"])
        address_input = st.text_area("Address", details["Address"])
        id_number_input = st.text_input("ID Number", details["ID Number"])
