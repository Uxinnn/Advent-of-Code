#include <iostream>
#include <vector>
#include <string>
#include <sstream>
#include <algorithm>
#include <map>

using namespace std;


void part1(vector<vector<vector<int>>> coordinatePairs);
void part2(vector<vector<vector<int>>> coordinatePairs);
vector<vector<vector<int>>> readInput();
vector<int> parseRawCoordinate(const string& rawCoordinate);
vector<vector<vector<int>>> parseCoordinatePairs(vector<vector<vector<int>>> &coordinatePairs, bool isPart1);
map<vector<int>, int> initCoorDict();
void markCoordinates(vector<int> p1, vector<int> p2, map<vector<int>, int> &coorDict);
void markAllCoordinates(vector<vector<vector<int>>> coordinates, map<vector<int>, int> &coorDict);
int getNumberOfDangerPoints(map<vector<int>, int> coorDict);


int main() {
    vector<vector<vector<int>>> coordinatePairs = readInput();
    part1(coordinatePairs);
    part2(coordinatePairs);
    return 0;
}

void part1(vector<vector<vector<int>>> coordinatePairs) {
    vector<vector<vector<int>>> parsedCoordinatePairs = parseCoordinatePairs(coordinatePairs, true);
    auto coorDict = initCoorDict();
    markAllCoordinates(parsedCoordinatePairs, coorDict);
    int numberOfDangerPoints = getNumberOfDangerPoints(coorDict);
    cout << "Part 1: " << numberOfDangerPoints << endl;
}

void part2(vector<vector<vector<int>>> coordinatePairs) {
    vector<vector<vector<int>>> parsedCoordinatePairs = parseCoordinatePairs(coordinatePairs, false);
    auto coorDict = initCoorDict();
    markAllCoordinates(parsedCoordinatePairs, coorDict);
    int numberOfDangerPoints = getNumberOfDangerPoints(coorDict);
    cout << "Part 2: " << numberOfDangerPoints << endl;
}

vector<vector<vector<int>>> readInput() {
    vector<vector<vector<int>>> coordinatePairs;
    for (string line; getline(cin, line);) {
        vector<vector<int>> coordinatePair;
        int pos = 0;
        string token;
        while ((pos = line.find(" -> ")) != string::npos) {
            token = line.substr(0, pos);
            vector<int> coordinate = parseRawCoordinate(token);
            coordinatePair.push_back(coordinate);
            line.erase(0, pos + 4);
        }
        vector<int> coordinate = parseRawCoordinate(line);
        coordinatePair.push_back(coordinate);
        coordinatePairs.push_back(coordinatePair);
    }
    return coordinatePairs;
}

vector<int> parseRawCoordinate(const string& rawCoordinate) {
    vector<int> coordinate;
    stringstream ss(rawCoordinate);
    for (int i; ss >> i;) {
        coordinate.push_back(i);
        if (ss.peek() == ',') {
            ss.ignore();
        }
    }
    return coordinate;
}

// To order coordinate pairs in correct order to facilitate marking of coorDict
// Horizontal lines: Coordinate with smaller x value should be p1.
// Vertical lines: Coordinate with smaller y value should be p1.
// Diagonal lines: Coordinate with smaller x value should be p1.
vector<vector<vector<int>>> parseCoordinatePairs(vector<vector<vector<int>>> &coordinatePairs, bool isPart1) {
    vector<vector<vector<int>>> updatedCoordinatePairs;
    for (auto &coordinatePair : coordinatePairs) {
        vector<int> p1 = coordinatePair[0];
        vector<int> p2 = coordinatePair[1];
        // Filter out diagonals for part 1
        if (isPart1 && p1[0] != p2[0] && p1[1] != p2[1]) {
            continue;
        }
        if (p1[0] == p2[0] && p1[1] > p2[1]) {
            swap(p1[1], p2[1]);
        } else if (p1[1] == p2[1] && p1[0] > p2[0]) {
            swap(p1[0], p2[0]);
        } else {
            if (!isPart1) {
                if (p1[0] > p2[0]) {
                    swap(p1, p2);
                }
            }
        }
        updatedCoordinatePairs.push_back({p1, p2});
    }

    return updatedCoordinatePairs;
}

map<vector<int>, int> initCoorDict() {
    map<vector<int>, int> coorDict;
    return coorDict;
}

void markCoordinates(vector<int> p1, vector<int> p2, map<vector<int>, int> &coorDict) {
    if (p1[1] == p2[1]) {
        int y = p1[1];
        for (int x = p1[0]; x < p2[0] + 1; x++) {
            if (coorDict.count({x, y}) == 0) {
                coorDict[{x, y}] = 0;
            }
            coorDict[{x, y}]++;
        }
    }
    else if (p1[0] == p2[0]) {
        int x = p1[0];
        for (int y = p1[1]; y < p2[1] + 1; y++) {
            if (coorDict.count({x, y}) == 0) {
                coorDict[{x, y}] = 0;
            }
            coorDict[{x, y}]++;
        }
    } else {
        if (p1[1] > p2[1]) {
            for (int i = 0; i < p2[0] - p1[0] + 1; i++) {
                int x = p1[0] + i;
                int y = p1[1] - i;
                if (coorDict.count({x, y}) == 0) {
                    coorDict[{x, y}] = 0;
                }
                coorDict[{x, y}]++;
            }
        } else {
            for (int i = 0; i < p2[0] - p1[0] + 1; i++) {
                int x = p1[0] + i;
                int y = p1[1] + i;
                if (coorDict.count({x, y}) == 0) {
                    coorDict[{x, y}] = 0;
                }
                coorDict[{x, y}]++;
            }
        }
    }
}

void markAllCoordinates(vector<vector<vector<int>>> coordinates, map<vector<int>, int> &coorDict) {
    for (auto coordinatePair : coordinates) {
        auto p1 = coordinatePair[0];
        auto p2 = coordinatePair[1];
        markCoordinates(p1, p2, coorDict);
    }
}

int getNumberOfDangerPoints(map<vector<int>, int> coorDict) {
    int totalDangerPoints = 0;
    for ( auto &entry : coorDict) {
        if (entry.second > 1) {
            totalDangerPoints++;
        }
    }
    return totalDangerPoints;
}
