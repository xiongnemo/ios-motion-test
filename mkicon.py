#!/usr/bin/env python3
"""The icon of MotionTest as the PNGs its Info.plist names (no asset catalog: actool is a Mac program): a cube, its
three faces in three shades, with an orbit around it -- the back of the orbit behind the cube, the front over it --
on an indigo to teal gradient. SpringBoard rounds the corners itself.
usage: python3 -I mkicon.py APP_DIR"""
import math
import os
import struct
import sys
import zlib

TOP, BOTTOM = (0x3a, 0x2f, 0x9e), (0x12, 0x86, 0xb8)
ORBIT = (0xff, 0xc8, 0x3c)
SS = 4      # samples per pixel along each side

CX, CY, R = 0.5, 0.52, 0.27                 # the cube's centre (where its three faces meet) and size
C30 = math.cos(math.pi / 6)
T, B = (CX, CY - R), (CX, CY + R)
UR, LR = (CX + R * C30, CY - R / 2), (CX + R * C30, CY + R / 2)
UL, LL = (CX - R * C30, CY - R / 2), (CX - R * C30, CY + R / 2)
FACES = (((T, UR, (CX, CY), UL), 1.00),     # the top, lit
         ((UL, (CX, CY), B, LL), 0.80),     # the left
         ((UR, LR, B, (CX, CY)), 0.58))     # the right, in shadow
TILT = math.radians(-18)


def inside(p, poly):
    """a point in a convex polygon, its corners clockwise on the screen (y down)"""
    for (ax, ay), (bx, by) in zip(poly, poly[1:] + poly[:1]):
        if (bx - ax) * (p[1] - ay) - (by - ay) * (p[0] - ax) < 0:
            return False
    return True


def orbit(u, v):
    """None, or whether the point is on the orbit's front half"""
    du, dv = u - CX, v - CY
    x = du * math.cos(TILT) - dv * math.sin(TILT)
    y = du * math.sin(TILT) + dv * math.cos(TILT)
    f = math.hypot(x / 0.43, y / 0.15)
    if 0.90 <= f <= 1.0:
        return y > 0
    return None


def color(u, v, bg):
    o = orbit(u, v)
    if o is True:
        return ORBIT
    for poly, light in FACES:
        if inside((u, v), poly):
            return tuple(round(255 * light) for _ in range(3))
    if o is False:
        return ORBIT
    return bg


def png(size):
    rows = []
    for y in range(size):
        row = bytearray([0])
        bg = [round(a + (b - a) * y / (size - 1)) for a, b in zip(TOP, BOTTOM)]
        for x in range(size):
            total = [0, 0, 0]
            for i in range(SS):
                for j in range(SS):
                    c = color((x + (i + 0.5) / SS) / size, (y + (j + 0.5) / SS) / size, bg)
                    total = [t + k for t, k in zip(total, c)]
            row += bytes(round(t / (SS * SS)) for t in total)
        rows.append(bytes(row))

    def chunk(kind, data):
        return struct.pack('>I', len(data)) + kind + data + struct.pack('>I', zlib.crc32(kind + data))
    return (b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR', struct.pack('>IIBBBBB', size, size, 8, 2, 0, 0, 0)) +
            chunk(b'IDAT', zlib.compress(b''.join(rows), 9)) + chunk(b'IEND', b''))


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    for scale in (2, 3):
        with open(os.path.join(sys.argv[1], 'AppIcon60x60@%dx.png' % scale), 'wb') as f:
            f.write(png(60 * scale))


main()
