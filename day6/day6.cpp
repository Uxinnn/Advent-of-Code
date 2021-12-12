#include <iostream>
#include <vector>
#include <string>
#include <sstream>
#include <algorithm>
#include <numeric>

using namespace std;
typedef long long ll;

void part1(vector<ll> ishCount);
void part2(vector<ll> fishCount);
vector<ll> readInput();
vector<ll> simulate1Day(vector<ll> fishCount);
vector<ll> simulateNDays(int n, vector<ll> fishCount);
ll getNumberOfFish(vector<ll> fishCount);


int main() {
    vector<ll> fishCount = readInput();
    part1(fishCount);
    part2(fishCount);
    return 0;
}

void part1(vector<ll> fishCount) {
    vector<ll> updatedFishCount = simulateNDays(80, fishCount);
    ll numberOfFish = getNumberOfFish(updatedFishCount);
    cout << "Part 1: " << numberOfFish << endl;
}

void part2(vector<ll> fishCount) {
    vector<ll> updatedFishCount = simulateNDays(256, fishCount);
    ll numberOfFish = getNumberOfFish(updatedFishCount);
    cout << "Part 2: " << numberOfFish << endl;
}

vector<ll> readInput() {
    string rawInput; cin >> rawInput;
    vector<ll> fishCount(9, 0);
    stringstream ss(rawInput);
    for (int i; ss >> i;) {
        fishCount[i]++;
        if (ss.peek() == ',') {
            ss.ignore();
        }
    }
    return fishCount;
}

vector<ll> simulate1Day(vector<ll> fishCount) {
    ll fishDue = fishCount[0];
    for (int i = 1; i < 9; i++) {
        fishCount[i - 1] = fishCount[i];
    }
    fishCount[8] = fishDue;
    fishCount[6] += fishDue;
    return fishCount;
}

vector<ll> simulateNDays(int n, vector<ll> fishCount) {
    for (int i = 0; i < n; i++) {
        vector<ll> updatedFishCount = simulate1Day(fishCount);
        fishCount = updatedFishCount;
    }
    return fishCount;
}

ll getNumberOfFish(vector<ll> fishCount) {
    return accumulate(fishCount.begin(), fishCount.end(), 0ll);
}
