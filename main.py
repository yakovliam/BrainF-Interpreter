#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
BrainFuck Interpreter written in python
Default memory buffer of 1000
"""

import sys

### global initialization
# the program's memory buffer
buffer = [0] * 1000

# the code that will be interpreted
code = ""
with open('code.txt', 'r') as file:
    code = file.read().replace('\n', '')

# the data pointer of the buffer
pointer = 0
# the read position in the original code
position = 0
# a map of braces that need to be kept track of for loops
brace_map = []


### functions
# interpret the code
def interpret(code):
    global position

    # break down the operation character by character

    list_code = list(code)

    # split into characters and evaluate for braces (and log the position)
    evaluate_braces(list_code)

    # now, take the split characters and execute
    position = 0
    while position <= len(list_code) - 1:
        char = list_code[position]
        execute(char)
        position += 1


# evaluates position of braces
def evaluate_braces(chars):
    # log temporary position of loop and go through chars
    for temp_pos, char in enumerate(chars, start=0):
        # if opening brace
        if char == '[':
            # log as 1 of a pair
            brace_map.append({'[': temp_pos})
        # if closing brace, find the very last element that is is [ and pair it with it
        if char == ']':
            # find last element in brace map that isn't completed
            for reverse_pos, reverse_elem in reversed(list(enumerate(brace_map))):
                # if not completed
                if '[' in reverse_elem and ']' not in reverse_elem:
                    brace_map[reverse_pos][']'] = temp_pos
                    # now break!
                    break


# executes a command
def execute(command):
    global pointer
    global position
    # increment data pointer
    if command == '>':
        pointer += 1

    # decrement data pointer
    if command == '<':
        pointer -= 1

    # increment data
    if command == '+':
        # if >= 255, then wrap around to 0
        if buffer[pointer] >= 255:
            buffer[pointer] = 0
        else:
            # else increment
            buffer[pointer] += 1

    # decrement data
    if command == '-':
        # if <= 0, then wrap around to 255
        if buffer[pointer] <= 0:
            buffer[pointer] = 255
        else:
            # else decrement
            buffer[pointer] -= 1

    # output byte
    if command == '.':
        sys.stdout.write(chr(buffer[pointer]))

    # input byte
    if command == ',':
        inp = input(":")
        buffer[pointer] = str.encode(inp)[0]  # in case there are multiple characters here, let's just grab the first

    # open brace loop
    if command == '[':
        # if the byte at the data pointer is zero, then instead of moving the instruction pointer forward to the next
        # command, jump it forward to the command after the matching ] command.
        if buffer[pointer] == 0:
            # find the corresponding pointer by looking for the dict with the current position
            new_position = get_corresponding_ending_brace_position(position)

            # if none, that means there was an error with the code
            if new_position is None:
                raise RuntimeError(
                    "There was an error with your code on character " + position + ". Looks like maybe you forgot a "
                                                                                   "closing brace?")
            else:
                # set position
                position = new_position

    # closing brace loop
    if command == ']':
        # if the byte at the data pointer is nonzero, then instead of moving the instruction pointer forward to the
        # next command, jump it back to the command after the matching [ command.
        if buffer[pointer] != 0:
            # find the corresponding pointer by looking for the dict with the current position
            new_position = get_corresponding_opening_brace_position(position)

            # if none, that means there was an error with the code
            if new_position is None:
                raise RuntimeError(
                    "There was an error with your code on character " + position + ". Looks like maybe you forgot an "
                                                                                   "opening brace?")
            else:
                # set position
                position = new_position


def get_corresponding_ending_brace_position(pos):
    global brace_map

    for pair in brace_map:
        # if this '[' has the position 'position'
        if pair['['] == pos:
            return pair[']']

    # if we can't find it, then return none
    return None


def get_corresponding_opening_brace_position(pos):
    global brace_map

    for pair in brace_map:
        # if this ']' has the position 'position'
        if pair[']'] == pos:
            return pair['[']

    # if we can't find it, then return none
    return None


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    interpret(code)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
