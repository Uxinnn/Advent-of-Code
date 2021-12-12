#include <iostream>
#include <vector>
#include <string>
#include <algorithm>

using namespace std;


void part1(vector<string> numbers);
void part2(vector<string> numbers);
vector<string> readInput();
pair<int, int> getCountAtIndex(vector<string> &numbers, int idx);
int getGammaEpsilon(vector<string> &numbers, bool mostCommon);
int getO2Co2(vector<string> &numbers, bool isO2);


int main() {
    vector<string> numbers = readInput();
    part1(numbers);
    part2(numbers);
    return 0;
}

void part1(vector<string> numbers) {
    int gamma = getGammaEpsilon(numbers, true);
    int epsilon = getGammaEpsilon(numbers, false);
    cout << "Part 1: " << gamma << ", " << epsilon << ", " << gamma * epsilon << endl;
}

void part2(vector<string> numbers) {
    vector<string> numbers1 = move(numbers);
    vector<string> numbers2 = numbers1;
    int o2 = getO2Co2(numbers1, true);
    int co2 = getO2Co2(numbers2, false);
    cout << "Part 2: " << o2 << ", " << co2 << ", " << o2 * co2 << endl;
}

vector<string> readInput() {
    vector<string> lines;
    string line;
    while (cin >> line) {
        line.erase(remove(line.begin(), line.end(), '\n'), line.end());
        lines.push_back(line);
    }
    return lines;
}

pair<int, int> getCountAtIndex(vector<string> &numbers, int idx) {
    int zeroCount = 0, oneCount = 0;
    for (string number : numbers) {
        number.at(idx) == '0' ? zeroCount++ : oneCount++;
    }
    pair<int, int> counts;
    counts.first = zeroCount;
    counts.second = oneCount;
    return counts;
}

int getGammaEpsilon(vector<string> &numbers, bool mostCommon) {
    int n = numbers[0].length();
    string rate_base2;
    for (int idx = 0; idx < n; idx++) {
        pair<int, int> counts = getCountAtIndex(numbers, idx);
        int zeroCount = counts.first;
        int oneCount = counts.second;
        if (zeroCount > oneCount) {
            mostCommon ? rate_base2 += '0' : rate_base2 += '1';
        } else {
            mostCommon ? rate_base2 += '1' : rate_base2 += '0';
        }
    }
    int rate = stoi(rate_base2, nullptr, 2);
    return rate;
}

int getO2Co2(vector<string> &numbers, bool isO2) {
    int n = numbers.at(0).length();
    for (int idx = 0; idx < n; idx++) {
        pair<int, int> counts = getCountAtIndex(numbers, idx);
        int zeroCount = counts.first;
        int oneCount = counts.second;
        char valueToKeep;
        if (isO2) {
            valueToKeep = zeroCount > oneCount ? '0' : '1';
        } else {
            valueToKeep = zeroCount <= oneCount ? '0' : '1';
        }
        vector<string> temp;
        copy_if(numbers.begin(), numbers.end(), back_inserter(temp), [&valueToKeep, idx](string number){return number.at(idx) == valueToKeep;});
        numbers = temp;
        if (numbers.size() == 1) {
            break;
        }
    }
    int rate = stoi(numbers.at(0), nullptr, 2);
    return rate;
}
