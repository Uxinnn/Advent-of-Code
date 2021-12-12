#include <iostream>
#include <vector>
#include <string>
#include <algorithm>
#include <unordered_map>
#include <stack>
#include <sstream>
#include <set>

using namespace std;

void part1(unordered_map<string, set<string>> links);
void part2(unordered_map<string, set<string>> links);
unordered_map<string, set<string>> readInput();
void step(unordered_map<string, set<string>> &links, stack<pair<vector<string>, bool>> &connections, set<vector<string>> &fullConnections, bool isPart1);
int getNumberOfFullConnections(unordered_map<string, set<string>> &links, bool isPart1);


int main() {
    unordered_map<string, set<string>> links = readInput();
    part1(links);
    part2(links);
    return 0;
}

void part1(unordered_map<string, set<string>> links) {
    auto numberOfFullConnections = getNumberOfFullConnections(links, true);
    cout << "Part 1: " << numberOfFullConnections << endl;
}

void part2(unordered_map<string, set<string>> links) {
    auto numberOfFullConnections = getNumberOfFullConnections(links, false);
    cout << "Part 2: " << numberOfFullConnections << endl;
}

unordered_map<string, set<string>> readInput() {
    unordered_map<string, set<string>> links;
    string line;
    while (cin >> line) {
        stringstream ss(line);
        string node1, node2;
        getline(ss, node1, '-');
        getline(ss, node2, '-');
        if (links.find(node1) == links.end()) {  // Insert node1 --> node2
            set<string> edges;
            links[node1] = edges;
        }
        links[node1].insert(node2);
        if (links.find(node2) == links.end()) {  // Insert node2 --> node1
            set<string> edges;
            links[node2] = edges;
        }
        links[node2].insert(node1);
    }

    return links;
}

void step(unordered_map<string, set<string>> &links, stack<pair<vector<string>, bool>> &connections, set<vector<string>> &fullConnections, bool isPart1) {
    pair<vector<string>, bool> item = connections.top();
    connections.pop();
    vector<string> connection = item.first;
    bool flag = item.second;
    string lastNode = connection[connection.size() - 1];
    for (const string& link : links[lastNode]) {
        if (link == "start") {
            continue;
        }
        if (islower(link[0]) && (isPart1 || flag) && (find(connection.begin(), connection.end(), link) != connection.end())) {
            continue;
        }
        vector<string> newConnection = connection;
        newConnection.push_back(link);
        if (link == "end") {
            fullConnections.insert(newConnection);
            continue;
        }
        if (isPart1) {
            pair<vector<string>, bool> newItem = {newConnection, flag};
            connections.push(newItem);
        } else {
            if (islower(link[0]) && count(newConnection.begin(), newConnection.end(), link) == 2) {
                pair<vector<string>, bool> newItem = {newConnection, !flag};
                connections.push(newItem);
            } else {
                pair<vector<string>, bool> newItem = {newConnection, flag};
                connections.push(newItem);
            }
        }
    }
}

int getNumberOfFullConnections(unordered_map<string, set<string>> &links, bool isPart1) {
    stack<pair<vector<string>, bool>> connections;
    for (const string& link : links["start"]) {
        connections.push({{"start", link}, false});
    }
    set<vector<string>> fullConnections;
    while (!connections.empty()) {
        step(links, connections, fullConnections, isPart1);
    }
    return fullConnections.size();
}
