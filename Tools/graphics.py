"""
Copyright (C) 2017 David Boddie <david@boddie.org.uk>

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

import os
import Image
from palette import get_entries, black, red, green, yellow, blue, magenta, \
                    cyan, white

# Dictionary mapping RGB values from PNG files to logical colours.
palette = {"\x00\x00\x00": 0,
           "\xff\x00\x00": 1,
           "\x00\xff\x00": 2,
           "\xff\xff\x00": 3,
           "\x00\x00\xff": 4,
           "\xff\x00\xff": 8,
           "\x00\xff\xff": 12}

# Bit patterns used to encode the rightmost pixel in each byte of screen memory
# for each logical colour in MODE 2.
bits = [0x00, 0x01, 0x04, 0x05, 0x10, 0x11, 0x14, 0x15,
        0x40, 0x41, 0x44, 0x45, 0x50, 0x51, 0x54, 0x55]

# Define all the sprites included in the game. This is imported by both the
# build script and the editor.
sprites = [
    "blank", "backwall0", "backwall1", "ledge0", "ledge1", "light0", "light1",
    "light2", "ledge2", "backwall2", "backwall3", "backwall4", "backwall5"]
    

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
        
        # Read 2 columns at a time.
        for column in range(0, width, 2):
        
            # Read the rows.
            for line in lines[row:row + 8]:
            
                shift = 1
                byte = 0
                for pixel in line[column:column + 2]:
                
                    byte = byte | (bits[pixel] << shift)
                    shift -= 1
                
                data += chr(byte)
    
    return data

def read_sprites():

    sprite_data = ""
    
    for sprite in sprites:
        sprite_data += read_sprite(read_png(os.path.join("images", sprite) + ".png"))
    
    # Add padding data.
    sprite_data += "\x00" * ((64 - len(sprites)) * 32)
    
    return sprite_data

def encode_palette(palette_info):

    return "".join(map(chr, get_entries(16, palette_info)))
