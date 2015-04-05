#!/usr/bin/env python
#-*- coding: utf8 -*-
#-----------------------------------------------------------------------
# Author: delimitry
#-----------------------------------------------------------------------

import time
import math
import datetime
from asciicanvas import AsciiCanvas


def draw_second_hand(ascii_canvas, seconds, length, fill_char):
	"""
	Draw second hand
	"""
	x0 = int(math.ceil(ascii_canvas.cols / 2.0))
	y0 = int(math.ceil(ascii_canvas.lines / 2.0))
	x1 = x0 + int(math.cos((seconds + 45) * 6 * math.pi / 180) * length)
	y1 = y0 + int(math.sin((seconds + 45) * 6 * math.pi / 180) * length)
	ascii_canvas.add_line(x0, y0, x1, y1, fill_char=fill_char)


def draw_minute_hand(ascii_canvas, minutes, length, fill_char):
	"""
	Draw minute hand
	"""
	x0 = int(math.ceil(ascii_canvas.cols / 2.0))
	y0 = int(math.ceil(ascii_canvas.lines / 2.0))
	x1 = x0 + int(math.cos((minutes + 45) * 6 * math.pi / 180) * length)
	y1 = y0 + int(math.sin((minutes + 45) * 6 * math.pi / 180) * length)
	ascii_canvas.add_line(x0, y0, x1, y1, fill_char=fill_char)


def draw_hour_hand(ascii_canvas, hours, minutes, length, fill_char):
	"""
	Draw hour hand
	"""
	x0 = int(math.ceil(ascii_canvas.cols / 2.0))
	y0 = int(math.ceil(ascii_canvas.lines / 2.0))
	total_hours = hours + minutes / 60.0
	x1 = x0 + int(math.cos((total_hours + 45) * 30 * math.pi / 180) * length)
	y1 = y0 + int(math.sin((total_hours + 45) * 30 * math.pi / 180) * length)
	ascii_canvas.add_line(x0, y0, x1, y1, fill_char=fill_char)


def draw_clock_face(ascii_canvas, radius):
	"""
	Draw clock face with hour and minute marks
	"""
	x0 = ascii_canvas.cols / 2
	y0 = ascii_canvas.lines / 2
	# draw marks first
	for mark in xrange(1, 12 * 5 + 1):
		x1 = x0 + int(math.cos((mark + 45) * 6 * math.pi / 180) * radius)
		y1 = y0 + int(math.sin((mark + 45) * 6 * math.pi / 180) * radius)
		if mark % 5 != 0:
			ascii_canvas.add_text(x1, y1, '\xF9')
	# start from 1 because at 0 index - 12 hour
	for mark in xrange(1, 12 + 1):
		x1 = x0 + int(math.cos((mark + 45) * 30 * math.pi / 180) * radius)
		y1 = y0 + int(math.sin((mark + 45) * 30 * math.pi / 180) * radius)
		ascii_canvas.add_text(x1, y1, '%s' % mark)


def draw_clock(cols, lines):
	"""
	Draw clock
	"""
	if cols < 25 or lines < 25:
		print('Too little columns/lines for print out the clock!')
		exit()
	# create ascii canvas for clock and eval vars
	ascii_canvas = AsciiCanvas(cols, lines)
	center_x = int(math.ceil(cols / 2.0))
	center_y = int(math.ceil(lines / 2.0))
	clock_radius = center_x - 5
	second_hand_length = int(clock_radius / 1.17)
	minute_hand_length = int(clock_radius / 1.25)
	hour_hand_length = int(clock_radius / 1.95)
	# add clock region and clock face
	ascii_canvas.add_rect(center_x - clock_radius - 2, center_y - clock_radius - 2, clock_radius * 2 + 5, clock_radius * 2 + 5)
	draw_clock_face(ascii_canvas, clock_radius)
	now = datetime.datetime.now()
	# add regions with weekday and day if possible
	if clock_radius > 12:
		single_line_chars = ('\xDA', '\xC4', '\xBF', '\xB3', '\x20', '\xB3', '\xC0', '\xC4', '\xD9')
		left_pos = clock_radius / 2 - 4
		ascii_canvas.add_rect_nine_patch(center_x + left_pos, center_y - 1, 5, 3, outline_3x3_chars=single_line_chars)
		ascii_canvas.add_text(center_x + left_pos + 1, center_y, now.strftime('%a'))
		ascii_canvas.add_rect_nine_patch(center_x + left_pos + 5, center_y - 1, 4, 3, outline_3x3_chars=single_line_chars)
		ascii_canvas.add_text(center_x + left_pos + 1 + 5, center_y, now.strftime('%d'))
	# add clock hands
	draw_second_hand(ascii_canvas, now.second, second_hand_length, fill_char='\xFA')
	draw_minute_hand(ascii_canvas, now.minute, minute_hand_length, fill_char='\xF9')
	draw_hour_hand(ascii_canvas, now.hour, now.minute, hour_hand_length, fill_char='o')
	# print out canvas
	ascii_canvas.print_out()


def main():
	cols = 50
	lines = cols
	while True:
		draw_clock(cols, lines)
		time.sleep(0.2)


if __name__ == '__main__':
	main()
