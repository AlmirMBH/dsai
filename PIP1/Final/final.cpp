// Command to run the code: g++ main.cpp && ./a.out
#include <iostream>
#include <map>
#include <vector>
#include <string>

// Compiler 11: echo 'alias g++="g++ -std=c++11"' >> ~/.zshrc && source ~/.zshrc

template <typename T, std::size_t N>
std::size_t arrayLength(const T (&)[N]) {
    return N;
}

// Deduce the output
// int main() {
//     int x = 10;
//     int y = 20;
//     int* ptr = &x;
//     int& ref = y;
//     *ptr = 30;
//     ref = 40;
//     std::cout << "x: " << x << ", y: " << y << std::endl; // 30, 40

//     auto a = 5; // compulier deduces the type 
//     auto b = 3.14;
//     auto c = a + b; // int c = a + b; // 8
//     std::cout << "a: " << a << ", b: " << b << ", c: " << c << std::endl; // 5, 3.14, 8.14

//  return 0;
// }


// what is the output
// void updateValues(int num, int& ref) {
//     num = num + 5;
//     ref = ref + 5;
// }

// int main() {
//     int a = 10, b = 20;
//     updateValues(a, b);
//     std::cout << "a: " << a << ", b: " << b << std::endl; // 10 25
//     return 0;
// }

// Predict the output
// void fn(int* x, int y) {
//     for (int i = 0; i < y; i++) {
//         x[i] = x[i] + 1;
//     }
// }

// int main() {
//     int arr[3] = {1, 2, 3}; // 2, 4, 
//     fn(arr, 3);
//     std::cout << "arr[0]: " << arr[0] << ", arr[1]: " << arr[1] << ", arr[2]: " << arr[2] << std::endl;
//     return 0;
// }

// Write C++ function that calculates the sum and the product of all digits in a number.
// int main(){
//     double sum = 0;
//     int digit;
//     int number = 4234;

//     while(number > 0){
//         digit = number % 10;
//         sum = sum + digit;
//         number /= 10;
//     }

//     std::cout << "Sum: " << sum << std::endl;
//     return 0;
// }

// Write C++ function most_frequent_digit(start, end) that returns the most frequent digit across all numbers in the range [start, end]. 
// int most_frequent_digit(int start, int end) {
//     std::vector<int> range;
//     int index = 0;

//     int most_frequent = 0;
//     for (int i = start; i < end; i++) { // 100, 101, 102,..., 199
//         range.push_back(i);
//     }

//     int number_of_elements = 0;
//     std::vector<int> individual_numbers;
//     for(int num : range) {
//         while (num > 0) {
//             number_of_elements++;
//             int digit = num % 10;
//             num = num/10;
//             individual_numbers.push_back(digit);
//         }
//     }

    
//     std::map<int, int> myMap;
//     for (int number : individual_numbers){
//         myMap[number]++;
//     }

//     int temp = 0;
//     for (const auto& pair : myMap) {
//         std::cout << pair.first << ": " << pair.second << std::endl;
        
//         if (pair.second > temp) {
//             temp = pair.second;
//             most_frequent = pair.first;
//         }
//     }

//     return most_frequent;
// }

// int main() {
//     std::cout << most_frequent_digit(100, 200) << std::endl;
//     return 0;
// }

// Write C++ function that asks the user to enter a string and replaces all occurrences of a specific character
// (given by the user) with another character.
// int main () {
//     std::string string;
//     std::string letter_to_replace;
//     std::string new_letter;
//     std::cout << "Enter a string" << std::endl;
//     std::cin >> string;
//     std::cout << "Enter a letter to replace" << std::endl;
//     std::cin >> letter_to_replace;
//     std::cout << "Enter a new letter" << std::endl;
//     std::cin >> new_letter;
//     for (char &letter : string) {
//         if (letter == letter_to_replace[0]) {
//             letter = new_letter[0];
//         }
//     }
//     std::cout << string << std::endl;
//     return 0;
// }

// Write C++ function that asks the user to enter a string and checks in the string is a palindrome.
// int main() {
//     std::string str;
//     std::cout << "Enter a word to check if it is a palindrome"<< std::endl;
//     std::cin >> str;
    
//     // the equal compares strings from boths sides all the way to the mid-character
//     // equal(firstCharacter, middleCharacter, lastCharecter)
//     if (std::equal(str.begin(), str.begin() + str.size() / 2, str.rbegin()))
//         std::cout << "The word is a palindrome" << std::endl;
//     else
//         std::cout << "The word is not a palindrome" << std::endl;

//     return 0;
// }

// Write C++ function that asks the user to enter a sentence and returns the number of words in the sentence.
// int  main(){
//     std::string sentence;
//     std::cout << "Enter your sentence" << std::endl;
//     std::getline(std::cin, sentence); 
//     int number_of_words = 1;
//     for (char letter : sentence) {
//         if (letter == ' '){
//             number_of_words++;
//         }
//     }
//     std::cout << "Words" << number_of_words << std::endl;
//     return 0;
// }

