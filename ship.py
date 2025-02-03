
class Ship:
    def __init__(self, x: int, y: int, x_indent: int, y_indent: int, length: int):
        self.x = x
        self.y = y
        self.x_indent = x_indent
        self.y_indent = y_indent
        self.len = length
        self.hp = length

    def __repr__(self):
        return f"x = {self.x}, y = {self.y}, x_indent = {self.x_indent}, y_indent = {self.y_indent}, len = {self.len}, hp = {self.hp}"
