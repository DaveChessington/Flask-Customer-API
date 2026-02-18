import sqlite3
from Customer import Customer

def get_connection():
    return sqlite3.connect("customers.db")

def create_DB():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            phone TEXT NOT NULL,
            address TEXT NOT NULL,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            last_login DATETIME
        );
    """)
    conn.commit()
    conn.close()

def listCustomers():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM customers")
    rows = cursor.fetchall()
    conn.close()
    return [Customer(
        id=r[0],
        first_name=r[1],
        last_name=r[2], 
        email=r[3],
        phone=r[4],
        address=r[5],
        username=r[6], 
        encrypted_password=r[7], 
        last_login=r[8]
    ) for r in rows]

def newCustomer(customer: Customer):
    conn=get_connection()
    cursor=conn.cursor()
    cursor.execute("""
        INSERT INTO customers (
        first_name, 
        last_name, 
        email, 
        phone, 
        address, 
        username, 
        password)
        VALUES (?,?,?,?,?,?,?)
    """,(
        customer.first_name, 
        customer.last_name, 
        customer.email,
        customer.phone, 
        customer.address, 
        customer.username,
        customer.encrypted_password
    ))
    conn.commit()
    conn.close()

def updateCustomer(id, customer:Customer):
    if searchCustomerById(id):
        conn=get_connection()
        cursor=conn.cursor()
        cursor.execute("""
        UPDATE customers
        SET first_name=?,
            last_name=?,
            email=?,
            phone=?,
            address=?,
            username=?,
            password=?
        WHERE id=?
        """,(
        customer.first_name, 
        customer.last_name, 
        customer.email,
        customer.phone, 
        customer.address, 
        customer.username,
        customer.encrypted_password,
        id
        ))
        conn.commit()
        conn.close()



def searchCustomerById(id:int):
    conn=get_connection()
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM customers WHERE id=?",(id,))
    r=cursor.fetchone()
    conn.close()
    
    if r:
        return Customer(
            id=r[0], 
            first_name=r[1], 
            last_name=r[2], 
            email=r[3],
            phone=r[4], 
            address=r[5], 
            username=r[6], 
            encrypted_password=r[7], 
            last_login=r[8]
        )
    return None

def searchCustomer(username:str):
    conn=get_connection()
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM customers WHERE username=?",(username,))
    r=cursor.fetchone()
    conn.close()
    
    if r:
        return Customer(
            id=r[0], 
            first_name=r[1], 
            last_name=r[2], 
            email=r[3],
            phone=r[4], 
            address=r[5], 
            username=r[6], 
            encrypted_password=r[7], 
            last_login=r[8]
        )
    return None

def deleteCustomer(id: int):
    conn=get_connection()
    cursor=conn.cursor()
    cursor.execute("DELETE FROM customers WHERE id =?", (id,))
    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_DB()