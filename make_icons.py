"""
PWA 아이콘 생성 — pillow 없이 순수 Python으로 PNG 생성
실행: python make_icons.py
"""
import struct, zlib, math

def png(size):
    bg = (212, 133, 10)   # --accent 색
    fg = (255, 255, 255)

    pixels = []
    cx = cy = size / 2
    r_outer = size * 0.42
    r_inner = size * 0.10

    for y in range(size):
        row = []
        for x in range(size):
            dx, dy = x - cx, y - cy
            dist = math.hypot(dx, dy)

            # 둥근 배경
            corner_r = size * 0.22
            in_bg = (x >= corner_r and x <= size - corner_r and
                     y >= corner_r and y <= size - corner_r)
            if not in_bg:
                # 모서리 둥글게
                nx = max(corner_r - x, x - (size - corner_r), 0)
                ny = max(corner_r - y, y - (size - corner_r), 0)
                in_bg = math.hypot(nx, ny) <= corner_r

            if not in_bg:
                row.extend([0, 0, 0, 0])
                continue

            # 책 모양 아이콘 (단순 사각형 3개)
            bw = size * 0.08
            bh = size * 0.38
            gap = size * 0.04
            total_w = 3 * bw + 2 * gap
            bx = cx - total_w / 2
            by = cy - bh / 2 + size * 0.02

            in_icon = False
            for i in range(3):
                x1 = bx + i * (bw + gap)
                x2 = x1 + bw
                if x1 <= x <= x2 and by <= y <= by + bh:
                    in_icon = True
                    break
            # 책 상단 가로선
            lh = size * 0.025
            lw = total_w
            lx = cx - lw / 2
            ly = by - lh - size * 0.03
            if lx <= x <= lx + lw and ly <= y <= ly + lh:
                in_icon = True

            if in_icon:
                row.extend([*fg, 255])
            else:
                row.extend([*bg, 255])
        pixels.append(row)

    def chunk(name, data):
        c = struct.pack('>I', len(data)) + name + data
        return c + struct.pack('>I', zlib.crc32(name + data) & 0xffffffff)

    raw = b''
    for row in pixels:
        raw += b'\x00' + bytes(row)

    ihdr = struct.pack('>IIBBBBB', size, size, 8, 6, 0, 0, 0)
    idat = zlib.compress(raw, 9)

    return (b'\x89PNG\r\n\x1a\n' +
            chunk(b'IHDR', ihdr) +
            chunk(b'IDAT', idat) +
            chunk(b'IEND', b''))

for sz, name in [(192, 'icon-192.png'), (512, 'icon-512.png')]:
    with open(name, 'wb') as f:
        f.write(png(sz))
    print(f'  생성 완료: {name}')

print('아이콘 생성 완료!')
