Palette
-------

    Original        XOR Common 0    XOR Back 1    XOR Back 2    XOR Foreground 0
0   Common 0        Common 0
1   Sprite 0        Sprite 0
2   Sprite 1        Sprite 1
3   Sprite 2        Sprite 2
4   Background 0                    Background 0
5   Sprite 0                        Sprite 0
6   Sprite 1                        Sprite 1
7   Sprite 2                        Sprite 2
8   Background 1                                  Background 1
9   Sprite 0                                      Sprite 0
10  Sprite 1                                      Sprite 1
11  Sprite 2                                      Sprite 2
12  Foreground 0                                                Foreground 0
13  Foreground 0                                                Foreground 0
14  Foreground 0                                                Foreground 0
15  Foreground 0                                                Foreground 0


Tiles
-----

64 tiles, each 32 bytes in size, arranged in blocks of 8 for convenient
addressing:

0:  0-7     (256 bytes)
1:  8-15    (256 bytes)
...
7:  56-63   (256 bytes)

Because the tiles take up more than 256 bytes in total, we need a way to
quickly reference a tile, given an index.

  ttt00bbb - t = tile index; b = bank number
