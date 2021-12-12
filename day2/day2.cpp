//
// Created by foong on 2/12/2021.
//
#include <iostream>

using namespace std;


int main() {
    string direction;
    int x, horizontal = 0, depth = 0, aim = 0;
    while (cin >> direction >> x) {
        if (direction == "forward") {
            horizontal += x;
            depth += aim * x;
        } else if (direction == "down") {
            aim += x;
        } else if (direction == "up") {
            aim -= x;
        }
    }
    cout << horizontal << " " << depth << " " << horizontal*depth << endl;

    return 0;
}

