#!/usr/bin/env python3.8

from __future__ import annotations

from time import time
from typing import List, NamedTuple, Set, Tuple, Dict

BookID = int
LibraryID = int

class Library:
    bookqtt: int
    signup: int
    shipping: int
    books: Set[BookID]
    id: LibraryID

    def __init__(self, f, id):
        self.id = id
        
        line = f.readline().split()
        self.bookqtt = int(line[0]) # the number of books in this library
        self.signup = int(line[1]) # the number of days it takes to sign up this library
        self.shipping = int(line[2]) # the number of books that can be shipped per day
        
        self.books = set()
        line = f.readline().split()
        for i in line:
            self.books.add(int(i))

    def time_to_fully_scan(self):
        val = self.bookqtt//self.shipping
        if ((self.bookqtt%self.shipping) != 0):
            val +=1
        return val
        
    def total_process_time(self):
        return time_to_fully_scan() + self.signup
     
    def library_books_value(self, modified_book_value: List[int]) -> int:
        value = 0
        for i in self.books:
            value += modified_book_value[i]
        return value
       
    def value_per_day(self,modified_book_value):
        self.library_books_value/self.total_process_time
        pass
        

    def __repr__(self):
        return f"id: {self.id} books: {self.bookqtt} signup: {self.signup} shipping: {self.shipping} books: {self.books}"


class Problem(NamedTuple):
    book_scores: List[int]
    days: int
    libraries: List[Library]


def loadfile(filename) -> Tuple[List[int], int, List[Library]]:
    """Determines:
    - the scores of each book (and therefore implicitly how many books there are)
    - the number of days available
    - the libraries that exist
    """
    with open(filename, "r") as f:
        line = f.readline()
        line = line.split()
        books = int(line[0]) # the number of different books that exist
        libqtt = int(line[1]) # the number of different libraries that exist
        days = int(line[2]) # the number of days available

        bookscores: List[int] = [] # map of book ID to book score
        line = f.readline()
        line = line.split()
        for i in line:
            bookscores.append(int(i))

        librarys: List[Library] = []
        for i in range(libqtt):
            librarys.append(Library(f,i))

    return Problem(bookscores, days, librarys)

Solution = List[Tuple[LibraryID, List[BookID]]]

def savefile(filename: str, books_by_library: List[Tuple[LibraryID, List[BookID]]]):
    """Takes a list of tuples in the form (library ID, list of books sent by that
    library), in the order in which the libraries are signed up. Writes a
    submission file using this data to the given file path.

    For example, [(1, [4, 2, 0]), (0, [6, 9])] indicates that:
      - library ID 1 signs up first and sends 3 books: 4, 2, and 0
      - library ID 0 signs up second and sends 2 books: 6 and 9
    (nice)
    """
    with open(filename, "w") as f:
        # Write the number of libraries
        f.write(f"{len(books_by_library)}\n")
        
        for library, books in books_by_library:
            # Write the library ID and number of books
            f.write(f"{library} {len(books)}\n")

            # Write each book, separated by a space
            f.write(f"{' '.join(str(x) for x in books)}\n")

def bookoccurances(book: BookID, librarys: List[Library]) -> int:
    """Counts the number of libraries which have a particular book."""
    # iow: inversely proportional to book rarity
    # (note that rarity != score)
    val = 0
    for i in librarys:
        if book in i.books:
            val += 1
    return val

    # but this will change based on if the book has been documented already

# List[Tuple[LibraryID, List[BookID]]]
def shit_solution(problem: Problem) -> Solution:
    book_scores, days_available, libraries = problem
    current_day = 0
    solution = []
    for library in libraries:
        if current_day > days_available:
            print("ran out of days, exiting")
            break
        solution.append((library.id, list(library.books)))
        current_day += library.signup
    else:
        print("did not run out of days")
    return solution

def slightly_better_solution(problem: Problem) -> Solution:
    library_values_per_day = []
    for i in Problem.books:
        
    
    for i in Problem.libraries:
        library_values_per_day.append((i.value_per_day(),i.id))
    
    
    pass

def calculate_score(problem: Problem, solution: Solution) -> int:
    libraries_in_signup_order = [problem.libraries[library_id] for library_id, _ in solution]
    score = 0
    upcoming_books_for_libraries = []
    library_signup_in_progress = None
    library_signup_days_remaining = 0

    for day in range(problem.days):
        for library, books in upcoming_books_for_libraries:
            for _ in range(library.shipping):
                if any(books):
                    book_id = books.pop(0)
                    score += solution.book_scores[book_id]

        if library_signup_days_remaining == 0:
            if library_signup_in_progress is not None:
                upcoming_books_for_libraries.append(
                    (library_signup_in_progress, library.books[:])
                )

            library_signup_in_progress = libraries_in_signup_order.pop(0)
            library_signup_days_remaining = library_signup_in_progress.signup


PROBLEMS = {
    "a_example.txt",
    "b_read_on.txt",
    "c_incunabula.txt",
    "d_tough_choices.txt",
    "e_so_many_books.txt",
    "f_libraries_of_the_world.txt",
}


if __name__ == "__main__":
    filename = "c_incunabula.txt"
    f = loadfile(filename)
    books = f.book_scores
    days = f.days
    librarys = f.libraries

    for the_filename in PROBLEMS:
        problem = loadfile(the_filename)
        start = time()
        solution = shit_solution(problem)
        end = time()
        print(f"Solution for problem {}")
        print("Estimated score: ", calculate_score(solution))
        savefile("shit_solution_" + letter, solution)
 
    bookmod = []    # number of times the book occurs in total
    for i in range(len(books)):
        bookmod.append(bookoccurances(i,librarys))
    modified_book_values = [] # number of total occurances/number of occurences
    for i in range(len(books)):
        modified_book_values.append(books[i]/bookmod[i]) # calculate modified book value
    
    #print(f)
    
    #print(bookmod)
    #print(books)
    print(modified_book_values)
