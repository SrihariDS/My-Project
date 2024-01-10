
from tkinter import *
from tkinter import MULTIPLE
from tkinter.ttk import Combobox
import tkinter.messagebox as mb
import sqlite3

# Global variables
name_entry = None
number_entry = None
Nick_entry = None
contacts_listbox = None
cursor = None
connector = None



def login():
    if username_entry.get() == "srihari" and password_entry.get() == "123":
        login_window.destroy
def open_main_window():
    global window, name_entry, number_entry, Nick_entry, Mail_entry, contacts_listbox, cursor, connector
    window = Tk()
    window.title("Contact Book")
    window.geometry('1000x500')
    window.resizable(False, False)
    window.configure(bg="#c2d1ff")

    # Creating the StringVar variables
    global name_strvar, number_strvar, Nick_strvar, Mail_strvar
    name_strvar = StringVar()
    number_strvar = StringVar()
    Nick_strvar = StringVar()
    Mail_strvar = StringVar()
    
    ### Top frame
    Top_frame = Frame(window, bg="#ebf0ff", width=1000, height=100)
    Top_frame.place(x=0, y=0)

    Label(Top_frame, text="CONTACT BOOK", font="arial 20 bold", bg="white", fg="#002e4d").place(x=400, y=30)
    Label(window, text="Name:", font="arial 15 bold", bg="#ffffff", fg="black").place(x=100, y=150)
    Label(window, text="Number:", font="arial 15 bold", bg="#ffffff", fg="black").place(x=100, y=200)
    Label(window, text="Nick Name:", font="arial 15 bold", bg="#ffffff", fg="black").place(x=100, y=250)
   
    # Entry fields
    name_entry = Entry(window)
    name_entry.place(x=250, y=150)

    number_entry = Entry(window)
    number_entry.place(x=250, y=200)

    Nick_entry = Entry(window)  # Fix: create Entry for Nick
    Nick_entry.place(x=250, y=250)

    # Add New button
    add_contact_button = Button(window, text="Add New", width=10, bg="#e6ffff", font="arial 14 bold", command=submit_record)
    add_contact_button.place(x=460, y=180)

    view_button = Button(window, text="View Contact", width=10, bg="#e6ffff", font="arial 14 bold", command=view_record)
    view_button.place(x=460, y=230)

    clear_button = Button(window, text="Clear Contact", width=13, bg="#e6ffff", font="arial 14 bold", command=clear_record)
    clear_button.place(x=460, y=280)

    delete_button = Button(window, text="Delete Contact", width=13, bg="#e6ffff", font="arial 14 bold", command=delete_record)
    delete_button.place(x=460, y=330)

    delete_all_button = Button(window, text="Delete All Contact", width=15, bg="#e6ffff", font="arial 14 bold", command=delete_all_records)
    delete_all_button.place(x=460, y=380)




    exit_button = Button(window, text="Exit", width=10, bg="#e6ffff", font="arial 14 bold", command=window.destroy)
    exit_button.place(x=480, y=450)


    try:
        connector = sqlite3.connect('contact_book.db')
        cursor = connector.cursor()
        # Creating the table if it doesn't exist
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS CONTACT_BOOK (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                NAME TEXT,
                PHONE_NUMBER TEXT,
                NICK TEXT
            )
        ''')
        connector.commit()
    except sqlite3.Error as e:
        print("Error connecting to the database:", e)
        mb.showerror("Database Error", "Error connecting to the database.")

    
    # Contacts listbox
    contacts_listbox = Listbox(window, font="Roboto 12", bg="white", selectbackground="#a6a6a6", selectmode=MULTIPLE)
    contacts_listbox.place(x=550, y=50, width=300, height=350)
    scroller = Scrollbar(contacts_listbox, orient=VERTICAL, command=contacts_listbox.yview)
    scroller.place(relx=0.93, rely=0, relheight=1)
    contacts_listbox.config(yscrollcommand=scroller.set)
    contacts_listbox.place(relx=0.1, rely=0.15)

    list_contacts()
    
def submit_record():
    global name_entry, number_entry, Nick_entry, contacts_listbox
    name = name_entry.get()
    number = number_entry.get()
    Nick = Nick_entry.get()
    

    if name == '' or number == '':
        mb.showerror('Error!', "Please fill all the required fields!")
    else:
        cursor.execute("INSERT INTO CONTACT_BOOK (NAME, PHONE_NUMBER, NICK) VALUES (?, ?, ?)", (name, number, Nick))
        connector.commit()
        mb.showinfo('Contact added', 'Contact stored successfully!')
        list_contacts()
        clear_fields()

def list_contacts():
    global contacts_listbox
    contacts_listbox.delete(0, END)
    curr = cursor.execute('SELECT NAME FROM CONTACT_BOOK')
    fetch = curr.fetchall()

    for data in fetch:
        contacts_listbox.insert(END, data)

def clear_fields():
    global name_entry, number_entry, Nick_entry, contacts_listbox
    name_entry.delete(0, END)
    number_entry.delete(0, END)
    Nick_entry.delete(0, END)
    
def delete_record():
    global contacts_listbox, connector, cursor

    if not contacts_listbox.get(ACTIVE):
        mb.showerror("No item selected", "You have not selected any item!")

    cursor.execute('DELETE FROM CONTACT_BOOK WHERE NAME = ?', (contacts_listbox.get(ACTIVE)))
    connector.commit()

    mb.showinfo('Contact deleted', 'The desired contact has been deleted')
    contacts_listbox.delete(0, END)
    list_contacts()


def view_record():
    global contacts_listbox, cursor, name_entry, number_entry, Nick_entry

    selected_contact = contacts_listbox.curselection()
    if not selected_contact:
        mb.showerror("No item selected", "You have not selected any item!")
        return

    contact_name = contacts_listbox.get(selected_contact)
    curr = cursor.execute('SELECT * FROM CONTACT_BOOK WHERE NAME=?', contacts_listbox.get(ACTIVE))
    values = curr.fetchall()[0]
    
    clear_fields()

    name_entry.insert(0, values[1])
    number_entry.insert(0, values[2])
    Nick_entry.insert(0, values[3])
  
def clear_fields():
    global name_entry, number_entry, Nick_entry, contacts_listbox

    # Clear entry fields
    name_entry.delete(0, END)
    number_entry.delete(0, END)
    Nick_entry.delete(0, END)
    
    # Clear selection in the listbox
    contacts_listbox.selection_clear(0, END)

def clear_record():
    clear_fields()

def delete_all_records():
    cursor.execute('DELETE FROM CONTACT_BOOK')
    connector.commit()

    mb.showinfo("All records deleted", "All the records in your contact book have been deleted")

    contacts_listbox.delete(0, END)
    list_contacts()


# Initializing the GUI window
login_window = Tk()
login_window.title("Login")
login_window.geometry('500x300')
login_window.resizable(False, False)
login_window.configure(bg="#c2d1ff")

Label(login_window, text="Username:", font="arial 15 bold", bg="#ffffff", fg="black").place(x=100, y=50)
username_entry = Entry(login_window)
username_entry.place(x=250, y=50)

Label(login_window, text="Password:", font="arial 15 bold", bg="#ffffff", fg="black").place(x=100, y=100)
password_entry = Entry(login_window, show="*")
password_entry.place(x=250, y=100)

login_button = Button(login_window, text="Login", width=10, bg="#e6ffff", font="arial 14 bold", command=open_main_window)
login_button.place(x=200, y=200)


login_window.update()
login_window.mainloop()





