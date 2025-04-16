import json
from typing import List, Dict
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt
from rich.panel import Panel
from rich.text import Text

# File to store library data
LIBRARY_FILE = "library.txt"

# Initialize Rich console
console = Console()

def load_library() -> List[Dict]:
    """Load the library from a file."""
    try:
        with open(LIBRARY_FILE, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_library(library: List[Dict]) -> None:
    """Save the library to a file."""
    with open(LIBRARY_FILE, "w") as file:
        json.dump(library, file, indent=4)

def get_valid_input(prompt: str, input_type=str) -> any:
    """Helper function to get valid user input."""
    while True:
        try:
            user_input = Prompt.ask(prompt)
            return input_type(user_input)
        except ValueError:
            console.print(f"[red]Invalid input. Please enter a valid {input_type.__name__}.[/red]")

def add_book(library: List[Dict]) -> None:
    """Add a new book to the library."""
    title = get_valid_input("Enter the book title: ")
    author = get_valid_input("Enter the author: ")
    year = get_valid_input("Enter the publication year: ", int)
    genre = get_valid_input("Enter the genre: ")
    read_status = get_valid_input("Have you read this book? (yes/no): ").strip().lower() == "yes"
    
    library.append({
        "Title": title,
        "Author": author,
        "Year": year,
        "Genre": genre,
        "Read": read_status
    })
    console.print("[green]Book added successfully![/green]")

def remove_book(library: List[Dict]) -> None:
    """Remove a book from the library by title."""
    title = Prompt.ask("Enter the title of the book to remove")
    for book in library:
        if book["Title"].lower() == title.lower():
            library.remove(book)
            console.print("[green]Book removed successfully![/green]")
            return
    console.print("[red]Book not found.[/red]")

def edit_book(library: List[Dict]) -> None:
    """Edit an existing book's details."""
    title = Prompt.ask("Enter the title of the book to edit")
    for book in library:
        if book["Title"].lower() == title.lower():
            console.print(Panel.fit(f"Editing book: [bold]{book['Title']}[/bold]"))
            book["Title"] = get_valid_input(f"Enter new title ({book['Title']}): ") or book["Title"]
            book["Author"] = get_valid_input(f"Enter new author ({book['Author']}): ") or book["Author"]
            book["Year"] = get_valid_input(f"Enter new publication year ({book['Year']}): ", int) or book["Year"]
            book["Genre"] = get_valid_input(f"Enter new genre ({book['Genre']}): ") or book["Genre"]
            book["Read"] = get_valid_input(f"Have you read this book? (yes/no) ({'Read' if book['Read'] else 'Unread'}): ").strip().lower() == "yes"
            console.print("[green]Book updated successfully![/green]")
            return
    console.print("[red]Book not found.[/red]")

def search_book(library: List[Dict]) -> None:
    """Search for a book by title or author."""
    choice = Prompt.ask("Search by:\n1. Title\n2. Author\nEnter your choice", choices=["1", "2"])
    query = Prompt.ask("Enter the search term").strip().lower()
    
    results = [book for book in library if query in book["Title"].lower() or query in book["Author"].lower()]
    
    if results:
        table = Table(title="Matching Books", show_header=True, header_style="bold magenta")
        table.add_column("No.", style="dim", width=4)
        table.add_column("Title")
        table.add_column("Author")
        table.add_column("Year")
        table.add_column("Genre")
        table.add_column("Status")
        
        for i, book in enumerate(results, 1):
            status = "Read" if book["Read"] else "Unread"
            table.add_row(str(i), book["Title"], book["Author"], str(book["Year"]), book["Genre"], status)
        
        console.print(table)
    else:
        console.print("[red]No matching books found.[/red]")

def display_books(library: List[Dict], sort_by: str = None) -> None:
    """Display all books in the library, optionally sorted."""
    if not library:
        console.print("[yellow]Your library is empty.[/yellow]")
        return

    if sort_by:
        library = sorted(library, key=lambda x: x[sort_by])

    table = Table(title="Your Library", show_header=True, header_style="bold magenta")
    table.add_column("No.", style="dim", width=4)
    table.add_column("Title")
    table.add_column("Author")
    table.add_column("Year")
    table.add_column("Genre")
    table.add_column("Status")
    
    for i, book in enumerate(library, 1):
        status = "Read" if book["Read"] else "Unread"
        table.add_row(str(i), book["Title"], book["Author"], str(book["Year"]), book["Genre"], status)
    
    console.print(table)

def display_statistics(library: List[Dict]) -> None:
    """Display statistics about the library."""
    total_books = len(library)
    read_books = sum(1 for book in library if book["Read"])
    percentage_read = (read_books / total_books * 100) if total_books > 0 else 0
    
    console.print(Panel.fit(
        f"[bold]Total books:[/bold] {total_books}\n"
        f"[bold]Percentage read:[/bold] {percentage_read:.2f}%",
        title="Library Statistics"
    ))

def main():
    """Main function to run the menu system."""
    library = load_library()
    
    while True:
        console.print(Panel.fit(
            "[bold]Welcome to your Personal Library Manager![/bold]",
            subtitle="Choose an option below"
        ))
        console.print("1. Add a book")
        console.print("2. Remove a book")
        console.print("3. Edit a book")
        console.print("4. Search for a book")
        console.print("5. Display all books")
        console.print("6. Display statistics")
        console.print("7. Sort books")
        console.print("8. Exit")
        
        choice = Prompt.ask("Enter your choice", choices=["1", "2", "3", "4", "5", "6", "7", "8"])
        
        if choice == "1":
            add_book(library)
        elif choice == "2":
            remove_book(library)
        elif choice == "3":
            edit_book(library)
        elif choice == "4":
            search_book(library)
        elif choice == "5":
            display_books(library)
        elif choice == "6":
            display_statistics(library)
        elif choice == "7":
            sort_by = Prompt.ask("Sort by (Title/Author/Year/Genre)", choices=["Title", "Author", "Year", "Genre"])
            display_books(library, sort_by)
        elif choice == "8":
            save_library(library)
            console.print("[green]Library saved to file. Goodbye![/green]")
            break

if __name__ == "__main__":
    main()