// Write C++ function that asks the user to enter a sentence, a word to find and a replacement word. The
// function then replaces all occurrences of the word with the replacement in the sentence and prints it.
// int main() {
//     std::string sentence;
//     std::string replace;
//     std::string insert;

//     std::cout << "Enter a sentence" << std::endl;
//     std::getline(std::cin, sentence);

//     std::cout << "Enter a word to replace" << std::endl;
//     std::cin >> replace;

//     std::cout << "Enter a word to insert" << std::endl;
//     std::cin >> insert;
    
//     std::string word;
//     std::string final_string;

//     for (char letter : sentence) {
//         if(letter != ' ') {
//             word.push_back(letter);
//         } else {
//             if (word == replace) {
//                 final_string += insert;
//             } else {
//                 final_string += word;
//             }
//             final_string.push_back(' ');
//             word.clear();
//         }
//     }

//     if (!word.empty()) {
//         if (word == replace) {
//             final_string += insert;
//         } else {
//             final_string += word;
//         }
//     }

//     std::cout << "Final: "<< final_string << std::endl;

//     return 0;
// }

// Write C++ program that finds matching prime numbers between two matrices.
// A matching prime number is a prime number that is located in the same position in both matrices and has same value.
// Steps needed to solve this problem:
// a) Declare a 10x10 integer matrix A and B, and ask the user to enter it. Use std::vector.
// b) Write a function bool isPrime(int n); that checks whether a number passed as argument is prime or not.
// c) In main(), count the sum of matching primes between two matrices (call this value ResA).
// d) Find the number of even digits in ResA.
// bool isPrime(int n) {
//     if (n <= 1) return false;
//     for (int i = 2; i* i <= n; ++i) {
//         if (n % i == 0) return false;
//     }

//     return true;
// }

// int primeSum(const std::vector<int> primes) {
//     int ResA = 0;
//     for (int prime : primes) {
//         ResA = ResA + prime;
//     }

//     return ResA;
// }

// int evenDigits(int prime) {
//     if (prime % 2 == 0)
//         return prime;
//     else return 0;
// }



// int main() {
//     std::vector<std::vector<int>> first_matrix(3, std::vector<int>(3));
//     std::vector<std::vector<int>> second_matrix(3, std::vector<int>(3));

//     std::cout << "Enter the elements of the first matrix" << std::endl;
//     for (int i = 0; i < 3; i++) {
//         for (int j = 0; j < 3; j++) {
//             std::cin >> first_matrix[i][j];
//         }
//     }

//     std::cout << "Enter the elements of the second matrix" << std::endl;
//     for (int i = 0; i < 3; i++) {
//         for (int j = 0; j < 3; j++) {
//             std::cin >> second_matrix[i][j];
//         }
//     }

//     std::vector<int> prime_numbers;
//     for (int i = 0; i < 3; i++) {
//         for (int j = 0; j < 3; j++) {
//             if (first_matrix[i][j] == second_matrix[i][j] && isPrime(first_matrix[i][j])) {
//                 prime_numbers.push_back(first_matrix[i][j]);
//             }
//         }
//     }

//     std::cout << "Prime numbers that are at the same position in both matrices:" << std::endl;
//     for (int prime : prime_numbers) {
//         std::cout << prime << ", ";
//     }

//     std::cout << "Sum of primes" << std::endl;
//     std::cout << primeSum(prime_numbers)<< std::endl;

//     std::cout << "Even digits in primes" << std::endl;
//     for (int prime : prime_numbers) {
//         if (evenDigits(prime) != 0) {
//             std::cout << evenDigits(prime) << ", ";
//         }
//     }
// }

// ===================================
//                 SQL
// ===================================
//  Create a database containing two tables described below:
// 1. Books
// • book_id (Primary Key, Integer)
// • title (Text)
// • author (Text)
// • published_year (Integer)
// • available_copies (Integer)
// 2. Borrowers
// • borrower_id (Primary Key, Integer)
// • name (Text)
// • email (Text)
// • borrowed_book_id (Foreign Key referencing Books.book_id)
// create schema Library;
// create table Books(book_id INT PRIMARY KEY, title TEXT, author TEXT, published_year INT, available_copies INT)
// create table Borrowers(borrower_id INT PRIMARY KEY, name TEXT, email TEXT, borrowed_book_id INT, FOREIGN KEY (borrowed_book_id) REFERENCES Books(book_id))

