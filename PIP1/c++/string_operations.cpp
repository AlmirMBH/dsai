#include <iostream>
#include <string>

int main() {
// DATA TYPES
     int age = 25; // Integer type
     double pi = 3.14; // Floating-point type
     char grade = 'A'; // Character type
     bool isPassed = true; // Boolean type
     std::cout << "Age: " << age << ", Pi: " << pi << ", Grade: " << grade << std::endl;

// Strings
     std::string name = "Alice";
     std::cout << "Hello, " << name << "!";

// Read input strings
     std::string first_name;
     std::cout << "Enter your name: ";
     std::cin >> first_name; // Reads input until the first space
     std::cout << "Hello, " << first_name << "!" << std::endl;

// Read input line
     std::string fullName;
     std::cout << "Enter your full name: ";
     std::getline(std::cin, fullName);//Reads the entire line
     std::cout << "Hello, " << fullName << "!" << std::endl;

// String operations
    std::string fName = "Alice";
    std::string lName = "Wonderland";
// Concatenation
    std::string full_name = fName + " " + lName;
    std::cout << "Full name: " << full_name << std::endl;
// Length of the string
    std::cout << "Length: "<< full_name.length()<< std::endl;
    std::cout << "Size: "<< full_name.size()<< std::endl;
// Accessing characters
    std::cout << "First character: " << full_name[0] << std::endl;

// Finding a substring
    int position = full_name.find("Wonder");
    if (position != std::string::npos) { // npos = no position
        std::cout << "'Wonder' found at position: " << position << std::endl;
    }

// Substring extraction
    std::string lastNameExtracted = full_name.substr(position, 2); // index till the end, if no 2nd parameter
    std::cout << "Extracted last name: " << lastNameExtracted << std::endl;

// Replacing part of a string
    full_name.replace(position, 9, "Dreamland"); // (start, length, newText)
    std::cout << "Modified full name: " << full_name << std::endl;

// Inserting into a string
    full_name.insert(6, "L. ");
    std::cout << "After insertion: " << full_name << std::endl;

// Erasing part of a string
    full_name.erase(6, 3);
    std::cout << "After erasing middle initial: " << full_name << std::endl;

// Converting to uppercase (manual method)
    for (char &ch : full_name) {
        ch = std::toupper(ch); // or tolower
    }
    std::cout << "Uppercase full name: " << full_name << std::endl;

// Comparing strings
    if (fName == "Alice") {
        std::cout << "First name matches 'Alice'" << std::endl;
    } else {
        std::cout << "First name does not match 'Alice'" << std::endl;
    }

    return 0;
}
