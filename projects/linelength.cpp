//////////////////////////////////////////////////////////////////
//
// Liu Chen Lu
// 
// checking line numbering
//
//	Reads a set of lines from standard input using the C++ I/O
//	streaming facilities. Each line will start with a number (an
//	integer) and will be followed by zero or more words.
//	The literals in each line are assumed to be separated by
//	exactly one space, with no trailing space at the end.
//
//	The program will print the lines for which the starting
//	number does not match the number of words (or literals) in
//	that line, with the modification that the output line should
//	now contain the correct number of words in each line.
//
//	For an example of the implimentation of this code, see tests
//	at the end of this program
//
////////////////////////////////////////////////////////////////////

#include<iostream>
#include<string>

using std::cin;
using std::cout;
using std::endl;
using std::string;

int main (){
	
	while (cin) {
		int linelen;
		cin>>linelen;
		
		// if cin read eof then cin.fail will be true and the program
		// breaks out of the while loop
		// if this line is not here the program will print out the last
		// number twice
	if (cin.fail()) break;
		
		// a string that will hold an entire line read from cin
		string line;
		// read a line until it ends into the string line
		std::getline(cin, line, '\n');

		// the length of the string, ie the number of characters 
		// in the string
		int length = line.length();

		// i is to be the actual number of words in the string
		int i = 0;
		for (int pos = 0; pos<length; i++, pos++){
			// find the position of the next space character
			pos = line.find (' ', pos);
			// if line.find did not find a new position
			if (pos == string::npos) break;
		}
		// if the number of words on the line is not the same as it
		//  claims, print the actual number of words and the line
		if (i != linelen) 
			cout << i << line << endl;
	}
	// when loop exits all the input has been dealt with

	return 1;
}

/*
tests
~/cs246/a02$ ./a2p2.out < test2.in
10 a b c d f d d d d d
~/cs246/a02$ cat test2.in
9 a b c d f d d d d d
1 a

~/cs246/a02$ ./a2p2.out < test.in
6 there seven words in this line
5 this line is not consistent
2 another error
~/cs246/a02$ cat test.in
7 there seven words in this line
5 how many words are there
6 this line is not consistent
5 He is 100 years old
8 another error

~/cs246/a02$ ./a2p2.out < test3.in
0
~/cs246/a02$ cat test3.in
2
0

*/