//  Write following SQL statements:
// 1. Insert 5 books into the Books table.
// 2. Insert 3 borrowers into the Borrowers table, linking each borrower to a borrowed book.
// 3. Display all books borrowed by a specific borrower.
// 4. Update the available_copies of a book after a borrower returns it.
// 5. Retrieve the emails of borrowers who have borrowed books published after 2010.
// INSERT INTO Books (book_id, title, author, published_year, available_copies) 
// VALUES
// (1, "Book 1", "Author 1", 2000, 100),
// (2, "Book 2", "Author 2", 2001, 200),
// (3, "Book 3", "Author 3", 2002, 300),
// (4, "Book 4", "Author 4", 2003, 400),
// (5, "Book 5", "Author 5", 2004, 500);
// INSERT INTO Borrowers (borrower_id, name, email, borrowed_book_id) VALUES
// (1, "Name 1", "email1", 1),
// (2, "Name 2", "email2", 2),
// (3, "Name 3", "email3", 3),
// (4, "Name 4", "email4", 4),
// (5, "Name 5", "email5", 5);
// Select * from Borrowers br JOIN Books b on br.borrowed_book_id = b.book_id WHERE br.borrower_id = 1;
// UPDATE Books SET available_copies=available_copies + 1 WHERE book_id = 1 
// SELECT email from Borrowers br JOIN Books b ONnbr.borrowed_book_id = b.book_id WHERE b.published_year > 2003;

//  Create a database containing two tables described below:
// 1. Employees
// • employee_id (Primary Key, Integer)
// • first_name (Text)
// • last_name (Text)
// • email (Text)
// • department_id (Foreign Key referencing Departments.department_id)
// 2. Departments
// • department_id (Primary Key, Integer)
// • department_name (Text)
// • location (Text)
// CREATE TABLE Departments (department_id INT PRIMARY KEY, department_name TEXT, location TEXT);
// create table Employees(employee_id INT PRIMARY KEY, first_name TEXT, last_name TEXT, email TEXT, department_id INT, FOREIGN KEY (department_id) REFERENCES Departments(department_id));

// Write following SQL statements:
// 1. Insert 5 employees with different names and emails.
// 2. Insert 3 departments into the Departments table.
// 3. Assign each employee to a department.
// 4. Display all employees in a specific department.
// 5. Update the department of an employee of your choosing.
// 6. Retrieve the emails of employees working in the "IT" department.

// INSERT INTO Departments (department_id, department_name, location) VALUES 
// (1, "FINANCES", "Sarajevo"),
// (2, "IT", "TUZLA"),
// (3, "HR", "ZENICA");
// INSERT INTO Employees (employee_id, first_name, last_name, email, department_id) VALUES
// (1, "Paja", "Patak", "pp@gmail.com", 1),
// (2, "Djed", "Mraz", "dm@gmail.com", 2),
// (3, "Kim", "Jong", "kj@gmail.com", 3),
// (4, "Lepa", "Brena", "lb@hmail.com", 1),
// (5, "Ekrem", "Jevric", "ej@hmail.com", 2);
// SELECT * FROM Employees where department_id = 2;
// UPDATE Employees SET department_id = 2 WHERE employee_id = 5;
// SELECT email FROM Employees e JOIN Departments d ON e.department_id = d.department_id WHERE d.department_name = "IT";

// Implement several classes:
// 1. Class Vehicle contains information about the vehicles that drive on the highway. Each vehicle has
// information about its:
// a. Type (can be one of these: Motorcycle, Car, Truck)
// b. License number (string)
// c. Maximum speed (in m/s)
// d. Current speed (in m/s)
// For each type of the vehicle create child class. Maximum speed of a motorcycle is 8 m/s, of a car is 7 m/s and of a truck is 4 m/s. 
// A constructor of each subclass only takes one parameter (a license plate number).
// Provide two methods that accelerate and decelerate a vehicle. Each call to the method will change
// motorcycle’s speed by 2 m/s, car’s speed by 2 m/s and truck’s speed by 1 m/s.
// Minimum speed is 0 m/s.
// Vehicles cannot drive in reverse on the highway. Use virtual methods to implement.
// Create get and set methods if necessary.
// All member variables must be private or protected.
class Vehicle{
    protected:
        std::string license_number;
        int minimum_speed = 0;
        int current_speed = 0;
        int maximum_speed = 0;
    public:
        Vehicle(std::string license_number){
            this->license_number = license_number;
        }
    
    virtual void accelerate() = 0;
    virtual void decelerate() = 0;

    virtual ~Vehicle() = default;
};

class Motorcycle : public Vehicle {
    public:
        Motorcycle(std::string license_number) : Vehicle(license_number) {
            maximum_speed = 7;
        };
    
    void accelerate() override {
        if ((current_speed+2) <= maximum_speed) {
            std::cout << "Motorcycle is accelerating from speed: " << current_speed << " to speed: " << (current_speed += 2) << std::endl;
        } else {
            std::cout << "Motorcycle is already driving at max speed" << std::endl;
        }
    }


    void decelerate() override {
        if ((current_speed-2) >= minimum_speed) {
            std::cout << "Motorcycle is decelerating from speed: " << current_speed << " to speed: " << (current_speed -= 2) << std::endl;
        } else {
            std::cout << "Motorcycle is already at min speed" << std::endl;
        }
    }
};

int main() {
    Motorcycle m("123ABC");

    m.accelerate();
    m.accelerate();
    m.accelerate();
    m.accelerate();
    m.decelerate();
}

