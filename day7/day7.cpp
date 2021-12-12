#include <iostream>
#include <vector>
#include <string>
#include <sstream>
#include <algorithm>

using namespace std;

void part1(vector<int> crabs);
void part2(vector<int> crabs);
vector<int> readInput();
int median(vector<int> &crabs);
int calcTriNumber(int idx);
int calcTotalFuel(int x, vector<int> &crabs);
int calcTotalFuel2(int x, vector<int> &crabs);


int main() {
    vector<int> crabs = readInput();
    part1(crabs);
    part2(crabs);
    return 0;
}

void part1(vector<int> crabs) {
    int idealLine = median(crabs);
    int totalFuelNeeded = calcTotalFuel(idealLine, crabs);
    cout << "Part 1: " << totalFuelNeeded << endl;
}

void part2(vector<int> crabs) {
    int lowestCrab = *min_element(crabs.begin(), crabs.end());
    int highestCrab = *max_element(crabs.begin(), crabs.end());
    int minFuelNeeded = INT32_MAX;
    for (int i = lowestCrab; i < highestCrab; i++) {
        int fuelNeeded = calcTotalFuel2(i, crabs);
        if (fuelNeeded < minFuelNeeded) {
            minFuelNeeded = fuelNeeded;
        }
    }
    cout << "Part 2: " << minFuelNeeded << endl;
}

vector<int> readInput() {
    vector<int> crabs;
    string line; cin >> line;
    stringstream ss(line);
    for (int i; ss >> i;) {
        crabs.push_back(i);
        if (ss.peek() == ',') {
            ss.ignore();
        }
    }
    return crabs;
}

int median(vector<int> &crabs) {
    size_t n = crabs.size() / 2;
    nth_element(crabs.begin(), crabs.begin() + n, crabs.end());
    return crabs[n];
}

int calcTriNumber(int idx) {
    return idx * (idx + 1) / 2;
}

int calcTotalFuel(int x, vector<int> &crabs) {
    int totalFuel = 0;
    for (int crab : crabs) {
        totalFuel += abs(crab - x);
    }
    return totalFuel;
}

int calcTotalFuel2(int x, vector<int> &crabs) {
    int totalFuel = 0;
    for (int crab : crabs) {
        totalFuel += calcTriNumber(abs(crab - x));
    }
    return totalFuel;
}
