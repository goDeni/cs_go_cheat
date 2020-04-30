import win32con
import win32gui

BRUSH = win32gui.CreateSolidBrush(255)


def draw_line(dc: int, start_x: int, start_y: int, end_x: int, end_y: int):
    hpen = win32gui.CreatePen(win32con.PS_SOLID, 2, 255)
    hopen = win32gui.SelectObject(dc, hpen)
    win32gui.MoveToEx(dc, start_x, start_y)
    win32gui.LineTo(dc, end_x, end_y)
    win32gui.DeleteObject(win32gui.SelectObject(dc, hopen))


def draw_filled_rect(dc, x: int, y: int, w: int, h: int):
    win32gui.FillRect(dc, (x, y, x + w, y + h), BRUSH)


def draw_text(dc, text: str, x, y, width: int, height: int):
    win32gui.DrawText(dc, text, len(text), (x, y, x + width, y + height), win32con.DT_LEFT)


def draw_border_box(dc, x: int, y: int, w: int, h: int, thickness: int):
    draw_filled_rect(dc, x, y, w, thickness)
    draw_filled_rect(dc, x, y, thickness, h)
    draw_filled_rect(dc, x + w, y, thickness, h)
    draw_filled_rect(dc, x, y + h, w + thickness, thickness)
