import easyocr
from pprint import *
from PIL import Image
import easyocr
import numpy as np
import re
import pandas as pd



def ocr(uploaded_image):
    # Convert the UploadedFile object to a PIL image
    image = Image.open(uploaded_image)
    
    reader = easyocr.Reader(['en'])
    result = reader.readtext(np.array(image))
    
    extracted_text = ""
    for detection in result:
        extracted_text += detection[1] + " "
        
    return extracted_text



def extract_email_addresses(text):
    email_pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[com]{2,}\b"
    email_addresses = re.findall(email_pattern, text)
    return email_addresses

def extract_name_and_title(text):
    name_pattern = r"(?i)\b([A-Z][a-z]+)\s+([A-Z][a-z]+)\s*"
    title_pattern = r"(?i)\b(?:CEO|Founder|Technical|Engineer|Manager|MARKETING|GM)\b"
    name_match = re.search(name_pattern, text)
    title_match = re.search(title_pattern, text)
    name = f"{name_match.group(1)} {name_match.group(2)}" if name_match else None
    title = title_match.group(0) if title_match else None
    return name, title


def extract_phone_numbers(text):
    # Define a regular expression pattern to match phone numbers
    text = text.replace("-","")
    phone_pattern = r"\+\d{9,}"
    # Find all phone numbers in the text
    phone_numbers = re.findall(phone_pattern, text)  
    
    if len(phone_numbers)==0:
        phone_pattern = r"\b\d{9,}\b"
        phone_numbers = re.findall(phone_pattern, text)
        phone_numbers = ",".join(phone_numbers)

    # for i in len(phone_numbers):
    return phone_numbers


def extract_websites(text):
    text = text.replace(' ','').lower()

    # Find all occurrences of "www" in the text
    www_indices = [m.start() for m in re.finditer('www', text)]

    # Initialize a list to store the indices of 'com' following 'www'
    com_indices = []

    # Find the index of 'com' following each 'www'
    for idx in www_indices:
        com_idx = text.find('com', idx)
        if com_idx != -1:
            com_indices.append(com_idx)

    # Slice the text based on the indices of 'www' and 'com'
    slices = []
    for www_idx, com_idx in zip(www_indices, com_indices):
        slices.append(text[www_idx:com_idx + len('com')])

    for s in slices:
        return s
    
    
def extract_address(raw_extracted_text):
    remove_texts = []
    name, title = extract_name_and_title(raw_extracted_text)
    email = extract_email_addresses(raw_extracted_text)
    phone = extract_phone_numbers(raw_extracted_text)
    website = extract_websites(raw_extracted_text)
    remove_texts.extend([name, title, *email, *phone, website])

    cleaned_text = raw_extracted_text.replace('-','')
    for remove_text in remove_texts:
        cleaned_text = cleaned_text.replace(remove_text, "")

    return cleaned_text
        



import mysql.connector
import streamlit as st

def retrieve_data():
    # Establish a connection to the database
    db_connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='1022',
        database='guvi'
    )

    # Create a cursor object
    cursor = db_connection.cursor()

    # Retrieve all data from the table
    select_query = "SELECT * FROM ocr"
    cursor.execute(select_query)
    data = cursor.fetchall()

    # Close the cursor and connection
    cursor.close()
    db_connection.close()

    return data

