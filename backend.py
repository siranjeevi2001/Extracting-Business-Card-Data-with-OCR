import mysql.connector

def create_table():
    # Establish a connection to the database
    db_connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='1022',
        database='guvi'
    )

    # Create a cursor object
    cursor = db_connection.cursor()

    # Create the table
    create_table_query = """
    CREATE TABLE IF NOT EXISTS ocr (
        ID INT AUTO_INCREMENT PRIMARY KEY,
        Name VARCHAR(255),
        Title VARCHAR(255),
        Email VARCHAR(255),
        Phone VARCHAR(255),
        Website VARCHAR(255),
        Company VARCHAR(255),
        Address VARCHAR(255)
    )
    """
    cursor.execute(create_table_query)

    # Commit the changes and close the connection
    db_connection.commit()
    cursor.close()
    db_connection.close()
    print("Table created successfully!")

def insert(data_to_insert):
    # Establish a connection to the database
    db_connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='1022',
        database='guvi'
    )

    # Create a cursor object
    cursor = db_connection.cursor()

    # Insert data into the table
    insert_query = "INSERT INTO ocr (Name, Title, Email, Phone, Website, Company, Address) VALUES (%s,%s,%s,%s,%s,%s,%s)"
    cursor.execute(insert_query, data_to_insert)
    db_connection.commit()
    cursor.close()
    db_connection.close()
    print("Data inserted successfully!")





def insert_data(name, title, email, phone, website, company, address):
    # Establish a connection to the database
    db_connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='1022',
        database='guvi'
    )

    # Create a cursor object
    cursor = db_connection.cursor()

    # Insert data into the table
    insert_query = "INSERT INTO ocr (Name, Title, Email, Phone, Website, Company, Address) VALUES (%s,%s,%s,%s,%s,%s,%s)"
    data_to_insert = (name, title, email, phone, website, company, address)
    cursor.execute(insert_query, data_to_insert)
    db_connection.commit()
    cursor.close()
    db_connection.close()
    print("Data inserted successfully!")


import mysql.connector


# Global variable for the database connection
db_connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='1022',
        database='guvi'
)



def retrieve_data():
    # Global variable for the database connection
    db_connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='1022',
            database='guvi'
    )
    # global db_connection
    # Create a cursor object
    cursor = db_connection.cursor()

    # Retrieve all data from the table
    select_query = "SELECT * FROM ocr"
    cursor.execute(select_query)
    data = cursor.fetchall()

    # Close the cursor
    cursor.close()

    return data

def delete_row(id_value):
    db_connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='1022',
        database='guvi'
    )

    # global db_connection
    # Create a cursor object
    cursor = db_connection.cursor()

    # Delete the row with the specified ID
    delete_query = "DELETE FROM ocr WHERE ID = %s"
    cursor.execute(delete_query, (id_value,))

    # Commit the transaction
    db_connection.commit()

    # Close the cursor
    cursor.close()



def update_data(id_value, name, title, email, phone, website, company, address):
    global db_connection
    # Create a cursor object
    cursor = db_connection.cursor()

    # Update the row with the specified ID
    update_query = "UPDATE ocr SET Name=%s, Title=%s, Email=%s, Phone=%s, Website=%s, Company=%s, Address=%s WHERE ID=%s"
    data_to_update = (name, title, email, phone, website, company, address, id_value)
    cursor.execute(update_query, data_to_update)

    # Commit the transaction
    db_connection.commit()

    # Close the cursor
    cursor.close()
