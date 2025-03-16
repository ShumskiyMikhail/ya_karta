from flask import Flask, request
import requests
from pprint import pprint
from PIL import Image

r = requests.get('https://olimp.miet.ru/ppo_it/api').json()
i = 1

for e in r['message']['data']:
    print(*e, sep='\t')

ans = []

im = Image.new("RGB", (256, 256), (0, 0, 0))
pixels = im.load()

for n1 in range(4):
    ans.append([])
    for n2 in range(4):
        r = requests.get('https://olimp.miet.ru/ppo_it/api').json()['message']['data']
        for i in range(64):
            for j in range(64):
                pixels[n2 * 64 + j, n1 * 64 + i] = r[i][j], r[i][j], r[i][j]

im.save('res.jpg')


