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

def display_books(books):
    """Displays all available and issued books."""
    print("\n" + "="*60)
    print(f"{'Book ID':<10} {'Title':<25} {'Author':<20} {'Status'}")
    print("="*60)

    if not books:
        print("No books available in the library database.")
    else:
        for book_id, info in books.items():
            status = f"Issued to {info['issued_to']}" if info['issued_to'] else "Available"
            print(f"{book_id:<10} {info['title']:<25} {info['author']:<20} {status}")
    print("="*60)

def add_book(books):
    """Adds a new book to the library."""
    print("\n--- ADD NEW BOOK ---")
    book_id = input("Enter unique Book ID (e.g., 104): ").strip()

    if book_id in books:
        print("Error: A book with this ID already exists!")
        return

    title = input("Enter Book Title: ").strip()
    author = input("Enter Author Name: ").strip()

    if title and author:
        books[book_id] = {"title": title, "author": author, "issued_to": None}
        save_data(books)
        print(f"Success: '{title}' added to the library!")
    else:
        print("Error: Title and Author cannot be empty.")

def issue_book(books):
    """Issues an available book to a student."""
    print("\n--- ISSUE BOOK ---")
    book_id = input("Enter Book ID to issue: ").strip()

    if book_id not in books:
        print("Error: Book ID not found!")
    elif books[book_id]["issued_to"] is not None:
        print(f"Error: Book is already issued to '{books[book_id]['issued_to']}'.")
    else:
        student_name = input("Enter Student Name / Roll No: ").strip()
        if student_name:
            books[book_id]["issued_to"] = student_name
            save_data(books)
            print(f"Success: '{books[book_id]['title']}' issued to {student_name}.")
        else:
            print("Error: Student details cannot be blank.")

def return_book(books):
    """Returns an issued book back to the library."""
    print("\n--- RETURN BOOK ---")
    book_id = input("Enter Book ID to return: ").strip()

    if book_id not in books:
        print("Error: Book ID not found!")
    elif books[book_id]["issued_to"] is None:
        print("Error: This book was not issued to anyone.")
    else:
        student_name = books[book_id]["issued_to"]
        books[book_id]["issued_to"] = None
        save_data(books)
        print(f"Success: '{books[book_id]['title']}' returned by {student_name}.")

def search_book(books):
    """Searches for a book by title or ID."""
    print("\n--- SEARCH BOOK ---")
    query = input("Enter Book ID or Title to search: ").strip().lower()

    found = False
    for book_id, info in books.items():
        if query == book_id.lower() or query in info["title"].lower():
            status = f"Issued to {info['issued_to']}" if info['issued_to'] else "Available"
            print(f"\nFound -> ID: {book_id} | Title: {info['title']} | Author: {info['author']} | Status: {status}")
            found = True

    if not found:
        print("No matching book found.")

def main():
    books = load_data()

   import streamlit as st

st.title("AKTU Library Management System")

# Create a web-based menu selection
menu = st.sidebar.selectbox(
    "Select an Option",
    ["Display All Books", "Add New Book", "Issue Book", "Return Book", "Search Book"]
)

        # 1. Create the web sidebar dropdown menu
choice = st.sidebar.selectbox(
    "Select an Option",
    ["Display All Books", "Add New Book", "Issue Book", "Return Book", "Search Book"]
)

# 2. Map your existing functions to the web selections
if choice == "Display All Books":
    display_books(books)
    
elif choice == "Add New Book":
    add_book(books)
    
elif choice == "Issue Book":
    issue_book(books)
    
elif choice == "Return Book":
    return_book(books)
    
elif choice == "Search Book":
    search_book(books)


      
if __name__ == "__main__":
    main()




