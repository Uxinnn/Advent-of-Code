#include <iostream>
#include <vector>
#include <string>
#include <algorithm>
#include <sstream>
#include <fstream>
#include <unordered_map>

using namespace std;

typedef long long ll;

void part1(const pair<unordered_map<string, ll>, unordered_map<string, string>>& polymerAndRules);
void part2(const pair<unordered_map<string, ll>, unordered_map<string, string>>& polymerAndRules);
pair<unordered_map<string, ll>, unordered_map<string, string>> readInput();
void insertOnce(unordered_map<string, ll> &polymer, const unordered_map<string, string> &rules);
void insertN(unordered_map<string, ll> &polymer, const unordered_map<string, string> &rules, int n);
pair<ll, ll> getMostLeastCommonElement(const unordered_map<string, ll> &polymer);


int main() {
    pair<unordered_map<string, ll>, unordered_map<string, string>> polymerAndRules = readInput();
    part1(polymerAndRules);
    part2(polymerAndRules);
    return 0;
}

void part1(const pair<unordered_map<string, ll>, unordered_map<string, string>>& polymerAndRules) {
    unordered_map<string, ll> polymer = polymerAndRules.first;
    unordered_map<string, string> rules = polymerAndRules.second;
    insertN(polymer, rules, 10);
    pair<ll, ll> counts = getMostLeastCommonElement(polymer);
    ll answer = counts.first - counts.second;
    cout << "Part 1: " << answer << endl;
}

void part2(const pair<unordered_map<string, ll>, unordered_map<string, string>>& polymerAndRules) {
    unordered_map<string, ll> polymer = polymerAndRules.first;
    unordered_map<string, string> rules = polymerAndRules.second;
    insertN(polymer, rules, 40);
    pair<ll, ll> counts = getMostLeastCommonElement(polymer);
    ll answer = counts.first - counts.second;
    cout << "Part 1: " << answer << endl;
}

pair<unordered_map<string, ll>, unordered_map<string, string>> readInput() {
    unordered_map<string, ll> polymer;
    unordered_map<string, string> rules;
    string line;

    // Process first line
    cin >> line;
    for (int i = 0; i < line.size() - 1; i++) {
        string pairOfElements = line.substr(i, 2);
        if (polymer.find(pairOfElements) == polymer.end()) {
            polymer[pairOfElements] = 0;
        }
        polymer[pairOfElements]++;
    }

    // Process rules
    string pairOfElements, value;
    while (cin >> pairOfElements) {
        cin >> line; cin >> value;
        rules[pairOfElements] = value;
    }

    return {polymer, rules};
}

void insertOnce(unordered_map<string, ll> &polymer, const unordered_map<string, string> &rules) {
    vector<pair<string, ll>> temp;
    for (const auto& pairOfElementsCount : polymer) {
        if (pairOfElementsCount.second == 0) {
            continue;
        }
        temp.emplace_back(pairOfElementsCount);
    }
    for (const auto& pairOfElementsCount : temp) {
        string pairOfElements = pairOfElementsCount.first;
        ll count = pairOfElementsCount.second;
        polymer[pairOfElements] -= count;
        const string& element = rules.at(pairOfElements);
        string firstPair = pairOfElements[0] + element, secondPair = element + pairOfElements[1];
        if (polymer.find(firstPair) == polymer.end()) {
            polymer[firstPair] = 0;
        }
        polymer[firstPair] += count;
        if (polymer.find(secondPair) == polymer.end()) {
            polymer[secondPair] = 0;
        }
        polymer[secondPair] += count;
    }
}

void insertN(unordered_map<string, ll> &polymer, const unordered_map<string, string> &rules, int n) {
    for (int i = 0; i < n; i++) {
        insertOnce(polymer, rules);
    }
}

pair<ll, ll> getMostLeastCommonElement(const unordered_map<string, ll> &polymer) {
    unordered_map<char, ll> elementCount;
    for (const auto& pairOfElementsCount : polymer) {
        string pairOfElements = pairOfElementsCount.first;
        ll count = pairOfElementsCount.second;
        for (int i = 0; i < 2; i++) {
            char element = pairOfElements[i];
            if (elementCount.find(element) == elementCount.end()) {
                elementCount[element] = 0;
            }
            elementCount[element] += count;
        }
    }
    vector<ll> counts;
    for (auto elementAndCount : elementCount) {
        ll count = elementAndCount.second;
        counts.push_back(1 + ((count - 1) / 2));  // Ceiling division, avoids integer overflow too
    }
    ll maxCount = *max_element(counts.begin(), counts.end());
    ll minCount = *min_element(counts.begin(), counts.end());
    return {maxCount, minCount};
}
