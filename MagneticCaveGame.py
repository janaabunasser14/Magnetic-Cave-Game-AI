import java.util.Scanner;

public class MagneticCaveGame {
    private static final int BOARD_SIZE = 8;
    private static final int BRIDGE_LENGTH = 5;
    private static final char EMPTY = '-';
    private static final char PLAYER1_BRICK = '■';
    private static final char PLAYER2_BRICK = '□';

    private char[][] board;
    private char currentPlayer;

    public MagneticCaveGame() {
        board = new char[BOARD_SIZE][BOARD_SIZE];
        currentPlayer = PLAYER1_BRICK;

        // Initialize the board with empty cells
        for (int i = 0; i < BOARD_SIZE; i++) {
            for (int j = 0; j < BOARD_SIZE; j++) {
                board[i][j] = EMPTY;
            }
        }
    }

    public void playGame() {
        Scanner scanner = new Scanner(System.in);

        while (true) {
            printBoard();

            System.out.println("Player " + currentPlayer + ", enter the row (0-7): ");
            int row = scanner.nextInt();

            System.out.println("Player " + currentPlayer + ", enter the column (0-7): ");
            int col = scanner.nextInt();

            if (isValidMove(row, col)) {
                board[row][col] = currentPlayer;

                if (isWinningMove(row, col)) {
                    printBoard();
                    System.out.println("Player " + currentPlayer + " wins!");
                    break;
                } else if (isBoardFull()) {
                    printBoard();
                    System.out.println("The game ends in a draw!");
                    break;
                } else {
                    currentPlayer = currentPlayer == PLAYER1_BRICK ? PLAYER2_BRICK : PLAYER1_BRICK;
                }
            } else {
                System.out.println("Invalid move! Please choose an empty cell adjacent to the wall or another brick.");
            }
        }

        scanner.close();
    }

    private boolean isValidMove(int row, int col) {
        if (row < 0 || row >= BOARD_SIZE || col < 0 || col >= BOARD_SIZE || board[row][col] != EMPTY) {
            return false;
        }

        // Check if the cell is adjacent to the wall or another brick
        boolean adjacentToWall = col == 0 || col == BOARD_SIZE - 1;
        boolean adjacentToBrick = (col > 0 && board[row][col - 1] != EMPTY) || (col < BOARD_SIZE - 1 && board[row][col + 1] != EMPTY);

        return adjacentToWall || adjacentToBrick;
    }

    private boolean isWinningMove(int row, int col) {
        char player = board[row][col];

        // Check horizontally
        int count = 0;
        for (int c = Math.max(0, col - BRIDGE_LENGTH + 1); c <= Math.min(BOARD_SIZE - 1, col + BRIDGE_LENGTH - 1); c++) {
            if (board[row][c] == player) {
                count++;
                if (count == BRIDGE_LENGTH) {
                    return true;
                }
            } else {
                count = 0;
            }
        }

        // Check vertically
        count = 0;
        for (int r = Math.max(0, row - BRIDGE_LENGTH + 1); r <= Math.min(BOARD_SIZE - 1, row + BRIDGE_LENGTH - 1); r++) {
            if (board[r][col] == player) {
                count++;
                if (count == BRIDGE_LENGTH) {
                    return true;
                }
            } else {
                count = 0;
            }
        }

        // Check diagonals
        count = 0;
        for (int d = -BRIDGE_LENGTH + 1; d <= BRIDGE_LENGTH - 1; d++) {
            int r = row + d;
            int c = col + d;
            if (r >= 0 && r < BOARD_SIZE && c >= 0 && c < BOARD_SIZE) {
                if (board[r][c] == player) {
                    count++;
                    if (count == BRIDGE_LENGTH) {
                        return true;
                    }
                } else {
                    count = 0;
                }
            }
        }

        count = 0;
        for (int d = -BRIDGE_LENGTH + 1; d <= BRIDGE_LENGTH - 1; d++) {
            int r = row - d;
            int c = col + d;
            if (r >= 0 && r < BOARD_SIZE && c >= 0 && c < BOARD_SIZE) {
                if (board[r][c] == player) {
                    count++;
                    if (count == BRIDGE_LENGTH) {
                        return true;
                    }
                } else {
                    count = 0;
                }
            }
        }

        return false;
    }

    private boolean isBoardFull() {
        for (int i = 0; i < BOARD_SIZE; i++) {
            for (int j = 0; j < BOARD_SIZE; j++) {
                if (board[i][j] == EMPTY) {
                    return false;
                }
            }
        }
        return true;
    }

    private void printBoard() {
        System.out.println("Current board:");

        for (int i = 0; i < BOARD_SIZE; i++) {
            for (int j = 0; j < BOARD_SIZE; j++) {
                System.out.print(board[i][j] + " ");
            }
            System.out.println();
        }
        System.out.println();
    }

    public static void main(String[] args) {
        MagneticCaveGame game = new MagneticCaveGame();
        game.playGame();
    }
}