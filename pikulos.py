import tkinter as tk
from tkinter import messagebox

class PicrossGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("피크로스 퍼즐")

        self.size = 5  # 기본 크기
        self.grid_frame = tk.Frame(self.root)
        self.grid_frame.grid(row=2, column=1, padx=10, pady=10)

        self.cells = {}  # 클릭 가능한 셀들을 저장할 딕셔너리
        self.row_hints = []  # 행 힌트 입력창
        self.col_hints = []  # 열 힌트 입력창

        # 판 크기 입력 필드
        self.create_size_input()

        # UI 생성 (초기 5x5 크기)
        self.create_input_boxes()
        self.create_clickable_grid()

        # 버튼 생성
        self.create_buttons()

    def create_size_input(self):
        """판 크기를 입력할 수 있는 입력창을 생성."""
        tk.Label(self.root, text="판 크기:").grid(row=0, column=0, padx=10, pady=5)
        self.size_entry = tk.Entry(self.root, width=5)
        self.size_entry.grid(row=0, column=1, padx=5, pady=5)
        self.size_entry.insert(0, "5")  # 기본 크기

    def create_input_boxes(self):
        """행과 열의 힌트를 입력할 수 있는 입력창을 생성."""
        # 기존 입력창 초기화
        for widget in self.grid_frame.winfo_children():
            widget.destroy()
        self.row_hints.clear()
        self.col_hints.clear()

        # 세로 힌트 (가장 왼쪽)
        for row in range(self.size):
            row_hint = tk.Entry(self.grid_frame, width=5, font=("Arial", 12))
            row_hint.grid(row=row + 1, column=0, padx=5, pady=5)
            self.row_hints.append(row_hint)

        # 가로 힌트 (가장 위쪽)
        for col in range(self.size):
            col_hint = tk.Entry(self.grid_frame, width=5, font=("Arial", 12))
            col_hint.grid(row=0, column=col + 1, padx=5, pady=5)
            self.col_hints.append(col_hint)

    def create_clickable_grid(self):
        """클릭 가능한 피크로스 셀 그리드를 생성."""
        self.cells = {}
        for row in range(self.size):
            for col in range(self.size):
                cell = tk.Label(self.grid_frame, width=2, height=1, bg="white", relief="solid")
                cell.grid(row=row + 1, column=col + 1, padx=1, pady=1)
                self.cells[(row, col)] = cell

    def set_cell_color(self, row, col, color):
        """특정 셀의 색상을 설정."""
        self.cells[(row, col)].config(bg=color)

    def solve_puzzle(self):
        """입력된 힌트를 바탕으로 퍼즐을 재귀적으로 해결."""
        try:
            # 힌트 가져오기 및 형식 맞추기
            row_hints = [self.parse_hint(hint.get().strip()) for hint in self.row_hints]
            col_hints = [self.parse_hint(hint.get().strip()) for hint in self.col_hints]

            # 그리드 초기화
            self.clear_board()

            # 초기 빈 그리드
            grid = [[-1] * self.size for _ in range(self.size)]  # -1은 아직 결정되지 않은 셀을 의미

            # 재귀적으로 퍼즐 해결
            if self.solve_recursive(grid, row_hints, col_hints, 0):
                # 해결된 결과를 GUI에 반영
                self.update_gui(grid)
            else:
                messagebox.showerror("오류", "해결할 수 없는 퍼즐입니다.")
        except Exception as e:
            messagebox.showerror("오류", f"문제가 발생했습니다: {e}")

    def parse_hint(self, hint):
        """입력된 힌트를 공백 기준으로 숫자로 변환."""
        return list(map(int, hint.split())) if hint else []

    def solve_recursive(self, grid, row_hints, col_hints, row):
        """재귀적으로 피크로스 퍼즐을 해결하는 함수."""
        # 재귀 종료 조건: 모든 행이 처리되었으면 퍼즐 해결 성공
        if row == self.size:
            return self.check_cols(grid, col_hints)

        # 현재 행에 대해 가능한 패턴을 생성
        patterns = self.generate_patterns(row_hints[row], self.size)

        # 각 패턴을 적용해보고, 그다음 행을 재귀적으로 처리
        for pattern in patterns:
            grid[row] = pattern
            if self.check_partial_cols(grid, col_hints, row):  # 현재까지 열들이 유효한지 확인
                if self.solve_recursive(grid, row_hints, col_hints, row + 1):  # 다음 행을 재귀적으로 처리
                    return True

        # 가능한 패턴 중에 유효한 것이 없으면 false 반환
        return False

    def check_cols(self, grid, col_hints):
        """모든 열이 주어진 힌트를 만족하는지 확인."""
        for col in range(self.size):
            col_pattern = [grid[row][col] for row in range(self.size)]
            if not self.pattern_matches(col_pattern, col_hints[col]):
                return False
        return True

    def check_partial_cols(self, grid, col_hints, row):
        """현재까지의 열이 유효한지 확인 (부분적으로)."""
        for col in range(self.size):
            col_pattern = [grid[r][col] for r in range(row + 1)]
            if not self.partial_pattern_matches(col_pattern, col_hints[col]):
                return False
        return True

    def pattern_matches(self, pattern, hint):
        """주어진 패턴이 힌트를 만족하는지 확인."""
        return self.generate_patterns(hint, len(pattern)) == [pattern]

    def partial_pattern_matches(self, pattern, hint):
        """부분적인 패턴이 힌트와 일치하는지 확인."""
        return any(p[:len(pattern)] == pattern for p in self.generate_patterns(hint, self.size))

    def generate_patterns(self, hint, size):
        """주어진 힌트에 맞는 가능한 패턴을 생성."""
        patterns = []
        self.backtrack_patterns(hint, size, 0, [], patterns)
        return patterns

    def backtrack_patterns(self, hint, size, index, current_pattern, patterns):
        """백트래킹을 이용해 가능한 패턴을 모두 탐색."""
        if index == len(hint):
            current_pattern += [0] * (size - len(current_pattern))  # 남은 공간은 모두 0으로
            patterns.append(current_pattern)
            return

        max_start = size - sum(hint[index:]) - (len(hint) - index - 1)
        for start in range(len(current_pattern), max_start + 1):
            new_pattern = current_pattern + [0] * (start - len(current_pattern)) + [1] * hint[index]
            if len(new_pattern) < size:
                new_pattern.append(0)  # 블록 사이에는 0이 필요
            self.backtrack_patterns(hint, size, index + 1, new_pattern, patterns)

    def update_gui(self, grid):
        """해결된 그리드를 GUI에 반영."""
        for row in range(self.size):
            for col in range(self.size):
                if grid[row][col] == 1:
                    self.set_cell_color(row, col, "blue")  # 입력해야 하는 칸은 파란색
                elif grid[row][col] == 0:
                    self.set_cell_color(row, col, "black")  # 입력되면 안 되는 칸은 검정색
                else:
                    self.set_cell_color(row, col, "white")  # 아직 정보가 없는 칸은 하얀색

    def set_board_size(self):
        """사용자가 입력한 크기로 보드를 조정."""
        try:
            new_size = int(self.size_entry.get())
            if new_size < 1:
                raise ValueError
            self.size = new_size
            self.create_input_boxes()
            self.create_clickable_grid()
        except ValueError:
            messagebox.showerror("오류", "올바른 숫자를 입력하세요.")

    def create_buttons(self):
        """퍼즐 해결 및 초기화 버튼을 생성."""
        solve_button = tk.Button(self.root, text="풀기", command=self.solve_puzzle, font=("Arial", 14), bg="#4CAF50", fg="white")
        solve_button.grid(row=3, column=1, pady=10)

        clear_button = tk.Button(self.root, text="초기화", command=self.clear_board, font=("Arial", 14), bg="#f44336", fg="white")
        clear_button.grid(row=3, column=2, pady=10)

        size_button = tk.Button(self.root, text="크기 설정", command=self.set_board_size, font=("Arial", 14), bg="#2196F3", fg="white")
        size_button.grid(row=0, column=2, padx=5, pady=5)

    def clear_board(self):
        """입력창과 클릭 가능한 셀을 초기화."""
        for hint in self.row_hints + self.col_hints:
            hint.delete(0, 'end')

        for cell in self.cells.values():
            cell.config(bg="white")

# 메인 실행 부분
if __name__ == "__main__":
    root = tk.Tk()
    gui = PicrossGUI(root)  # 원하는 기본 크기 설정 가능 (예: 5x5)
    root.mainloop()
