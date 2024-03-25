#!/usr/bin/env python
#-*- coding: utf-8 -*-
#-----------------------------------------------------------------------
# Author: delimitry
#-----------------------------------------------------------------------

import os
import time
import math
import datetime
from asciicanvas import AsciiCanvas


x_scale_ratio = 1.75


def draw_second_hand(ascii_canvas, seconds, length, fill_char):
    """
    Draw second hand
    """
    x0 = int(math.ceil(ascii_canvas.cols / 2.0))
    y0 = int(math.ceil(ascii_canvas.lines / 2.0))
    x1 = x0 + int(math.cos((seconds + 45) * 6 * math.pi / 180) * length * x_scale_ratio)
    y1 = y0 + int(math.sin((seconds + 45) * 6 * math.pi / 180) * length)
    ascii_canvas.add_line(int(x0), int(y0), int(x1), int(y1), fill_char=fill_char)


def draw_minute_hand(ascii_canvas, minutes, length, fill_char):
    """
    Draw minute hand
    """
    x0 = int(math.ceil(ascii_canvas.cols / 2.0))
    y0 = int(math.ceil(ascii_canvas.lines / 2.0))
    x1 = x0 + int(math.cos((minutes + 45) * 6 * math.pi / 180) * length * x_scale_ratio)
    y1 = y0 + int(math.sin((minutes + 45) * 6 * math.pi / 180) * length)
    ascii_canvas.add_line(int(x0), int(y0), int(x1), int(y1), fill_char=fill_char)


def draw_hour_hand(ascii_canvas, hours, minutes, length, fill_char):
    """
    Draw hour hand
    """
    x0 = int(math.ceil(ascii_canvas.cols / 2.0))
    y0 = int(math.ceil(ascii_canvas.lines / 2.0))
    total_hours = hours + minutes / 60.0
    x1 = x0 + int(math.cos((total_hours + 45) * 30 * math.pi / 180) * length * x_scale_ratio)
    y1 = y0 + int(math.sin((total_hours + 45) * 30 * math.pi / 180) * length)
    ascii_canvas.add_line(int(x0), int(y0), int(x1), int(y1), fill_char=fill_char)


def draw_clock_face(ascii_canvas, radius, mark_char):
    """
    Draw clock face with hour and minute marks
    """
    x0 = ascii_canvas.cols // 2
    y0 = ascii_canvas.lines // 2
    # draw marks first
    for mark in range(1, 12 * 5 + 1):
        x1 = x0 + int(math.cos((mark + 45) * 6 * math.pi / 180) * radius * x_scale_ratio)
        y1 = y0 + int(math.sin((mark + 45) * 6 * math.pi / 180) * radius)
        if mark % 5 != 0:
            ascii_canvas.add_text(x1, y1, mark_char)
    # start from 1 because at 0 index - 12 hour
    for mark in range(1, 12 + 1):
        x1 = x0 + int(math.cos((mark + 45) * 30 * math.pi / 180) * radius * x_scale_ratio)
        y1 = y0 + int(math.sin((mark + 45) * 30 * math.pi / 180) * radius)
        ascii_canvas.add_text(x1, y1, '%s' % mark)


def draw_clock(cols, lines):
    """
    Draw clock
    """
    if cols < 25 or lines < 25:
        print('Too little columns/lines for print out the clock!')
        exit()
    # prepare chars
    single_line_border_chars = ('.', '-', '.', '|', ' ', '|', '`', '-', "'")
    second_hand_char = '.'
    minute_hand_char = 'o'
    hour_hand_char = 'O'
    mark_char = '`'
    if os.name == 'nt':
        single_line_border_chars = ('.', '-', '.', '|', ' ', '|', '`', '-', "'")  # ('\xDA', '\xC4', '\xBF', '\xB3', '\x20', '\xB3', '\xC0', '\xC4', '\xD9')
        second_hand_char = '.'  # '\xFA'
        minute_hand_char = 'o'  # '\xF9'
        hour_hand_char = 'O'  # 'o'
        mark_char = '`'  # '\xF9'
    # create ascii canvas for clock and eval vars
    ascii_canvas = AsciiCanvas(cols, lines)
    center_x = int(math.ceil(cols / 2.0))
    center_y = int(math.ceil(lines / 2.0))
    radius = center_y - 5
    second_hand_length = int(radius / 1.17)
    minute_hand_length = int(radius / 1.25)
    hour_hand_length = int(radius / 1.95)
    # add clock region and clock face
    # removed rectangle around clock, uncomment to add it again
    # ascii_canvas.add_rect(5, 3, int(math.floor(cols / 2.0)) * 2 - 9, int(math.floor(lines / 2.0)) * 2 - 5)
    draw_clock_face(ascii_canvas, radius, mark_char)
    now = datetime.datetime.now()
    # add regions with weekday and day if possible
    if center_x > 25:
        left_pos = int(radius * x_scale_ratio) / 2 - 4
        ascii_canvas.add_nine_patch_rect(int(center_x + left_pos), int(center_y - 1), 5, 3, single_line_border_chars)
        ascii_canvas.add_text(int(center_x + left_pos + 1), int(center_y), now.strftime('%a'))
        ascii_canvas.add_nine_patch_rect(int(center_x + left_pos + 5), int(center_y - 1), 4, 3, single_line_border_chars)
        ascii_canvas.add_text(int(center_x + left_pos + 1 + 5), int(center_y), now.strftime('%d'))
    # add clock hands
    draw_second_hand(ascii_canvas, now.second, second_hand_length, fill_char=second_hand_char)
    draw_minute_hand(ascii_canvas, now.minute, minute_hand_length, fill_char=minute_hand_char)
    draw_hour_hand(ascii_canvas, now.hour, now.minute, hour_hand_length, fill_char=hour_hand_char)
    # print out canvas
    ascii_canvas.print_out()


def main():
    lines = 40
    cols = int(lines * x_scale_ratio)
    # set console window size and screen buffer size
    if os.name == 'nt':
        os.system('mode con: cols=%s lines=%s' % (cols + 1, lines + 1))
    while True:
       os.system('cls' if os.name == 'nt' else 'clear')
       draw_clock(cols, lines)
       time.sleep(1)


if __name__ == '__main__':
    main()
