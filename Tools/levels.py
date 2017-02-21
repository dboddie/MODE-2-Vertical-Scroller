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

def read_levels(file_name):

    lines = open(file_name).readlines()
    palette_text = lines.pop(0) + lines.pop(0)
    palette_info = []
    
    for rgb in palette_text.split():
        r, g, b = map(int, rgb.split(","))
        palette_info.append((r, g, b))
    
    i = 0
    while i < len(lines):
        lines[i] = map(int, lines[i].strip().split())
        i += 1
    
    return palette_info, lines

def encode_level(lines):

    level_data = ""
    
    lines.reverse()
    
    for line in lines:
    
        line.reverse()
        
        for tile in line:
            bank = tile / 32
            index = tile % 32
            level_data += chr((index * 32) | bank)
    
    return level_data
