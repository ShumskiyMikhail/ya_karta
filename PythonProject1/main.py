from flask import Flask, request
import requests
from pprint import pprint
from PIL import Image

def corners(sp):
    f1 = 0
    f2 = 0
    f3 = 0
    f4 = 0
    for i in range(4):
        for j in range(4):
            if sp[i][j][63][63] == 255 and sp[i][j][0][0] == 255 and sp[i][j][63][0] == 255 and f3 == 0:
                sp[i][j], sp[3][0] = sp[3][0], sp[i][j]
                f3 = 1

            if sp[i][j][63][63] == 255 and sp[i][j][0][0] == 255 and sp[i][j][0][63] == 255 and f2 == 0:
                sp[i][j], sp[0][3] = sp[0][3], sp[i][j]
                f2 = 1

            if sp[i][j][63][0] == 255 and sp[i][j][0][0] == 255 and sp[i][j][0][63] == 255 and f1 == 0:
                sp[i][j], sp[0][0] = sp[0][0], sp[i][j]
                f1 = 0

            if sp[i][j][63][63] == 255 and sp[i][j][63][0] == 255 and sp[i][j][0][63] ==  255 and f4 == 0:
                sp[i][j], sp[3][3] = sp[3][3], sp[i][j]
                f4 = 0
    return sp

def left(sp):
    l = 0
    for i in range(4):
        for j in range(4):
            if (i, j) != (0, 0) and (i, j) != (3, 0) and (i, j) != (0, 3) and (i, j) != (3, 3):
                if sp[i][j][32][0] == 255:
                    if l == 0:
                        sp[i][j], sp[1][0] = sp[1][0], sp[i][j]
                        l = 1
                    if l == 1:
                        sp[i][j], sp[2][0] = sp[2][0], sp[i][j]
                        return sp
    return sp

def right(sp):
    r = 0
    for i in range(4):
        for j in range(1, 4):
            if (i, j) != (0, 0) and (i, j) != (3, 0) and (i, j) != (0, 3) and (i, j) != (3, 3):
                if sp[i][j][32][63] == 255:
                    if r == 0:
                        sp[i][j], sp[1][3] = sp[1][3], sp[i][j]
                        r = 1
                    else:
                        sp[i][j], sp[2][3] = sp[2][3], sp[i][j]
                        return sp
    return sp

def top(sp):
    t = 0
    for i in range(4):
        for j in range(1, 3):
            if (i, j) != (0, 0) and (i, j) != (3, 0) and (i, j) != (0, 3) and (i, j) != (3, 3):
                if sp[i][j][0][32] == 255:
                    if t == 0:
                        sp[i][j], sp[0][1] = sp[0][1], sp[i][j]
                        t = 1
                    else:
                        sp[i][j], sp[0][2] = sp[0][2], sp[i][j]
                        return sp
    return sp

def bottom(sp):
    b = 0
    for i in range(1, 4):
        for j in range(1, 3):
            if (i, j) != (0, 0) and (i, j) != (3, 0) and (i, j) != (0, 3) and (i, j) != (3, 3):
                if sp[i][j][63][32] == 255:
                    if b == 0:
                        sp[i][j], sp[3][1] = sp[3][1], sp[i][j]
                        b = 1
                    else:
                        sp[i][j], sp[3][2] = sp[3][2], sp[i][j]
                        return sp
    return sp



ans = []

while len(ans) < 16:
    s = (requests.get('https://olimp.miet.ru/ppo_it/api').json()['message']['data'])
    if s not in ans:
        ans.append(s)

an = []

for i in range(4):
    an.append([])
    for j in range(4):
        an[i].append(ans[i * 4 + j])

print(an)

ans = corners(an)
ans = left(ans)
ans = right(ans)
ans = top(ans)
ans = bottom(ans)

im = Image.new("RGB", (256, 256), (0, 0, 0))
pixels = im.load()

for n1 in range(4):
    ans.append([])
    for n2 in range(4):
        r = ans[n1][n2]
        for i in range(64):
            for j in range(64):
                pixels[n2 * 64 + j, n1 * 64 + i] = r[i][j], r[i][j], r[i][j]

im.save('res.jpg')