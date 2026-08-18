import streamlit as st
import json
import os

# File where library data will be saved permanently
DATA_FILE = "library_data.json"

# Sample initial data if no saved file exists
default_books = {
    "101": {"title": "Python Programming", "author": "E. Balagurusamy", "issued_to": None},
    "102": {"title": "Data Structures", "author": "Seymour Lipschutz", "issued_to": None},
    "103": {"title": "Computer Networks", "author": "Andrew S. Tanenbaum", "issued_to": None}
}

def load_data():
    """Loads books from JSON file if it exists, otherwise loads default books."""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    return default_books

def save_data(books):
    """Saves book data back to JSON file."""
    with open(DATA_FILE, "w") as file:
        json.dump(books, file, indent=4)

# Initialize data session state storage for Streamlit web app
if 'books' not in st.session_state:
    st.session_state.books = load_data()

books = st.session_state.books

# Web page visual configuration setup
st.set_page_config(page_title="AKTU Library Web App", page_icon="📚", layout="wide")
st.title("📚 AKTU Library Management System")
st.markdown("---")

# Navigation sidebar drop down interaction 
menu = st.sidebar.selectbox(
    "Navigation Menu",
    ["Display Books", "Add New Book", "Issue Book", "Return Book", "Search Book"]
)

if menu == "Display Books":
    st.header("📋 Current Library Catalog")
    if not books:
        st.warning("No books in the database.")
    else:
        table_data = [
            {
                "Book ID": k,
                "Title": v["title"],
                "Author": v["author"],
                "Status": f"Issued to {v['issued_to']}" if v["issued_to"] else "Available"
            }
            for k, v in books.items()
        ]
        st.table(table_data)

elif menu == "Add New Book":
    st.header("➕ Add a New Book")
    with st.form("add_book"):
        b_id = st.text_input("Book ID")
        title = st.text_input("Title")
        author = st.text_input("Author")
        if st.form_submit_button("Add Book"):
            if b_id in books:
                st.error("Book ID already exists!")
            elif b_id and title and author:
                books[b_id] = {"title": title, "author": author, "issued_to": None}
                save_data(books)
                st.success(f"Added {title} successfully!")
            else:
                st.error("Please fill all fields.")

elif menu == "Issue Book":
    st.header("📖 Issue a Book")
    avail = {k: v for k, v in books.items() if v["issued_to"] is None}
    if not avail:
        st.info("No books available to issue.")
    else:
        options = [f"{k} - {v['title']}" for k, v in avail.items()]
        selected = st.selectbox("Select Book", options)
        student = st.text_input("Student Name / Roll No.")
        if st.button("Issue"):
            if student.strip():
                book_id = selected.split(" - ")[0]
                books[book_id]["issued_to"] = student
                save_data(books)
                st.success("Book issued successfully!")
                st.rerun()
            else:
                st.error("Please provide student info.")

elif menu == "Return Book":
    st.header("🔄 Return Book")
    issued = {k: v for k, v in books.items() if v["issued_to"] is not None}
    if not issued:
        st.info("No books currently issued.")
    else:
        options = [f"{k} - {v['title']} ({v['issued_to']})" for k, v in issued.items()]
        selected = st.selectbox("Select Book to Return", options)
        if st.button("Return"):
            book_id = selected.split(" - ")[0]
            books[book_id]["issued_to"] = None
            save_data(books)
            st.success("Book returned successfully!")
            st.rerun()

elif menu == "Search Book":
    st.header("🔍 Search Catalog")
    query = st.text_input("Enter Book ID or Title to search").strip().lower()
    if query:
        found = False
        for book_id, info in books.items():
            if query == book_id.lower() or query in info["title"].lower():
                status = f"Issued to {info['issued_to']}" if info['issued_to'] else "Available"
                st.info(f"**Found** -> ID: {book_id} | Title: {info['title']} | Author: {info['author']} | Status: {status}")
                found = True
        if not found:
            st.error("No matching book found.")

