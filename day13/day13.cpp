#include <iostream>
#include <vector>
#include <string>
#include <algorithm>
#include <map>
#include <sstream>
#include <fstream>
#include <set>

using namespace std;

void part1(const pair<set<pair<int, int>>, vector<pair<char, int>>>& dotsAndInstructions);
void part2(const pair<set<pair<int, int>>, vector<pair<char, int>>>& dotsAndInstructions);
pair<set<pair<int, int>>, vector<pair<char, int>>> readInput();
set<pair<int, int>> fold(set<pair<int, int>> &dots, pair<char, int> &instruction);
void foldAll(set<pair<int, int>> &dots, vector<pair<char, int>> &instructions);
int getNumberOfDots(set<pair<int, int>> &dots);
void printDots(const set<pair<int, int>> &dots);


int main() {
    pair<set<pair<int, int>>, vector<pair<char, int>>> dotsAndInstructions = readInput();
    part1(dotsAndInstructions);
    part2(dotsAndInstructions);
    return 0;
}

void part1(const pair<set<pair<int, int>>, vector<pair<char, int>>>& dotsAndInstructions) {
    set<pair<int, int>> dots = dotsAndInstructions.first;
    vector<pair<char, int>> instructions = dotsAndInstructions.second;
    set<pair<int, int>> updatedDots = fold(dots, instructions[0]);
    int numberOfDots = getNumberOfDots(updatedDots);
    cout << "Part 1: " << numberOfDots << endl;
}

void part2(const pair<set<pair<int, int>>, vector<pair<char, int>>>& dotsAndInstructions) {
    set<pair<int, int>> dots = dotsAndInstructions.first;
    vector<pair<char, int>> instructions = dotsAndInstructions.second;
    foldAll(dots, instructions);
    cout << "Part 2: " << endl;
    printDots(dots);
}

pair<set<pair<int, int>>, vector<pair<char, int>>> readInput() {
    set<pair<int, int>> dots;
    vector<pair<char, int>> instructions;
    string line;
    bool isDot = true;
    ifstream file("input.in", ios::in);

    while (getline(file, line)) {
        if (isspace(line[0])) {
            isDot = false;
        }
        else if (isDot) {
            string x, y;
            stringstream ss(line);
            getline(ss, x, ',');
            getline(ss, y, ',');
            dots.insert({stoi(x), stoi(y)});
        } else {
            string temp, value;
            stringstream ss(line);
            char axis = line[11];
            getline(ss, temp, '=');
            getline(ss, value, '=');
            instructions.emplace_back(axis, stoi(value));
        }
    }
    file.close();

    return {dots, instructions};
}

set<pair<int, int>> fold(set<pair<int, int>> &dots, pair<char, int> &instruction) {
    set<pair<int, int>> updatedDots;
    char axis = instruction.first;
    int value = instruction.second;
    for (auto dot : dots) {
        int x = dot.first, y = dot.second;
        if ((axis == 'x' && x == value) || (axis == 'y' && y == value)) {
            continue;
        }
        if (axis == 'x' && x > value) {
            updatedDots.insert({2 * value - x, y});
        } else if (axis == 'y' && y > value) {
            updatedDots.insert({x, 2 * value - y});
        } else {
            updatedDots.insert({x, y});
        }
    }
    return updatedDots;
}

void foldAll(set<pair<int, int>> &dots, vector<pair<char, int>> &instructions) {
    for (auto instruction : instructions) {
        set<pair<int, int>> updatedDots = fold(dots, instruction);
        dots = updatedDots;
    }
}

int getNumberOfDots(set<pair<int, int>> &dots) {
    return dots.size();
}

void printDots(const set<pair<int, int>> &dots) {
    int max_x = -1, max_y = -1;
    for (auto dot : dots) {
        max_x = (dot.first > max_x) ? dot.first : max_x;
        max_y = (dot.second > max_y) ? dot.second : max_y;
    }
    // Initialize grid
    map<pair<int, int>, char> grid;
    for (int j = 0; j < max_y + 1; j++) {
        for (int i = 0; i < max_x + 1; i++) {
            grid[{i, j}] = '.';
        }
    }
    for (auto dot : dots) {
        grid[{dot.first, dot.second}] = '#';
    }
    for (int j = 0; j < max_y + 1; j++) {
        for (int i = 0; i < max_x + 1; i++) {
            cout << grid[{i, j}] << " ";
        }
        cout << endl;
    }
}
