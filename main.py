import streamlit as st
from PIL import Image
from ocr import *
import mysql.connector
import pandas as pd
from backend import *
import time


# Display the DataFrame

def get_state():
    if 'show_button_b' not in st.session_state:
        st.session_state.show_button_b = False
    return st.session_state

state = get_state()

# Main Streamlit app

st.title("Customer Data Extract Using OCR")

st.header("",divider='rainbow')

    
    
col1, col2 = st.columns([5.7,3])

with col1:
    uploaded_image = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
    if uploaded_image:
        image = Image.open(uploaded_image)

        # Resize the image to 220x140
        resized_image = image.resize((420, 280))

        st.image(resized_image, caption="Resized Image (220x140)")

    def main():
        data=[]
        # Add a button to extract information from the image
        try:
            if st.button("Extract"):     
                with st.spinner('OCR in progress...'):
                    raw_extracted_text = ocr(uploaded_image)
                    raw_extracted_text = raw_extracted_text.lower()
                    print(raw_extracted_text)
                    st.success('OCR completed!')
                    name, title = extract_name_and_title(raw_extracted_text)
                    data.append(name)
                    data.append(title)
                    name = st.text_input("Name", value=name)
                    
                    title = st.text_input("Title", value=title)
                    
                    # contact = st.text_input("Extracted Information", value=extracted_text)
                    email = extract_email_addresses(raw_extracted_text)
                    email = st.text_input("Email", value=(email[0]))
                    # email= ",".join(email)
                    data.append(email)
                    
                    phone =extract_phone_numbers(raw_extracted_text)
                    phone = st.text_input("Phone Number", value="".join(phone))
                    data.append(phone)
                    
                    website = extract_websites(raw_extracted_text)
                    website = st.text_input("Website Link", value="".join(website))
                    data.append(website)
                    
                    company = extract_address(raw_extracted_text)
                    company = st.text_input("company", value=company)
                    data.append(company)
                    
                    address = extract_address(raw_extracted_text)
                    address = st.text_input("address", value=address)
                    data.append(address)
                    st.write('Thank you message')
                    state.show_button_b = True
                try:
                    insert_data(name, title, email, phone, website, company, address)
                    st.success('Data insert successful!')
                except Exception as e:
                    st.warning(f"Error inserting data: {e}")
                    
                tab_on = st.button("Exit")
    
                if tab_on == True:   
                    pass   
             
                            
            tab_on = st.toggle("Data",True)
    
            if tab_on == True:
            # Retrieve data from the table
                data = retrieve_data()
                # Display the data in a DataFrame
                df = pd.DataFrame(data, columns=["ID", "Name", "Title", "Email", "Phone", "Website", "Company", "Address"])
                st.write("## Current Data in MySQL Table")
                st.write(df)
                
        except Exception as e:
            time.sleep(1)
            # st.warning(f"upload image")
            
                  
    main()




with col2:
        
    # Display the Streamlit UI
    st.title("Delete Data from MySQL Table")

    del_on = st.toggle('Delete function')

    if del_on:
        st.warning('Carefull, Enter correct user ID data remove from Database')
        id_value = st.text_input("Enter the ID of the row you want to delete")

        if st.button("Delete ID"):
            delete_row(id_value)
            st.success(f"Row with ID {id_value} deleted successfully!")




    # Global variable for the database connection
    db_connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='1022',
            database='guvi'
    )


    # Display the Streamlit UI
    st.title("Update Data in MySQL Table")


    on = st.toggle('Activate Database Update')

    if on:
        st.write('Feature activated!!! ')

        # Retrieve data from the table
        cursor = db_connection.cursor()
        cursor.execute("SELECT ID FROM ocr")
        ids = [row[0] for row in cursor.fetchall()]
        print(ids)
        # User input for updating data
        st.write("## Update Data")
        selected_id = st.selectbox("Select ID to Update", ids)

        # Fetch current values for the selected ID
        cursor.execute("SELECT * FROM ocr WHERE ID = %s", (selected_id,))
        data = cursor.fetchone()

        if data:
            name = st.text_input("Name", value=data[1])
            title = st.text_input("Title", value=data[2])
            email = st.text_input("Email", value=data[3])
            phone = st.text_input("Phone", value=data[4])
            website = st.text_input("Website", value=data[5])
            company = st.text_input("Company", value=data[6])
            address = st.text_input("Address", value=data[7])

            if st.button("Update Row"):
                update_data(selected_id, name, title, email, phone, website, company, address)
                st.success(f"Row with ID {selected_id} updated successfully!")
        else:
            st.error("No data found for the selected ID.")
            
    

if __name__ == "__main__":
   main()