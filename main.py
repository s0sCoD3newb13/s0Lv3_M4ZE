from tkinter import *
from tkinter import messagebox


class Player():
    def __init__(self, canvas, r, c, cell_size):
        self.canvas = canvas
        self.cell_size = cell_size
        self.id = canvas.create_oval(c * cell_size + 5, r * cell_size + 5,
                                     c * cell_size + cell_size - 5, r * cell_size + cell_size - 5,
                                     fill="red", outline="white", tags="player")
        self.r, self.c = r, c
        self.nr, self.nc = r, c
        self.fog = True

    def move(self, direction):
        if direction == 'w':
            self.nr, self.nc = self.r - 1, self.c
        elif direction == 'a':
            self.nr, self.nc = self.r, self.c - 1
        elif direction == 's':
            self.nr, self.nc = self.r + 1, self.c
        elif direction == 'd':
            self.nr, self.nc = self.r, self.c + 1

        if not self.is_collide():
            self.canvas.move(self.id, (self.nc - self.c) * self.cell_size, (self.nr - self.r) * self.cell_size)
            self.r, self.c = self.nr, self.nc
            self.update_fog()

        if maze_map[self.r][self.c] == '3':
            messagebox.showinfo(title="Success!", message="FLAG: O_OOOO_OOO")

    def is_collide(self):
        if not (0 <= self.nr < len(maze_map) and 0 <= self.nc < len(maze_map[0])):
            return True
        if maze_map[self.nr][self.nc] == '0':
            return True
        return False

    def update_fog(self):
        if self.fog:
            for item in self.canvas.find_all():
                tags = self.canvas.gettags(item)
                if "player" in tags or "bg_text" in tags or "goal" in tags:
                    self.canvas.itemconfig(item, state='normal')
                    continue

                coords = self.canvas.coords(item)
                item_c = coords[0] // self.cell_size
                item_r = coords[1] // self.cell_size

                dist = abs(item_r - self.r) + abs(item_c - self.c)

                if dist <= 1:
                    self.canvas.itemconfig(item, state='normal')
                else:
                    self.canvas.itemconfig(item, state='hidden')


def keyEvent(event):
    key = event.char.lower()
    if key in ['w', 'a', 's', 'd']:
        player.move(key)


root = Tk()
root.title("Catch the Flag - High Contrast")
root.resizable(False, False)

raw_map = [
    "111111111111100011111",
    "100000000000100010001",
    "111111100000111010001",
    "010000101110101010001",
    "010111101010101011101",
    "110100001010001010101",
    "100100111011101110101",
    "101111001010100000101",
    "101001001010101111101",
    "101001111010100010001",
    "101001000010100010001",
    "001000011110101011101",
    "101010000000101000001",
    "100010110111101000001",
    "111110011100001111001",
    "001010010111001001001",
    "001010010001111001001",
    "101011110000000001001",
    "101000000000001111001",
    "111111111113000000002"
]

maze_map = [[char for char in line] for line in raw_map]

alphabets = {
    (10, 0): "M", (6, 6): "A", (11, 18): "A", (11, 7): "Z",
    (11, 14): "E", (18, 14): "I", (12, 0): "N", (17, 0): "G"
}

for (r, c), char in alphabets.items():
    maze_map[r][c] = char

rows = len(maze_map)
cols = len(maze_map[0])
cell_size = 35
width, height = cols * cell_size, rows * cell_size

sw, sh = root.winfo_screenwidth(), root.winfo_screenheight()
root.geometry("%dx%d+%d+%d" % (width, height, (sw - width) / 2, (sh - height) / 2))

canvas = Canvas(root, width=width, height=height, bg="white", highlightthickness=0)
canvas.bind("<Key>", keyEvent)
canvas.focus_set()
canvas.pack()

# 배경 텍스트
canvas.create_text(width // 2, height // 2, text="CATCH THE FLAG",
                   font=("Arial", 20, "bold"), fill="#f2f2f2", tags="bg_text")

# 맵 그리기
for r in range(rows):
    for c in range(cols):
        val = maze_map[r][c]
        if val != '0':
            # 길 테두리를 선명하게 수정 (outline="black", width=2)
            canvas.create_rectangle(c * cell_size, r * cell_size, c * cell_size + cell_size, r * cell_size + cell_size,
                                    fill="white", outline="black", width=2)

        if val == '2':  # 시작점
            player = Player(canvas, r, c, cell_size)
        elif val == '3':  # 도착점 (테두리 두께 유지)
            canvas.create_rectangle(c * cell_size, r * cell_size, c * cell_size + cell_size, r * cell_size + cell_size,
                                    fill="#0000CD", outline="black", width=3, tags="goal")
        elif val in "MAZEING":
            canvas.create_text(c * cell_size + cell_size // 2, r * cell_size + cell_size // 2,
                               text=val, font=("Arial", 14, "bold"), fill="darkblue")

canvas.tag_lower("bg_text")
player.update_fog()

root.mainloop()