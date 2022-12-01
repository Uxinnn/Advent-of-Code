#include <iostream>
#include <vector>
#include <string>
#include <algorithm>
#include <sstream>

using namespace std;

typedef long long ll;

void part1(vector<int> boundingBox);
void part2(vector<int> boundingBox);
vector<int> readInput();
pair<int, ll> findHighestYVelCount(vector<int> &boundingBox);
int simulate(int x_vel, int y_vel, vector<int> &boundingBox);


int main() {
    vector<int> boundingBox = readInput();
    part1(boundingBox);
    part2(boundingBox);
    return 0;
}

void part1(vector<int> boundingBox) {
    int maxMaxHeight = findHighestYVelCount(boundingBox).first;
    cout << "Part 1: " << maxMaxHeight << endl;
}

void part2(vector<int> boundingBox) {
    ll count = findHighestYVelCount(boundingBox).second;
    cout << "Part 2: " << count << endl;
}

vector<int> readInput() {
    int min_x, max_x, min_y, max_y;
    string line;

    cin >> line; cin >> line; cin >> line;
    // Process x range
    string raw_x = line.substr(2);
    raw_x.pop_back();
    int delimiter_index = raw_x.find("..");
    min_x = stoi(raw_x.substr(0, delimiter_index));
    max_x = stoi(raw_x.substr(delimiter_index + 2));

    // Process y range
    cin >> line;
    string raw_y = line.substr(2);
    delimiter_index = raw_y.find("..");
    min_y = stoi(raw_y.substr(0, delimiter_index));
    max_y = stoi(raw_y.substr(delimiter_index + 2));

    return {min_x, max_x, min_y, max_y};
}

pair<int, ll> findHighestYVelCount(vector<int> &boundingBox) {
    int x_max = boundingBox[1], y_min = boundingBox[2];
    vector<int> maxHeights;
    ll count = 0;
    for (int x_vel = 1; x_vel < x_max + 1; x_vel++) {
        for (int y_vel = y_min; y_vel < -y_min; y_vel++) {
            int height = simulate(x_vel, y_vel, boundingBox);
            if (height != -1) {
                maxHeights.push_back(height);
                count++;
            }
        }
    }
    int maxMaxHeight = *max_element(maxHeights.begin(), maxHeights.end());
    return {maxMaxHeight, count};
}

int simulate(int x_vel, int y_vel, vector<int> &boundingBox) {
    int x_min = boundingBox[0], x_max = boundingBox[1], y_min = boundingBox[2], y_max = boundingBox[3];
    int x = 0, y = 0;
    int highestHeight = -1;
    bool inBox = false;
    while ((x <= x_max && y >= y_min) || (x_vel == 0 && y >= y_min)) {
        if (y > highestHeight) {
            highestHeight = y;
        }
        if (x >= x_min && x <= x_max && y >= y_min && y <= y_max) {
            inBox = true;
        }
        x += x_vel; y += y_vel;
        x_vel = (x_vel != 0) ? x_vel - 1 : 0;
        y_vel -= 1;
    }
    if (inBox) {
        return highestHeight;
    }
    return -1;  // When the steps do not hit the bounding box
}

