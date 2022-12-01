#include <iostream>
#include <vector>
#include <string>
#include <algorithm>
#include <sstream>
#include <tuple>
#include <numeric>

using namespace std;


int LENGTH_OF_BOARD = 5;

void part1(vector<int> numbers, vector<vector<vector<int>>> boards);
void part2(vector<int> numbers, vector<vector<vector<int>>> boards);
pair<vector<int>, vector<vector<vector<int>>>> readInput();
bool checkWin(vector<vector<vector<int>>> shadowBoards);
vector<int> checkAllWin(vector<vector<vector<int>>> shadowBoards);
vector<vector<vector<int>>> createShadowBoards(vector<vector<vector<int>>> boards);
vector<vector<vector<int>>> markBoard(int number, vector<vector<vector<int>>> boards, vector<vector<vector<int>>> shadowBoards);
tuple<int, vector<int>, vector<vector<int>>> findWinner(vector<int> numbers, vector<vector<vector<int>>> boards, vector<vector<vector<int>>> shadowBoards);
tuple<int, vector<int>, vector<vector<int>>> findLoser(vector<int> numbers, vector<vector<vector<int>>> boards, vector<vector<vector<int>>> shadowBoards);
int getResult(int number, vector<int> pastNumbers, vector<vector<int>> winningBoard);
vector<int> flattenBoard(const vector<vector<int>>& board);
void printBoards(const vector<vector<vector<int>>>& boards);


int main() {
    pair<vector<int>, vector<vector<vector<int>>>> rawInput = readInput();
    vector<int> numbers = rawInput.first;
    vector<vector<vector<int>>> boards = rawInput.second;
    part1(numbers, boards);
    part2(numbers, boards);
    return 0;
}

void part1(vector<int> numbers, vector<vector<vector<int>>> boards) {
    auto shadowBoards = createShadowBoards(boards);
    auto rawResult = findWinner(numbers, boards, shadowBoards);
    int result = getResult(get<0>(rawResult), get<1>(rawResult), get<2>(rawResult));
    cout << "Part 1: " << result << endl;
}

void part2(vector<int> numbers, vector<vector<vector<int>>> boards) {
    auto shadowBoards = createShadowBoards(boards);
    auto rawResult = findLoser(numbers, boards, shadowBoards);
    int result = getResult(get<0>(rawResult), get<1>(rawResult), get<2>(rawResult));
    cout << "Part 2: " << result << endl;
}

pair<vector<int>, vector<vector<vector<int>>>> readInput() {
    string rawNumbers; cin >> rawNumbers;
    vector<int> numbers;
    stringstream ss(rawNumbers);

    for (int i; ss >> i;) {
        numbers.push_back(i);
        if (ss.peek() == ',') {
            ss.ignore();
        }
    }

    vector<vector<vector<int>>> boards;
    vector<vector<int>> board;
    vector<int> row;
    int digit;
    int count = 1;
    while (cin >> digit) {
        row.push_back(digit);
        if (count % 5 == 0 && count != 0) {
            vector<int> rowToPush = row;
            board.push_back(rowToPush);
            row.clear();
        }
        if (count % 25 == 0 && count != 0) {
            vector<vector<int>> boardToPush = board;
            boards.push_back(boardToPush);
            board.clear();
        }
        count++;
    }

    pair<vector<int>, vector<vector<vector<int>>>> output;
    output.first = numbers;
    output.second = boards;
    return output;
}

bool checkWin(vector<vector<int>> shadowBoard) {
    // Check rows
    for (auto row : shadowBoard) {
        int rowSum = accumulate(row.begin(), row.end(), 0);
        if (rowSum == LENGTH_OF_BOARD) {
            return true;
        }
    }
    // Check columns
    for (int i = 0; i < LENGTH_OF_BOARD; i++) {
        int colSum = 0;
        for (int j = 0; j < LENGTH_OF_BOARD; j++) {
            colSum += shadowBoard.at(j).at(i);
        }
        if (colSum == LENGTH_OF_BOARD) {
            return true;
        }
    }
    return false;
}

vector<int> checkAllWin(vector<vector<vector<int>>> shadowBoards) {
    vector<int> winningBoards;
    int numberOfBoards = shadowBoards.size();
    for (int i = 0; i < numberOfBoards; i++) {
        vector<vector<int>> shadowBoard = shadowBoards.at(i);
        if (checkWin(shadowBoard)) {
            winningBoards.push_back(i);
        }
    }
    return winningBoards;
}