# Commented out IPython magic to ensure Python compatibility.
# %%writefile app.py
# import streamlit as st
# import json
# import os
# 
# DATA_FILE = "library_data.json"
# 
# default_books = {
#     "101": {"title": "Python Programming", "author": "E. Balagurusamy", "issued_to": None},
#     "102": {"title": "Data Structures", "author": "Seymour Lipschutz", "issued_to": None},
#     "103": {"title": "Computer Networks", "author": "Andrew S. Tanenbaum", "issued_to": None}
# }
# 
# def load_data():
#     if os.path.exists(DATA_FILE):
#         with open(DATA_FILE, "r") as file:
#             return json.load(file)
#     return default_books
# 
# def save_data(books):
#     with open(DATA_FILE, "w") as file:
#         json.dump(books, file, indent=4)
# 
# if 'books' not in st.session_state:
#     st.session_state.books = load_data()
# 
# books = st.session_state.books
# 
# st.set_page_config(page_title="AKTU Library Web App", page_icon="📚", layout="wide")
# st.title("📚 AKTU Library Management System")
# st.markdown("---")
# 
# menu = st.sidebar.selectbox(
#     "Navigation Menu",
#     ["Display Books", "Add New Book", "Issue Book", "Return Book", "Search Book"]
# )
# 
# if menu == "Display Books":
#     st.header("📋 Current Library Catalog")
#     if not books:
#         st.warning("No books in the database.")
#     else:
#         table_data = [
#             {
#                 "Book ID": k,
#                 "Title": v["title"],
#                 "Author": v["author"],
#                 "Status": f"Issued to {v['issued_to']}" if v["issued_to"] else "Available"
#             }
#             for k, v in books.items()
#         ]
#         st.table(table_data)
# 
# elif menu == "Add New Book":
#     st.header("➕ Add a New Book")
#     with st.form("add_book"):
#         b_id = st.text_input("Book ID")
#         title = st.text_input("Title")
#         author = st.text_input("Author")
#         if st.form_submit_button("Add"):
#             if b_id in books:
#                 st.error("Book ID already exists!")
#             elif b_id and title and author:
#                 books[b_id] = {"title": title, "author": author, "issued_to": None}
#                 save_data(books)
#                 st.success(f"Added {title} successfully!")
#             else:
#                 st.error("Please fill all fields.")
# 
# elif menu == "Issue Book":
#     st.header("📖 Issue a Book")
#     avail = {k: v for k, v in books.items() if v["issued_to"] is None}
#     if not avail:
#         st.info("No books available to issue.")
#     else:
#         options = [f"{k} - {v['title']}" for k, v in avail.items()]
#         selected = st.selectbox("Select Book", options)
#         student = st.text_input("Student Name / Roll No.")
#         if st.button("Issue"):
#             if student.strip():
#                 book_id = selected.split(" - ")[0]
#                 books[book_id]["issued_to"] = student
#                 save_data(books)
#                 st.success("Book issued successfully!")
#                 st.rerun()
# 
# elif menu == "Return Book":
#     st.header("🔄 Return Book")
#     issued = {k: v for k, v in books.items() if v["issued_to"] is not None}
#     if not issued:
#         st.info("No books currently issued.")
#     else:
#         options = [f"{k} - {v['title']} ({v['issued_to']})" for k, v in issued.items()]
#         selected = st.selectbox("Select Book to Return", options)
#         if st.button("Return"):
#             book_id = selected.split(" - ")[0]
#             books[book_id]["issued_to"] = None
#             save_data(books)
#             st.success("Book returned successfully!")
#             st.rerun()
# 
# elif menu == "Search Book":
#     st.header("🔍 Search Book")
#     query = st.text_input("Search by ID or Title").strip().lower()
#     if query:
#         results = [
#             {
#                 "Book ID": k,
#                 "Title": v["title"],
#                 "Author": v["author"],
#                 "Status": f"Issued to {v['issued_to']}" if v["issued_to"] else "Available"
#             }
#             for k, v in books.items()
#             if query == k.lower() or query in v["title"].lower()
#         ]
#         if results:
#             st.table(results)
#         else:
#             st.warning("No matching books found.")





# Start Streamlit background process
os.system("streamlit run app.py &")
