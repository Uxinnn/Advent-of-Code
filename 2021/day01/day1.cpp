#include <iostream>
#include <vector>
#include <string>
#include <algorithm>

using namespace std;


void part1(vector<int> numbers);
void part2(vector<int> numbers);
vector<int> readInput();
int countIncrease(vector<int> numbers);
vector<int> convertTo3Window(vector<int> numbers);


int main() {
    vector<int> numbers = readInput();
    part1(numbers);
    part2(numbers);
    return 0;
}

void part1(vector<int> numbers) {
    int count = countIncrease(move(numbers));
    cout << "Part 1 Answer: " << count << endl;
}

void part2(vector<int> numbers) {
    vector<int> numbers3Window = convertTo3Window(move(numbers));
    int count = countIncrease(numbers3Window);
    cout << "Part 2 Answers: " << count << endl;
}

vector<int> readInput() {
    vector<int> lines;
    string line;
    while (cin >> line) {
        line.erase(remove(line.begin(), line.end(), '\n'), line.end());
        lines.push_back(stoi(line));
    }
    return lines;
}

int countIncrease(vector<int> numbers) {
    int count = 0, prevNumber = numbers.at(0);
    for (int i = 1; i < numbers.size(); i++) {
        int number = numbers.at(i);
        if (number > prevNumber) {
            count++;
        }
        prevNumber = number;
    }
    return count;
}


vector<int> convertTo3Window(vector<int> numbers) {
    vector<int> numbers3Window;
    for (int i = 1; i < numbers.size() - 1; i++) {
        int value = numbers.at(i - 1) + numbers.at(i) + numbers.at(i + 1);
        numbers3Window.push_back(value);
    }
    return numbers3Window;
}
