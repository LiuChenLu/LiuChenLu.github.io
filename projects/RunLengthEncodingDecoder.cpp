#include <iostream>
#include <string> 
#include <stack>
#include <queue>
#include <stdlib.h>
#include <sstream>
using namespace std;

/* Question A of ACM programming contest
 * 
 * A run length encoding (RLE) in this problem is defined as either
 *   -a single, lower-case letter
 *   -(e1 e2 e3 ... et n) where t and n are non-negative integers, and ei is a 
 *    ompressed word
 * To decompressed a string compressed by RLE, we must compress each ei, 
 * concatenate those uncompressed words into a new word, and repeatly 
 * concatenate that word n times.
 *
 * Keep in mind that there may be any number of white space (tab, space, \r, 
 * \f) can be between any ei
 * 
 * For example: 
 *   x             is uncompressed as x
 *   (t       3)   is uncompressed as ttt
 *   (a (b c 2) 3) is uncompressed as abcbcabcbcabcbc
 *   (a 0)         is uncompressed as
 *   (a 10)        is uncompressed as aaaaaaaaaa
 *
 * Each test case is made of one correctly compressed word on a separate line
 * $ marks the end of line. The last line of input is a single $ to mark EOF
 *
 * For example, input:
 *   x$
 *    (t 3)$
 *   (a b ( c 2) 1) $
 *   (a 1)$ at the end of the world
 *          $ 
 * output:
 *   x
 *   ttt
 *   abcc
 *   a
 *
 */


bool is_number(const std::string& s)
{
    std::string::const_iterator it = s.begin();
    while (it != s.end() && std::isdigit(*it)) ++it;
    return !s.empty() && it == s.end();
}

void decompress (queue<string> & toProcess, stack<string> & processed) {
    string tmp;
    while (!toProcess.empty()) {
        tmp=toProcess.front();
        toProcess.pop();
        /// cout << "processing: " << tmp << ", with " << toProcess.size() << "remaining" << endl;
        if (tmp == "(") {
            processed.push(tmp);
        } else if (tmp == ")") {
            string prev1=processed.top();
            processed.pop();
            string prev2=processed.top();
            processed.pop();
            if (prev2=="(") processed.push(prev1);
            else exit(2);
        } else if (is_number(tmp)) {
            string peep = toProcess.front();
            while (is_number(peep)) {
                tmp=tmp+peep;
                toProcess.pop();
                peep=toProcess.front();
            }
            int value = atoi (tmp.c_str());
            string pop = processed.top();
            processed.pop();
            string prev; string push;
            while (pop != "(") {
                prev=pop+prev;
                pop=processed.top();
                processed.pop();
            }
            processed.push("(");
            while (value>0) {
                value-=1;
                push=prev+push;
            }
            processed.push(push);
        } else if (tmp == "$") {
            cout << processed.top() << endl;
            /// cout << "printed something" << endl;
            return;
        } else {
            /// cout << "pushed "<<tmp<<" onto processed"<<endl;
            processed.push(tmp);
        }
    }
    /// cout << "exited the loop without printing" << endl;
}

bool space(char &c) {
    return c!=' ' and c!='\t' and c!='\n' and c!='\v' and c!='\f' and c!='\r';
}

int main () {
    string line = "";
    while(true) {
        getline(cin,line);
        if (false and line == "$") break;
        else {
            // stringstream s (line);
            queue<string> toProcess;
            stack<string> processed;

            /*while (true) {generalities
                string tmp;
                s >> tmp;
                toProcess.push(tmp);

                if (s.good()) continue;
                else break;
            }*/

            for (int i=0;
                 i<line.length();
                 i++) {
                if (line.at(i)!=' ' and line.at(i)!='\t'
                    and line.at(i)!='\n' and line.at(i)!='\v'
                    and line.at(i)!='\f' and line.at(i)!='\r') {
                    string c =line.substr(i,1);
                    toProcess.push(c);
                }
            }
            if (toProcess.front()=="$") break;
            /// cout << "about to call compress" << endl;
            decompress(toProcess,processed);
        }
    }
    return 0;
}