vector<vector<vector<int>>> createShadowBoards(vector<vector<vector<int>>> boards) {
    vector<vector<vector<int>>> shadowBoards;
    int numberOfBoards = boards.size();
    for (int i = 0; i < numberOfBoards; i++) {
        vector<vector<int>> board = {{0, 0, 0, 0, 0},
                                     {0, 0, 0, 0, 0},
                                     {0, 0, 0, 0, 0},
                                     {0, 0, 0, 0, 0},
                                     {0, 0, 0, 0, 0}};
        shadowBoards.push_back(board);
    }
    return shadowBoards;
}

vector<vector<vector<int>>> markBoard(int number, vector<vector<vector<int>>> boards, vector<vector<vector<int>>> shadowBoards) {
    int numberOfBoards = boards.size();
    for (int i = 0; i < numberOfBoards; i++) {
        for (int j = 0; j < LENGTH_OF_BOARD; j++) {
            for (int k = 0; k < LENGTH_OF_BOARD; k++) {
                if (number == boards[i][j][k]) {
                    shadowBoards[i][j][k] = 1;
                }
            }
        }
    }
    return shadowBoards;
}

tuple<int, vector<int>, vector<vector<int>>> findWinner(vector<int> numbers, vector<vector<vector<int>>> boards, vector<vector<vector<int>>> shadowBoards) {
    vector<int> pastNumbers;
    for (int number : numbers) {
        pastNumbers.push_back(number);
        vector<vector<vector<int>>> updatedShadowBoards = markBoard(number, boards, shadowBoards);
        shadowBoards = updatedShadowBoards;
        vector<int> winningIndices = checkAllWin(shadowBoards);
        if (winningIndices.empty()) {
            continue;
        }
        int winningIndex = winningIndices[0];
        return make_tuple(number, pastNumbers, boards[winningIndex]);
    }
    return make_tuple(-1, pastNumbers, boards[0]);
}

tuple<int, vector<int>, vector<vector<int>>> findLoser(vector<int> numbers, vector<vector<vector<int>>> boards, vector<vector<vector<int>>> shadowBoards) {
    int lastWinningIndex = -1;
    vector<vector<int>> lastWinner;
    for (int i = 0; i < numbers.size(); i++) {
        int number = numbers[i];
        auto updatedShadowBoards = markBoard(number, boards, shadowBoards);
        shadowBoards = updatedShadowBoards;
        vector<int> winningIndices = checkAllWin(shadowBoards);
        if (!winningIndices.empty()) {
            lastWinningIndex = i;
            lastWinner = boards[winningIndices[winningIndices.size() - 1]];
        }
        reverse(winningIndices.begin(), winningIndices.end());
        for (auto winningIndex : winningIndices) {
            boards.erase(boards.begin() + winningIndex);
            shadowBoards.erase(shadowBoards.begin() + winningIndex);
        }
    }
    int number = numbers[lastWinningIndex];
    vector<int> pastNumbers(numbers.begin(), numbers.begin() + lastWinningIndex + 1);
    return make_tuple(number, pastNumbers, lastWinner);
}

int getResult(int number, vector<int> pastNumbers, vector<vector<int>> winningBoard) {
    int totalSum = 0;
    for (auto row : winningBoard) {
        totalSum += accumulate(row.begin(), row.end(), 0);
    }
    vector<int> flattenedBoard = flattenBoard(winningBoard);
    int sumOfUnmarkedNumbers = totalSum;
    for (int pastNumber : pastNumbers) {
        if (find(flattenedBoard.begin(), flattenedBoard.end(), pastNumber) != flattenedBoard.end()) {
            sumOfUnmarkedNumbers -= pastNumber;
        }
    }
    return sumOfUnmarkedNumbers * number;
}

vector<int> flattenBoard(const vector<vector<int>>& board) {
    vector<int> flattenedBoard;
    for (auto row : board) {
        flattenedBoard.insert(flattenedBoard.end(), row.begin(), row.end());
    }
    return flattenedBoard;
}

void printBoards(const vector<vector<vector<int>>>& boards) {
    for (const auto& board: boards) {
        for (const auto& row: board) {
            for (auto digit: row) {
                cout << digit << " ";
            }
            cout << endl;
        }
        cout << endl;
    }
}
