MODE 2 Vertical Scrolling Demo for the Acorn Electron
=====================================================

This repository contains a demo that shows vertical scrolling of a tiled map
in MODE 2 on the Acorn Electron using a technique similar to that used in
Firetrack, a vertical scrolling shoot 'em up.

Building the Demo
-----------------

The source code is provided in the form of 6502 assembly language suitable for
the Ophis 6502 assembler. Code is assembled to either ROM images or written to
a UEF file that can be used with either an Electron emulator or converted to a
sound file for playback to a real Electron.

The build script requires both Python and the Ophis 6502 assembler to be
installed. The UEFfile module used by the build script is included in this
repository.

To build the examples, enter the directory containing the `build.py` script and
run it:

  ./build.py

If successful, the `game.rom` file should be created, and this can either be
used as a ROM cartridge image in Elkulator or flashed to an EEPROM and used
in a real ROM cartridge.

Running the Demo
----------------

With the ROM installed in either a real or virtual ROM cartridge, it should
be possible to use the *HELP command to get information on how to start the
demo:

  *HELP SCROLL

Typically, it should be sufficient to type

  *SCROLL

to start it.

License
-------

The source code is licensed under the GNU General Public License version 3 or
later. See the COPYING file for more information about this license. A short
version of the license is given below:

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
