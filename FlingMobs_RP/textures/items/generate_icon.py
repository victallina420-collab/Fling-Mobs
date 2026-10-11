
import struct
import zlib

SIZE = 32
pixels = [[(0, 0, 0, 0) for x in range(SIZE)]
          for y in range(SIZE)]

def put(x, y, color):
    if 0 <= x < SIZE and 0 <= y < SIZE:
        pixels[y][x] = color

GOLD = (255, 190, 35, 255)
LIGHT_GOLD = (255, 235, 100, 255)
DARK_GOLD = (130, 75, 20, 255)
CYAN = (0, 220, 255, 255)
WHITE = (225, 255, 255, 255)

# Draw a diagonal golden wand.
for i in range(5, 27):
    x = i
    y = 30 - i
    for ox in range(-1, 2):
        put(x + ox, y, DARK_GOLD if ox == -1 else GOLD)
    put(x, y - 1, LIGHT_GOLD)

# Add a glowing cyan crystal at the tip.
for x, y in [(25, 3), (24, 4), (25, 4), (26, 4),
             (24, 5), (25, 5), (26, 5), (25, 6)]:
    put(x, y, CYAN)

put(25, 4, WHITE)

# Add little magical sparkles.
for x, y in [(20, 2), (29, 7), (21, 9), (28, 1)]:
    put(x, y, CYAN)

def chunk(kind, data):
    return (struct.pack(">I", len(data)) + kind + data +
            struct.pack(">I", zlib.crc32(kind + data) & 0xffffffff))

raw = b"".join(
    b"\x00" + b"".join(bytes(pixel) for pixel in row)
    for row in pixels
)

png = (
    b"\x89PNG\r\n\x1a\n"
    + chunk(b"IHDR", struct.pack(">IIBBBBB",
                                 SIZE, SIZE, 8, 6, 0, 0, 0))
    + chunk(b"IDAT", zlib.compress(raw))
    + chunk(b"IEND", b"")
)

with open("fling_wand.png", "wb") as file:
    file.write(png)

print("Fling Wand PNG created!")
