#!/usr/bin/env python3.8

from __future__ import annotations

from functools import partial
from time import time
from typing import List, NamedTuple, Set, Tuple, Dict

BookID = int
LibraryID = int
Solution = List[Tuple[LibraryID, List[BookID]]]

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
        return self.time_to_fully_scan() + self.signup
     
    def library_books_value(self, modified_book_value: List[int]) -> int:
        value = 0
        for i in self.books:
            value += modified_book_value[i]
        return value
       
    def value_per_day(self,modified_book_value):
        self.library_books_value(modified_book_value)/self.total_process_time()
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


def heuristic_signup(days_left: int, library: Library) -> int:
    # heuristics: smaller is better
    return library.signup

HEURISTIC = heuristic_signup
def optimal_solution(problem: Problem) -> Solution:
    book_scores, days_available, libraries = problem
    current_day = 0
    solution = []
    while current_day < days_available and libraries:
        days_left = days_available - current_day
        # sort descending therefore optimal is at the end
        libraries.sort(reverse=True, key=partial(HEURISTIC, days_left))
        l = libraries.pop()
        solution.append((l.id, list(l.books)))
    return solution

def slightly_better_solution(problem: Problem) -> Solution:
    library_values_per_day = []
    occurances_per_book = []
    modified_book_values = []
    
    for i in range(len(problem.book_scores)):
        occurances_per_book.append(bookoccurances(i,problem.libraries))

    for i in range(len(problem.book_scores)):
        if occurances_per_book[i] != 0:
            modified_book_values.append(problem.book_scores[i]/occurances_per_book[i])
        else:
            modified_book_values.append(None)
            
            

    for i in problem.libraries:
        library_values_per_day.append((i.value_per_day(modified_book_values),i.id))
    library_values_per_day.sort(reverse = True)
    solution = []
    for i in library_values_per_day:
        solution.append((i[1],problem.libraries[i[1]].books))
    return solution
    
    
def questionable_solution(problem: Problem) -> Solution:
    #Because why not
    #This will not work on b
    library_dicti = {}
    solutions = []
    for i in problem.libraries:
        for j in i.books:
            if i in library_dicti:
                library_dicti[j].append(i)
            else:
                library_dicti[j] = [i]
    temp = sorted(library_dicti)
    for i in temp:
        for j in sorted(i.signup):
            solutions.append(i.id,i.books)
    return solutions
    


# def questionable_solution_2(problem:Problem) -> Solution:
#     library_dicti = {}
#     for i in problem.libraries:
#         if i.signup in library_dicti:
#             library_dicti[i.signup].append()
#         else:
#             library_dicti[i.signup] = [i]
    

def problem_b_specific_solution(problem: Problem) -> Solution:
    # Optimises because all books in B are unique. WILL NOT work for other
    # problems.
    solution = []
    for library in sorted(problem.libraries, key=lambda l: l.signup):
        solution.append((library.id, library.books))
        #print(library.id)

    return solution
    
def calculate_score(problem: Problem, solution: Solution) -> int:
    """Calculates an ESTIMATE of the score given a problem and solution. This is
    very naive, clearly has a bug somewhere because the scores are a little off,
    and is also really slow because it simulates day-by-day.
    """
    libraries_in_signup_order = [problem.libraries[library_id] for library_id, _ in solution]
    score = 0
    upcoming_books_for_libraries = []   #list of tuples of the library and the books it has left
    library_currently_signing_up = None #library in the process of signing up
    library_signup_days_remaining = None    #time left for remaining library

    for day in range(problem.days):
        for library, books in upcoming_books_for_libraries:
            for _ in range(library.shipping):
                if any(books):
                    book_id = books.pop(0)
                    score += problem.book_scores[book_id]

        if library_signup_days_remaining is not None:
            library_signup_days_remaining -= 1

        if library_signup_days_remaining == 0 or library_signup_days_remaining is None:
            if library_currently_signing_up is not None:
                upcoming_books_for_libraries.append(
                    (library_currently_signing_up, list(library_currently_signing_up.books))
                )

            if any(libraries_in_signup_order):
                library_currently_signing_up = libraries_in_signup_order.pop(0)
                library_signup_days_remaining = library_currently_signing_up.signup

    return score


PROBLEMS = [
    "a_example.txt",
    "b_read_on.txt",
    "c_incunabula.txt",
    "d_tough_choices.txt",
    "e_so_many_books.txt",
    "f_libraries_of_the_world.txt",
]


if __name__ == "__main__":
    filename = "c_incunabula.txt"
    f = loadfile(filename)
    books = f.book_scores
    days = f.days
    librarys = f.libraries

    #savefile("hacky_b", problem_b_specific_solution(loadfile("b_read_on.txt")))

    for the_filename in PROBLEMS:
        problem = loadfile(the_filename)
        letter = the_filename[0]
        start = time()
        solution = problem_b_specific_solution(problem)
        end = time()
        print(f"Solution for problem {letter} took {end-start} seconds")
        #print("Estimated score: ", calculate_score(problem, solution))
        savefile("problem_b_specific_solution_" + letter, solution)
 
    bookmod = []    # number of times the book occurs in total
    for i in range(len(books)):
        bookmod.append(bookoccurances(i,librarys))
    modified_book_values = [] # number of total occurances/number of occurences
    for i in range(len(books)):
        modified_book_values.append(books[i]/bookmod[i]) # calculate modified book value
    
    #print(f)
    
    #print(bookmod)
    #print(books)
    #print(modified_book_values)
