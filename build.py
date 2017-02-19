#!/usr/bin/env python

"""
Copyright (C) 2016 David Boddie <david@boddie.org.uk>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import os, stat, struct, sys
import Image

from palette import get_entries, black, red, green, yellow, blue, magenta, \
                    cyan, white
import UEFfile

version = "0.1"

def system(command):

    if os.system(command):
        sys.exit(1)

palette = {"\x00\x00\x00": 0,
           "\xff\x00\x00": 1,
           "\x00\xff\x00": 2,
           "\xff\xff\x00": 3,
           "\x00\x00\xff": 4,
           "\xff\x00\xff": 5,
           "\x00\xff\xff": 6,
           "\xff\xff\xff": 7,
           "\x80\x80\x80": 8,
           "\xff\x80\x80": 9,
           "\x80\xff\x80": 10,
           "\xff\xff\x80": 11,
           "\x80\x80\xff": 12,
           "\xff\x80\xff": 13,
           "\x80\xff\xff": 14,
           "\xff\xff\xff": 15}

def read_png(path):

    im = Image.open(path).convert("RGB")
    s = im.tostring()
    
    data = []
    a = 0
    
    i = 0
    while i < im.size[1]:
    
        line = []
        
        j = 0
        while j < im.size[0]:
        
            line.append(palette[s[a:a+3]])
            a += 3
            j += 1
        
        i += 1
        data.append(line)
    
    return data

def read_sprite(lines):

    data = ""
    
    # Read 8 rows at a time.
    for row in range(0, len(lines), 8):
    
        width = len(lines[0])
        
        # Read 4 columns at a time.
        for column in range(0, width, 4):
        
            # Read the rows.
            for line in lines[row:row + 8]:
            
                shift = 3
                byte = 0
                for pixel in line[column:column + 4]:
                
                    if pixel == 1:
                        byte = byte | (0x01 << shift)
                    elif pixel == 2:
                        byte = byte | (0x10 << shift)
                    elif pixel == 3:
                        byte = byte | (0x11 << shift)
                    
                    shift -= 1
                
                data += chr(byte)
    
    return data

rainbow_colours = [red, yellow, green, cyan, blue, magenta]

def rainbow(i, colours, s):

    # Each physical colour is used in two adjacent rows.
    c1 = colours[(i/s) % len(colours)]
    c2 = colours[(((i+1)/s) + 1) % len(colours)]
    return [black, c1, c2, white]

if __name__ == "__main__":

    if len(sys.argv) != 1:
    
        sys.stderr.write("Usage: %s\n" % sys.argv[0])
        sys.exit(1)
    
    # Memory map
    code_start = 0x0e00
    
    files = []
    
    # Assemble the files.
    assemble = [("mapscroll2.oph", "mapscroll2.rom")]
    
    code_data = {}
    
    for name, output in assemble:
        if name.endswith(".oph"):
            system("ophis " + name + " -o " + output)
            code = open(output).read()
        elif name.endswith(".dat"):
            code = open(name).read()
        elif name.endswith(".png"):
            code = read_sprite(read_png(name))
        else:
            code = open(name).read().replace("\n", "\r")
        
        code_data[output] = code
    
    # General ROM processing
    
    for src, obj in assemble:
        if not obj.endswith(".rom"):
            files.append((obj, code_start, code_start, code_data[obj]))
    
    # Exit
    sys.exit()
