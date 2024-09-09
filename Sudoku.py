import tkinter as tk
from tkinter import messagebox

# 스도쿠 해결 함수 (이전 코드 그대로 유지)
def solve_sudoku(board):
    empty_pos = find_empty_cell(board)
    if not empty_pos:
        return True
    row, col = empty_pos

    for num in range(1, 10):
        if is_valid_move(board, num, row, col):
            board[row][col] = num
            if solve_sudoku(board):
                return True
            board[row][col] = 0

    return False

# 빈 칸 찾기 함수
def find_empty_cell(board):
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                return row, col
    return None

# 유효성 검사 함수
def is_valid_move(board, num, row, col):
    return (is_valid_in_row(board, num, row) and
            is_valid_in_col(board, num, col) and
            is_valid_in_box(board, num, row, col))

def is_valid_in_row(board, num, row):
    return num not in board[row]

def is_valid_in_col(board, num, col):
    return num not in [board[row][col] for row in range(9)]

def is_valid_in_box(board, num, row, col):
    box_start_row, box_start_col = row // 3 * 3, col // 3 * 3
    for i in range(box_start_row, box_start_row + 3):
        for j in range(box_start_col, box_start_col + 3):
            if board[i][j] == num:
                return False
    return True

# GUI 구현 클래스
class SudokuGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("스도쿠 해결 프로그램")

        # 스타일 속성
        self.bg_color = "#f0f0f0"
        self.btn_color = "#4caf50"
        self.entry_white_color = "#ffffff"
        self.entry_black_color = "#c0c0c0"
        self.border_color = "black"
        self.font_style = ("Arial", 18)

        # 창 배경색 설정
        self.root.config(bg=self.bg_color)
        self.cells = {}

        # UI 그리드 생성 및 버튼 추가
        self.create_grid()
        self.create_buttons()

    # 9x9 그리드 생성 함수
    def create_grid(self):
        for row in range(9):
            for col in range(9):
                bg_color = self.entry_white_color if (row // 3 + col // 3) % 2 == 0 else self.entry_black_color
                
                cell = tk.Entry(self.root, width=5, justify="center", font=self.font_style, bg=bg_color, highlightthickness=1)
                cell.grid(row=row, column=col, padx=2, pady=2, ipadx=5, ipady=5)

                # 3x3 경계를 그리기 위한 조건 설정
                if col % 3 == 0:
                    cell.grid_configure(padx=(4, 2))  # 왼쪽 경계선 더 두껍게
                if row % 3 == 0:
                    cell.grid_configure(pady=(4, 2))  # 위쪽 경계선 더 두껍게
                if (row + 1) % 3 == 0:
                    cell.grid_configure(pady=(2, 4))  # 3x3 하단 경계선
                if (col + 1) % 3 == 0:
                    cell.grid_configure(padx=(2, 4))  # 3x3 우측 경계선

                self.cells[(row, col)] = cell

    # 버튼 및 UI 요소 생성 함수
    def create_buttons(self):
        solve_button = tk.Button(self.root, text="풀기", command=self.solve_puzzle, bg=self.btn_color, fg="white", font=self.font_style)
        solve_button.grid(row=10, column=0, columnspan=5, pady=10, ipadx=10)

        clear_button = tk.Button(self.root, text="초기화", command=self.clear_board, bg=self.btn_color, fg="white", font=self.font_style)
        clear_button.grid(row=10, column=5, columnspan=5, pady=10, ipadx=10)

    # 사용자 입력을 보드로 변환하는 함수
    def get_board_from_input(self):
        board = []
        for row in range(9):
            current_row = []
            for col in range(9):
                cell_value = self.cells[(row, col)].get()
                if cell_value == "":
                    current_row.append(0)
                else:
                    current_row.append(int(cell_value))
            board.append(current_row)
        return board

    # 보드 해결 및 결과 표시 함수
    def solve_puzzle(self):
        board = self.get_board_from_input()

        if solve_sudoku(board):
            self.update_grid_with_solution(board)
        else:
            messagebox.showinfo("오류", "해결할 수 없는 보드입니다.")

    # 해결된 결과를 그리드에 표시하는 함수
    def update_grid_with_solution(self, board):
        for row in range(9):
            for col in range(9):
                self.cells[(row, col)].delete(0, "end")
                self.cells[(row, col)].insert(0, str(board[row][col]))

    # 보드 초기화 함수
    def clear_board(self):
        for row in range(9):
            for col in range(9):
                self.cells[(row, col)].delete(0, "end")

# 메인 실행 부분
if __name__ == "__main__":
    root = tk.Tk()
    gui = SudokuGUI(root)
    root.mainloop()
