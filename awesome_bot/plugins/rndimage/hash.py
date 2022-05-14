import time

import cv2
import numpy as np
import os
from PIL import Image

def dHash(image):
    avreage = np.mean(image)
    ans = ""
    #每行前一个像素大于后一个像素为1，相反为0，生成哈希
    for i in range(8):
        for j in range(8):
            if image[i,j] > image[i,j+1]:
                ans+='1'
            else:
                ans+='0'
    return ans

def gif_distance(name1, name2):
    cnt = 0
    try:
        num1 = int(name1[0].split('_')[0])
        hash1 = name1[0].split("_")[1]
        num2 = int(name2[0].split('_')[0])
        hash2 = name2[0].split("_")[1]
    except:
        return -1
    ans = 0
    if num1 < num2:
        ans += num2 - num1
    else:
        ans += num1 - num2
    ans *= 2
    hash1 = str(format(int(hash1, 16), 'b'))
    l = len(hash1)
    for _ in range(64 - l):
        hash1 = '0' + hash1
    hash2 = str(format(int(hash2, 16), 'b'))
    l = len(hash2)
    for _ in range(64 - l):
        hash2 = '0' + hash2
    for k in range(64):
        if hash1[k] != hash2[k]:
            ans += 1
    if ans > 64:
        ans = 64
    return ans

def Hamming_distance(name1: str, name2: str):
    name1 = name1.split('.')
    name2 = name2.split('.')
    if name1[1] == 'gif' and name2[1] == 'gif':
        return gif_distance(name1, name2)
    if name1[1] == 'gif' or name2[1] == 'gif':
        return -1
    if name1[0][:2] != '0x' or name2[0][:2] != '0x':
        return -1
    try:
        hash1 = str(format(int(name1[0], 16), 'b'))
        l = len(hash1)
        for _ in range(64 - l):
            hash1 = '0' + hash1
        hash2 = str(format(int(name2[0], 16), 'b'))
        l = len(hash2)
        for _ in range(64 - l):
            hash2 = '0' + hash2
        num = 0
        for k in range(64):
            if hash1[k] != hash2[k]:
                num += 1
        return num
    except:
        return -1

#nomal 0x....jpg/png/bmp/jpeg
#gif  ..zhenshu.._0x.....gif

def gif_newname(gif_path, dirr, org_name):
    img = Image.open(gif_path)
    img.seek(0)
    img.save(os.path.join(dirr, org_name + '_test.png'))
    l = 1
    try:
        while True:
            img.seek(l)
            l += 1
    except:
        pass
    src = cv2.imread(os.path.join(dirr, org_name + '_test.png'))
    src = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
    src = cv2.resize(src, (9, 8))
    d2 = dHash(src)
    d16 = hex(int(d2, 2))
    new_img = os.path.join(dirr, str(l) + '_' + d16 + '.gif')
    os.remove(os.path.join(dirr, org_name + '_test.png'))
    return new_img, str(l) + '_' + d16 + '.gif'

async def hash_rename(org_img: str, dirr: str, org_name: str, ex: str):
    src = cv2.imread(org_img)
    cnt = 0
    if src is None:
        new_img, new_name = gif_newname(org_img, dirr, org_name)
        os.rename(org_img, new_img)
        return new_name
    src = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
    src = cv2.resize(src, (9, 8))
    d2 = dHash(src)
    d16 = hex(int(d2, 2))
    #d16 = d16[2:]
    new_img = os.path.join(dirr, d16 + ex)
    try:
        os.rename(org_img, new_img)
        return d16 + ex
    except:
        return None

