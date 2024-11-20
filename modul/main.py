import csv
import matplotlib.pyplot as plt


class Book:


    def __init__(self, title, author, year, genre, quantity):
        self.title = title
        self.author = author
        self.year = year
        self.genre = genre
        self.quantity = quantity


    def update_info(self, title = None, author = None, year = None, genre = None, quantity = None):
        if title:
            self.title = title

        if author:
            self.author = author

        if year:
            self.year = year

        if genre:
            self.genre = genre

        if quantity is not None:
            self.quantity = quantity


    def __str__(self):
        return f"{self.title}, {self.author}, {self.year}, {self.genre}, {self.quantity}"


class Library:


    def __init__(self, file_name):
        self.file_name = file_name
        self.books = self.load_books()


    # load books from file
    def load_books(self):
        books = []

        try:
            # Check if the file exists and if it is in the correct format
            with open(self.file_name, mode='r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                
                if reader.fieldnames != ['Title', 'Author', 'Year', 'Genre', 'Quantity']:
                    print(f"Warning: CSV columns are not matching expected columns. Found: {reader.fieldnames}")
                
                for row in reader:
                    print(f"Reading row: {row}")  
                    book = Book(row['Title'], row['Author'], int(row['Year']), row['Genre'], int(row['Quantity']))
                    books.append(book)

        except FileNotFoundError:
            print("File not found, creating a new library!")

        except Exception as e:
            print(f"Error while loading books: {e}!")

        return books


    # save current list of books to file
    def save_books(self):
        try:
            with open(self.file_name, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=['Title', 'Author', 'Year', 'Genre', 'Quantity'])
                writer.writeheader()

                for book in self.books:
                    writer.writerow({'Title': book.title, 'Author': book.author, 'Year': book.year, 'Genre': book.genre, 'Quantity': book.quantity})

        except Exception as e:
            print(f"Error while saving books: {e}!")


    # add new book to librory and save it to file
    def add_book(self, book):
        try:
            self.books.append(book)
            self.save_books()

        except Exception as e:
            print(f"Error while adding book: {e}!")


    # edit the book info by title
    def edit_book(self, title, **temp):
        try:
            for book in self.books:

                if book.title == title:
                    book.update_info(**temp)
                    self.save_books()
                    return
                
            print(f"Book with title '{title}' not found.")

        except Exception as e:
            print(f"Error while editing book: {e}")


    # delete book from librory by title
    def delete_book(self, title):
        try:
            for book in self.books:

                if book.title == title:
                    self.books.remove(book)
                    self.save_books()
                    return
                
            print(f"Book with title '{title}' not found!")

        except Exception as e:
            print(f"Error while deleting book: {e}")


    # display list of books
    def list_books(self):
        if not self.books:
            print("No books available!")

        else:
            for book in self.books:
                print(book)


    # total count of books in file
    def total_books(self):
        return sum(book.quantity for book in self.books)


    # get popular genres based on frequency in the library.
    def most_popular_genres(self):
        genre_count = {}

        for book in self.books:
            if book.genre in genre_count:
                genre_count[book.genre] += 1

            else:
                genre_count[book.genre] = 1

        return sorted(genre_count.items(), key=lambda x: x[1], reverse=True)


    # searche books by author or publication year.
    def find_books_by_author_or_year(self, author=None, year=None):
        try:
            result = []

            for book in self.books:
                if (author and book.author == author) or (year and book.year == year):
                    result.append(book)

            return result
        
        except Exception as e:
            print(f"Error during search: {e}")

            return []


    # show distribution of books by genre
    def plot_genres(self):
        try:
            genre_count = {}

            for book in self.books:
                if book.genre in genre_count:
                    genre_count[book.genre] += book.quantity

                else:
                    genre_count[book.genre] = book.quantity

            plt.pie(genre_count.values(), labels=genre_count.keys(), autopct='%1.1f%%')
            plt.title('Books Distribution by Genre')
            plt.show()

        except Exception as e:
            print(f"Error while plotting genres: {e}")


    # show distribution of books by publication year.
    def plot_books_by_year(self):
        try:
            year_count = {}

            for book in self.books:

                try:
                    year = int(book.year)  

                except ValueError:
                    print(f"Invalid year for book: {book.title}, skipping...")
                    continue

                if year < 1000 or year > 2024:
                    print(f"Skipping unreasonable year: {year} for book: {book.title}")
                    continue

                if year in year_count:
                    year_count[year] += book.quantity
                    
                else:
                    year_count[year] = book.quantity

            print("Year count:", year_count)

            sorted_years = sorted(year_count.keys())

            plt.bar(sorted_years, [year_count[year] for year in sorted_years])
            plt.title('Books Distribution by Year')
            plt.xlabel('Year')
            plt.ylabel('Number of Books')
            plt.show()

        except Exception as e:
            print(f"Error while plotting books by year: {e}")



def main_menu():
    library = Library("modul/books.csv")

    while True:
        print("\nMenu:")
        print("1. Add a new book")
        print("2. Edit book information")
        print("3. Delete a book")
        print("4. View all books")
        print("5. Total number of books")
        print("6. Most popular genres")
        print("7. Search books by author or year")
        print("8. Plot books distribution by genre")
        print("9. Plot books distribution by year")
        print("0. Exit")
        choice = input("Select an option: ")

        try:

            if choice == "1":

                title = input("Enter the title of the book: ")
                author = input("Enter the author: ")
                year = int(input("Enter the year of publication: "))
                genre = input("Enter the genre: ")
                quantity = int(input("Enter the quantity: "))

                new_book = Book(title, author, year, genre, quantity)
                library.add_book(new_book)
                print("Book added!")


            elif choice == "2":

                title = input("Enter the title of the book to edit: ")
                print("Select what to update: ")

                new_title = input("New title (leave blank if not changing): ")
                new_author = input("New author (leave blank if not changing): ")
                new_year = input("New year of publication (leave blank if not changing): ")
                new_genre = input("New genre (leave blank if not changing): ")
                new_quantity = input("New quantity (leave blank if not changing): ")

                temp = {}

                if new_title: 
                    temp['title'] = new_title

                if new_author: 
                    temp['author'] = new_author

                if new_year: 
                    temp['year'] = int(new_year)

                if new_genre: 
                    temp['genre'] = new_genre

                if new_quantity: 
                    temp['quantity'] = int(new_quantity)


                library.edit_book(title, **temp)
                print("Information updated!")


            elif choice == "3":
                title = input("Enter the title of the book to delete: ")
                library.delete_book(title)
                print("Book deleted!")


            elif choice == "4":
                library.list_books()


            elif choice == "5":
                print(f"Total number of books: {library.total_books()}")


            elif choice == "6":
                print("Most popular genres:")

                for genre, count in library.most_popular_genres():
                    print(f"{genre}: {count} books")


            elif choice == "7":
                author = input("Enter author to search (or leave blank): ")
                year = input("Enter year of publication to search (or leave blank): ")
                year = int(year) if year else None

                books_found = library.find_books_by_author_or_year(author, year)
                print(f"Found {len(books_found)} books:")

                for book in books_found:
                    print(book)


            elif choice == "8":
                library.plot_genres()


            elif choice == "9":
                library.plot_books_by_year()


            elif choice == "0":
                print("Exiting...")
                break


            else:
                print("Invalid choice, try again!")


        except ValueError:
            print("Invalid input! Please enter valid numbers where required!")


        except Exception as e:
            print(f"An unexpected error occurred: {e}!")



if __name__ == "__main__":
    main_menu()