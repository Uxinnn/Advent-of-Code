#include <iostream>
#include <vector>
#include <string>
#include <algorithm>
#include <stack>
#include <unordered_map>

using namespace std;

typedef long long ll;

void part1(vector<string> lines);
void part2(vector<string> lines);
vector<string> readInput();
pair<unordered_map<char, int>, vector<stack<char>>> getAndFilterCorrupted(vector<string> &lines);
int getCorruptedScore(unordered_map<char, int> &corruptedCount);
ll getAutocompleteScore(stack<char> &incompleteStack);
vector<ll> getAutocompleteScores(vector<stack<char>> &incompleteStacks);
ll getMiddleValue(vector<ll> &scores);


int main() {
    vector<string> lines = readInput();
    part1(lines);
    part2(lines);
    return 0;
}


void part1(vector<string> lines) {
    auto output = getAndFilterCorrupted(lines);
    int score = getCorruptedScore(output.first);
    cout << "Part 1: " << score << endl;
}

void part2(vector<string> lines) {
    auto output = getAndFilterCorrupted(lines);
    auto scores = getAutocompleteScores(output.second);
    ll middleScore = getMiddleValue(scores);
    cout << "Part 2: " << middleScore << endl;
}

vector<string> readInput() {
    vector<string> lines;
    string line;
    while (cin >> line) {
        lines.push_back(line);
    }
    return lines;
}

pair<unordered_map<char, int>, vector<stack<char>>> getAndFilterCorrupted(vector<string> &lines) {
    unordered_map<char, int> corruptedCount = {{')', 0}, {']', 0}, {'}', 0}, {'>', 0}};
    vector<stack<char>> incompleteStacks;
    for (const string& line : lines) {
        stack<char> bracketStack;
        bool isCorrupted = false;
        for (char bracket : line) {
            string openBrackets = "([{<";
            if (openBrackets.find(bracket) != string::npos) {
                bracketStack.push(bracket);
            } else if ((bracket == ')' && bracketStack.top() == '(') ||
                       (bracket == ']' && bracketStack.top() == '[') ||
                       (bracket == '}' && bracketStack.top() == '{') ||
                       (bracket == '>' && bracketStack.top() == '<')) {
                bracketStack.pop();
            } else {
                corruptedCount[bracket]++;
                isCorrupted = true;
                break;
            }
        }
        if (!isCorrupted) {
            incompleteStacks.push_back(bracketStack);
        }
    }
    pair<unordered_map<char, int>, vector<stack<char>>> output;
    output.first = corruptedCount;
    output.second = incompleteStacks;
    return output;
}

int getCorruptedScore(unordered_map<char, int> &corruptedCount) {
    int score = corruptedCount[')'] * 3 +
                corruptedCount[']'] * 57 +
                corruptedCount['}'] * 1197 +
                corruptedCount['>'] * 25137;
    return score;
}

ll getAutocompleteScore(stack<char> &incompleteStack) {
    unordered_map<char, int> points = {{'(', 1}, {'[', 2}, {'{', 3}, {'<', 4}};
    ll score = 0;
    while (!incompleteStack.empty()) {
        char bracket = incompleteStack.top();
        incompleteStack.pop();
        score *= 5;
        score += points[bracket];
    }
    return score;
}

vector<ll> getAutocompleteScores(vector<stack<char>> &incompleteStacks) {
    vector<ll> scores;
    for (auto stack : incompleteStacks) {
        ll points = getAutocompleteScore(stack);
        scores.push_back(points);
    }
    return scores;
}

ll getMiddleValue(vector<ll> &scores) {
    sort(scores.begin(), scores.end());
    return scores[scores.size() / 2];
}
