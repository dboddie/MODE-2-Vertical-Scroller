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

from Tools.graphics import encode_palette, read_sprites, read_tiles
from Tools.levels import encode_level, read_levels

import UEFfile

version = "0.1"

def system(command):

    if os.system(command):
        sys.exit(1)

if __name__ == "__main__":

    if len(sys.argv) != 1:
    
        sys.stderr.write("Usage: %s\n" % sys.argv[0])
        sys.exit(1)
    
    # Memory map
    code_start = 0x0e00
    
    # Encode images - these are listed in the Tools.graphics module.
    tile_data = read_tiles()
    sprite_data = read_sprites()
    
    # Encode level data.
    palette_info, level_lines = read_levels("levels/default.levels")
    
    palette_data = encode_palette(palette_info)
    level_data = encode_level(level_lines)
    
    # Assemble the source code.
    system("ophis mapscroll2.oph -o game.rom")
    
    rom_data = open("game.rom").read()
    rom_data += tile_data
    rom_data += sprite_data
    rom_data += palette_data
    rom_data += level_data
    
    open("game.rom", "w").write(rom_data)
    
    # Exit
    sys.exit()
