import java.util.Scanner;

public class Main {
    private static final int SIZE = 8;
    private static final char EMPTY = '-';
    private static final char PLAYER1 = '□';
    private static final char PLAYER2 = '■';
    private static final int[] WEIGHTS = {1, 5, 10}; // Adjust weights based on importance of each feature

    public static void main(String[] args) {
        char[][] board = createBoard();
        char currentPlayer = PLAYER2; // Switched to PLAYER2 for AI to play first

        while (true) {
            printBoard(board);
            System.out.println("Current player: " + currentPlayer);

            if (currentPlayer == PLAYER2) { // AI's turn
                int[] move = getBestMove(board, currentPlayer);
                board[move[0]][move[1]] = currentPlayer;
                if (isWinningMove(board, currentPlayer)) {
                    printBoard(board);
                    System.out.println("Player " + currentPlayer + " wins!");
                    break;
                } else if (isBoardFull(board)) {
                    printBoard(board);
                    System.out.println("It's a tie!");
                    break;
                } else {
                    currentPlayer = PLAYER1;
                }
            } else { // Human player's turn
                System.out.print("Enter row (0-7): ");
                int row = getPlayerInput();
                System.out.print("Enter column (0-7): ");
                int col = getPlayerInput();

                if (isValidMove(board, row, col)) {
                    board[row][col] = currentPlayer;
                    if (isWinningMove(board, currentPlayer)) {
                        printBoard(board);
                        System.out.println("Player " + currentPlayer + " wins!");
                        break;
                    } else if (isBoardFull(board)) {
                        printBoard(board);
                        System.out.println("It's a tie!");
                        break;
                    } else {
                        currentPlayer = PLAYER2;
                    }
                } else {
                    System.out.println("Invalid move! Try again.");
                }
            }
        }
    }

    private static char[][] createBoard() {
        char[][] board = new char[SIZE][SIZE];
        for (int i = 0; i < SIZE; i++) {
            for (int j = 0; j < SIZE; j++) {
                board[i][j] = EMPTY;
            }
        }
        return board;
    }

    private static void printBoard(char[][] board) {
        for (int i = 0; i < SIZE; i++) {
            for (int j = 0; j < SIZE; j++) {
                System.out.print(board[i][j] + " ");
            }
            System.out.println();
        }
    }

    private static int getPlayerInput() {
        Scanner scanner = new Scanner(System.in);
        int input = scanner.nextInt();
        while (input < 0 || input >= SIZE) {
            System.out.println("Invalid input! Try again.");
            input = scanner.nextInt();
        }
        return input;
    }

    private static boolean isValidMove(char[][] board, int row, int col) {
        return board[row][col] == EMPTY && (col == 0 || col == SIZE - 1 || board[row][col - 1] != EMPTY || board[row][col + 1] != EMPTY);
    }

    private static boolean isWinningMove(char[][] board, char player) {
        // Check rows
        for (int i = 0; i < SIZE; i++) {
            for (int j = 0; j <= SIZE - 5; j++) {
                boolean win = true;
                for (int k = 0; k < 5; k++) {
                    if (board[i][j + k] != player) {
                        win = false;
                        break;
                    }
                }
                if (win) {
                    return true;
                }
            }
        }

        // Check columns
        for (int i = 0; i < SIZE; i++) {
            for (int j = 0; j <= SIZE - 5; j++) {
                boolean win = true;
                for (int k = 0; k < 5; k++) {
                    if (board[j + k][i] != player) {
                        win = false;
                        break;
                    }
                }
                if (win) {
                    return true;
                }
            }
        }

        // Check diagonals
        for (int i = 0; i <= SIZE - 5; i++) {
            for (int j = 0; j <= SIZE - 5; j++) {
                boolean win1 = true;
                boolean win2 = true;
                for (int k = 0; k < 5; k++) {
                    if (board[i + k][j + k] != player) {
                        win1 = false;
                    }
                    if (board[i + k][j + 4 - k] != player) {
                        win2 = false;
                    }
                }
                if (win1 || win2) {
                    return true;
                }
            }
        }

        return false;
    }

    private static boolean isBoardFull(char[][] board) {
        for (int i = 0; i < SIZE; i++) {
            for (int j = 0; j < SIZE; j++) {
                if (board[i][j] == EMPTY) {
                    return false;
                }
            }
        }
        return true;
    }

    private static int[] getBestMove(char[][] board, char player) {
        int[] bestMove = new int[]{-1, -1};
        int bestScore = Integer.MIN_VALUE;

        for (int i = 0; i < SIZE; i++) {
            for (int j = 0; j < SIZE; j++) {
                if (isValidMove(board, i, j)) {
                    board[i][j] = player;
                    int score = evaluateBoard(board, player);
                    board[i][j] = EMPTY;

                    if (score > bestScore) {
                        bestScore = score;
                        bestMove[0] = i;
                        bestMove[1] = j;
                    }
                }
            }
        }

        return bestMove;
    }

    private static int evaluateBoard(char[][] board, char player) {
        int score = 0;

        // Evaluate rows
        for (int i = 0; i < SIZE; i++) {
            for (int j = 0; j <= SIZE - 5; j++) {
                int countPlayer1 = 0;
                int countPlayer2 = 0;
                for (int k = 0; k < 5; k++) {
                    if (board[i][j + k] == PLAYER1) {
                        countPlayer1++;
                    } else if (board[i][j + k] == PLAYER2) {
                        countPlayer2++;
                    }
                }
                score += countPlayer1 * WEIGHTS[0] + countPlayer2 * WEIGHTS[1];
            }
        }

        // Evaluate columns
        for (int i = 0; i < SIZE; i++) {
            for (int j = 0; j <= SIZE - 5; j++) {
                int countPlayer1 = 0;
                int countPlayer2 = 0;
                for (int k = 0; k < 5; k++) {
                    if (board[j + k][i] == PLAYER1) {
                        countPlayer1++;
                    } else if (board[j + k][i] == PLAYER2) {
                        countPlayer2++;
                    }
                }
                score += countPlayer1 * WEIGHTS[0] + countPlayer2 * WEIGHTS[1];
            }
        }

        // Evaluate diagonals
        for (int i = 0; i <= SIZE - 5; i++) {
            for (int j = 0; j <= SIZE - 5; j++) {
                int countPlayer1 = 0;
                int countPlayer2 = 0;
                for (int k = 0; k < 5; k++) {
                    if (board[i + k][j + k] == PLAYER1) {
                        countPlayer1++;
                    } else if (board[i + k][j + k] == PLAYER2) {
                        countPlayer2++;
                    }
                }
                score += countPlayer1 * WEIGHTS[0] + countPlayer2 * WEIGHTS[1];

                countPlayer1 = 0;
                countPlayer2 = 0;
                for (int k = 0; k < 5; k++) {
                    if (board[i + k][j + 4 - k] == PLAYER1) {
                        countPlayer1++;
                    } else if (board[i + k][j + 4 - k] == PLAYER2) {
                        countPlayer2++;
                    }
                }
                score += countPlayer1 * WEIGHTS[0] + countPlayer2 * WEIGHTS[1];
            }
        }

        return score;
    }
}
