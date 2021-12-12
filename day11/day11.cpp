#include <iostream>
#include <vector>
#include <string>
#include <algorithm>
#include <stack>

using namespace std;

void part1(vector<vector<int>> energyLevel);
void part2(vector<vector<int>> energyLevel);
vector<vector<int>> readInput();
int step(vector<vector<int>> &energyLevel);
int nStep(vector<vector<int>> &energyLevel, int n);
int getSynchronousFlash(vector<vector<int>> &energyLevel);


int main() {
    vector<vector<int>> energyLevel = readInput();
    part1(energyLevel);
    part2(energyLevel);
    return 0;
}

void part1(vector<vector<int>> energyLevel) {
    int totalFlashCount = nStep(energyLevel, 100);
    cout << "Part 1: " << totalFlashCount << endl;
}

void part2(vector<vector<int>> energyLevel) {
    int count = getSynchronousFlash(energyLevel);
    cout << "Part 2: " << count << endl;
}

vector<vector<int>> readInput() {
    vector<vector<int>> energyLevel;
    string line;
    while (cin >> line) {
        vector<int> row;
        for (char number : line) {
            int digit = number - '0';
            row.push_back(digit);
        }
        energyLevel.push_back(row);
    }

    return energyLevel;
}

int step(vector<vector<int>> &energyLevel) {
    stack<pair<int, int>> canFlash;
    int flashCount = 0;
    // Increment by 1
    for (int i = 0; i < energyLevel.size(); i++) {
        for (int j = 0; j < energyLevel[0].size(); j++) {
            energyLevel[i][j]++;
            if (energyLevel[i][j] == 10) {
                canFlash.push({i, j});
            }
        }
    }
    // Flash coordinates and carry out chain reactions
    while (!canFlash.empty()) {
        pair<int, int> coordinate = canFlash.top();
        canFlash.pop();
        int x = coordinate.first, y = coordinate.second;
        energyLevel[x][y] = 11;
        flashCount++;
        vector<pair<int, int>> surroundingCoordinates = {{x - 1, y - 1}, {x - 1, y}, {x - 1, y + 1},
                                                         {x, y - 1}, {x, y}, {x, y + 1},
                                                         {x + 1, y - 1}, {x + 1, y}, {x + 1, y + 1}};
        for (auto surroundingCoordinate : surroundingCoordinates) {
            int x1 = surroundingCoordinate.first, y1 = surroundingCoordinate.second;
            if (x1 < 0 || x1 >= energyLevel.size() || y1 < 0 || y1 >= energyLevel[0].size()) {
                continue;
            }
            if (energyLevel[x1][y1] >= 10) {
                continue;
            }
            energyLevel[x1][y1]++;
            if (energyLevel[x1][y1] == 10) {
                canFlash.push({x1, y1});
            }
        }
    }
    // Reset coordinates that have flashed back to 0
    for (int i = 0; i < energyLevel.size(); i++) {
        for (int j = 0; j < energyLevel[0].size(); j++) {
            if (energyLevel[i][j] == 11) {
                energyLevel[i][j] = 0;
            }
        }
    }
    return flashCount;
}

int nStep(vector<vector<int>> &energyLevel, int n) {
    int totalFlashCount = 0;
    for (int i = 0; i < n; i++) {
        totalFlashCount += step(energyLevel);
    }
    return totalFlashCount;
}

int getSynchronousFlash(vector<vector<int>> &energyLevel) {
    int count = 0, flashCount = 0, maxFlash = energyLevel.size() * energyLevel[0].size();
    while (flashCount != maxFlash) {
        flashCount = step(energyLevel);
        count++;
    }
    return count;
}
