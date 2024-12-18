#include <iostream>
#include <string>
#include <algorithm>
#include <tuple>

using namespace std;
/**
Write a C++ program that performs the following tasks related to string manipulation:
1) Accept Two Strings: Take two strings as input from the user and concatenated them to form a single string.
2. Concatenate the Strings: Combine the two strings into a single string and print the result.
3. Find the Position of a Substring:
- Prompt the user to input a substring to search for within the concatenated string.
- Use the find method to determine the position of the first occurrence of the substring.
- If the substring is found, display its position. If not, print an appropriate message.
4. Count the Occurrences of the Substring:
- Count and print the number of times the substring appears in the concatenated string.
- Use the two-parameter version of the find method for this:
- The first parameter, substring, is the text you want to find.
- The second parameter, startPos, specifies where to start searching in the string.
- By incrementing startPos after each match, you can find subsequent occurrences of the substring.
5. Reverse the Concatenated String: Reverse the concatenated string manually (without using the std::reverse function) and print the reversed string.
*/

string getUserInputConcatenated() {
    string str1, str2, concatenated;
    cout << "Enter first string: ";
    getline(cin, str1);
    cout << "Enter second string: ";
    getline(cin, str2);
    concatenated = str1 + str2;
    cout << "Concatenated string: " << concatenated << endl;
    return concatenated;
}


string stringToLowerCase(const string &str) {
    string result = str;
    transform(result.begin(), result.end(), result.begin(), ::tolower);
    return result;
}


void getSubstringOccurrences(const string &concatenated) {
    string substring;
    size_t startPos = 0; // unsigned
    int count = 0;

    cout << "Enter substring: ";
    getline(cin, substring);

    string lowerConcatenated = stringToLowerCase(concatenated);
    string lowerSubstring = stringToLowerCase(substring);

    cout << "Substring found at position(s): ";
    while ((startPos = lowerConcatenated.find(lowerSubstring, startPos)) != string::npos) {
        cout << startPos << " ";
        ++count;
        startPos += lowerSubstring.length();
    }

    if (count > 0) {
        cout << endl << "Substring appears " << count << " time(s)." << endl;
    } else {
        cout << "Substring not found." << endl;
    }
}


void reverseString(string concatenated){
    string reversed = "";
    for (int i = concatenated.length() - 1; i >= 0; --i) {
        reversed += concatenated[i];
    }
    cout << "Reversed string: " << reversed << endl;
}


void stringOperations() {
    string str1;
    string str2;
    string concatenatedInput;
    string substring;
    concatenatedInput = getUserInputConcatenated();
    string lowerConcatenated = stringToLowerCase(concatenatedInput);
    getSubstringOccurrences(lowerConcatenated);
    reverseString(concatenatedInput);
}


int main() {
    stringOperations();
    return 0;
}
