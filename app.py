import streamlit as st
import json
from typing import List, Dict

# Set page config (must be the first Streamlit command)
st.set_page_config(page_title="Personal Library Manager", page_icon="📚", layout="wide")

# File to store library data
LIBRARY_FILE = "library.json"

# Custom CSS for styling
st.markdown(
    """
    <style>
    .stButton button {
        background-color: ##04022D;
        color: white;
        border-radius: 5px;
        padding: 10px 20px;
        font-size: 16px;
    }
    .stButton button:hover {
        background-color: #45a049;
    }
    .stTextInput input {
        border-radius: 5px;
        padding: 10px;
    }
    .stNumberInput input {
        border-radius: 5px;
        padding: 10px;
    }
    .stCheckbox label {
        font-size: 16px;
    }
    .stRadio label {
        font-size: 16px;
    }
    .stMarkdown h1, h2, h3 {
        color: #4CAF50;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Load the library from a file
def load_library() -> List[Dict]:
    """Load the library from a file."""
    try:
        with open(LIBRARY_FILE, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

# Save the library to a file
def save_library(library: List[Dict]) -> None:
    """Save the library to a file."""
    with open(LIBRARY_FILE, "w") as file:
        json.dump(library, file, indent=4)

# Add a new book
def add_book(library: List[Dict]) -> None:
    """Add a new book to the library."""
    st.subheader("📖 Add a Book")
    with st.form("add_book_form"):
        col1, col2 = st.columns(2)
        with col1:
            title = st.text_input("Title", placeholder="Enter the book title")
            author = st.text_input("Author", placeholder="Enter the author name")
        with col2:
            year = st.number_input("Publication Year", min_value=0, max_value=9999, step=1)
            genre = st.text_input("Genre", placeholder="Enter the genre")
        read_status = st.checkbox("Have you read this book?")
        
        if st.form_submit_button("Add Book"):
            if title and author and genre:
                library.append({
                    "Title": title,
                    "Author": author,
                    "Year": int(year),
                    "Genre": genre,
                    "Read": read_status
                })
                save_library(library)
                st.success("✅ Book added successfully!")
            else:
                st.error("❌ Please fill in all fields.")

# Remove a book
def remove_book(library: List[Dict]) -> None:
    """Remove a book from the library by title."""
    st.subheader("🗑️ Remove a Book")
    title = st.text_input("Enter the title of the book to remove", placeholder="Enter the book title")
    
    if st.button("Remove Book"):
        for book in library:
            if book["Title"].lower() == title.lower():
                library.remove(book)
                save_library(library)
                st.success("✅ Book removed successfully!")
                return
        st.error("❌ Book not found.")

# Edit a book
def edit_book(library: List[Dict]) -> None:
    """Edit an existing book's details."""
    st.subheader("✏️ Edit a Book")
    title = st.text_input("Enter the title of the book to edit", placeholder="Enter the book title")
    
    if st.button("Search"):
        for book in library:
            if book["Title"].lower() == title.lower():
                st.write("Editing book:", book)
                with st.form("edit_book_form"):
                    col1, col2 = st.columns(2)
                    with col1:
                        book["Title"] = st.text_input("Title", value=book["Title"])
                        book["Author"] = st.text_input("Author", value=book["Author"])
                    with col2:
                        book["Year"] = st.number_input("Publication Year", value=book["Year"])
                        book["Genre"] = st.text_input("Genre", value=book["Genre"])
                    book["Read"] = st.checkbox("Have you read this book?", value=book["Read"])
                    
                    if st.form_submit_button("Save Changes"):
                        save_library(library)
                        st.success("✅ Book updated successfully!")
                return
        st.error("❌ Book not found.")

# Search for a book
def search_book(library: List[Dict]) -> None:
    """Search for a book by title or author."""
    st.subheader("🔍 Search for a Book")
    search_by = st.radio("Search by", ["Title", "Author"])
    query = st.text_input(f"Enter the {search_by.lower()} to search for", placeholder=f"Enter the {search_by.lower()}")
    
    if st.button("Search"):
        results = [book for book in library if query.lower() in book[search_by].lower()]
        if results:
            st.write("📚 Matching Books:")
            for i, book in enumerate(results, 1):
                status = "✅ Read" if book["Read"] else "❌ Unread"
                st.write(f"{i}. **{book['Title']}** by {book['Author']} ({book['Year']}) - {book['Genre']} - {status}")
        else:
            st.error("❌ No matching books found.")

# Display all books
def display_books(library: List[Dict]) -> None:
    """Display all books in the library."""
    st.subheader("📚 Your Library")
    if not library:
        st.warning("Your library is empty.")
    else:
        for i, book in enumerate(library, 1):
            status = "✅ Read" if book["Read"] else "❌ Unread"
            st.write(f"{i}. **{book['Title']}** by {book['Author']} ({book['Year']}) - {book['Genre']} - {status}")

# Display statistics
def display_statistics(library: List[Dict]) -> None:
    """Display statistics about the library."""
    st.subheader("📊 Library Statistics")
    total_books = len(library)
    read_books = sum(1 for book in library if book["Read"])
    percentage_read = (read_books / total_books * 100) if total_books > 0 else 0
    
    st.metric("Total Books", total_books)
    st.metric("Percentage Read", f"{percentage_read:.2f}%")

# Main function
def main():
    """Main function to run the Streamlit app."""
    st.title("📚 Personal Library Manager")
    
    # Load the library
    library = load_library()
    
    # Sidebar menu
    st.sidebar.title("Menu")
    menu = st.sidebar.radio(
        "Choose an option",
        ["Add a Book", "Remove a Book", "Edit a Book", "Search for a Book", "Display All Books", "Display Statistics"]
    )
    
    # Handle menu selection
    if menu == "Add a Book":
        add_book(library)
    elif menu == "Remove a Book":
        remove_book(library)
    elif menu == "Edit a Book":
        edit_book(library)
    elif menu == "Search for a Book":
        search_book(library)
    elif menu == "Display All Books":
        display_books(library)
    elif menu == "Display Statistics":
        display_statistics(library)

# Run the app
if __name__ == "__main__":
    main()
