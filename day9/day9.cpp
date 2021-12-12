#include <iostream>
#include <vector>
#include <string>
#include <algorithm>

using namespace std;

void part1(vector<vector<int>> heightMap);
void part2(vector<vector<int>> heightMap);
vector<vector<int>> readInput();
vector<int> getLowPoints(vector<vector<int>> &heightMap);
int getSumOfRiskLevels(vector<int> &lowPoints);
int floodFill(int x, int y, vector<vector<int>> &heightMap, int size);
vector<int> getBasinSizes(vector<vector<int>> &heightMap);
int getPart2Answer(vector<int> &basinSizes);


int main() {
    vector<vector<int>> heightMap = readInput();
    part1(heightMap);
    part2(heightMap);
    return 0;
}


void part1(vector<vector<int>> heightMap) {
    vector<int> lowPoints = getLowPoints(heightMap);
    int sumOfRiskLevels = getSumOfRiskLevels(lowPoints);
    cout << "Part 1: " << sumOfRiskLevels << endl;
}

void part2(vector<vector<int>> heightMap) {
    vector<int> basinSizes = getBasinSizes(heightMap);
    int answer = getPart2Answer(basinSizes);
    cout << "Part 2: " << answer << endl;
}

vector<vector<int>> readInput() {
    vector<vector<int>> heightMap;
    string line;
    bool isFirstLine = true;
    while (cin >> line) {
        if (isFirstLine) {
            vector<int> firstRow(line.size() + 2, 10);
            heightMap.push_back(firstRow);
            isFirstLine = false;
        }
        vector<int> row;
        row.push_back(10);
        for (char number : line) {
            int digit = number - '0';
            row.push_back(digit);
        }
        row.push_back(10);
        heightMap.push_back(row);
    }
    vector<int> lastRow(line.size() + 2, 10);
    heightMap.push_back(lastRow);
    return heightMap;
}

vector<int> getLowPoints(vector<vector<int>> &heightMap) {
    vector<int> lowPoints;
    for (int i = 1; i < heightMap.size() - 1; i++) {
        for (int j = 1; j < heightMap[0].size() - 1; j++) {
            int value = heightMap[i][j];
            if (value < heightMap[i][j - 1] and value < heightMap[i][j + 1] and value < heightMap[i - 1][j] and value < heightMap[i + 1][j]) {
                lowPoints.push_back(value);
            }
        }
    }
    return lowPoints;
}

int getSumOfRiskLevels(vector<int> &lowPoints) {
    int totalRiskLevels = 0;
    for (auto point : lowPoints) {
        totalRiskLevels += (point + 1);
    }
    return totalRiskLevels;
}

int floodFill(int x, int y, vector<vector<int>> &heightMap, int size) {
    if (heightMap[x][y] > 8) {
        return size;
    }
    heightMap[x][y] = 9;

    int size1 = floodFill(x + 1, y, heightMap, size + 1);
    int size2 = floodFill(x - 1, y, heightMap, size1);
    int size3 = floodFill(x, y + 1, heightMap, size2);
    int size4 = floodFill(x, y - 1, heightMap, size3);

    return size4;
}

vector<int> getBasinSizes(vector<vector<int>> &heightMap) {
    vector<int> basinSizes;
    for (int i = 1; i < heightMap.size() - 1; i++) {
        for (int j = 1; j < heightMap[0].size() - 1; j++) {
            if (heightMap[i][j] < 9) {
                int basinSize = floodFill(i, j, heightMap, 0);
                basinSizes.push_back(basinSize);
            }
        }
    }
    return basinSizes;
}

int getPart2Answer(vector<int> &basinSizes) {
    sort(basinSizes.begin(), basinSizes.end());
    int answer = 1;
    for (int i = basinSizes.size() - 3; i < basinSizes.size(); i++) {
        answer *= basinSizes[i];
    }
    return answer;
}
