import sys, random, argparse
import numpy as np
import math
import os

from PIL import Image

gscale1 = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. "
gscale2 = "@%#*+=-:. "


def getAverageL(image):
    img = np.array(image)

    w,h = img.shape

    return np.average(img.reshape(w*h))

def convert(file, cols, scale, reso):
    global gscale1, gscale2

    image = Image.open(file).convert('L')

    W,H = image.size[0], image.size[1]

    w = W / cols
    h = w / scale
    rows = int(H/h)

    if cols > W or rows > H:
        print("Image is too small for specified cols!")
        exit(0)

    aimg = []

    for j in range(rows):
        y1 = int(j*h)
        y2 = int((j+1)*h)
 
        # correct last tile
        if j == rows-1:
            y2 = H
 
        # append an empty string
        aimg.append("")
 
        for i in range(cols):
 
            # crop image to tile
            x1 = int(i*w)
            x2 = int((i+1)*w)
 
            # correct last tile
            if i == cols-1:
                x2 = W
 
            # crop image to extract tile
            img = image.crop((x1, y1, x2, y2))
 
            # get average luminance
            avg = int(getAverageL(img))
 
            # look up ascii char
            if reso:
                gsval = gscale1[int((avg*69)/255)]
            else:
                gsval = gscale2[int((avg*9)/255)]
 
            # append ascii char to string
            aimg[j] += gsval
     
    # return txt image
    return aimg

def main():

    descStr = "This program converts an image into ASCII art."
    parser = argparse.ArgumentParser(description=descStr)
    # add expected arguments
    parser.add_argument('--file', dest='imgFile', required=True)
    parser.add_argument('--scale', dest='scale', required=False)
    parser.add_argument('--out', dest='outFile', required=False)
    parser.add_argument('--cols', dest='cols', required=False)
    parser.add_argument('--morelevels',dest='moreLevels',action='store_true')
 
    # parse args
    args = parser.parse_args()
   
    imgFile = args.imgFile
 
    # set output file
    outFile = 'ascii' + imgFile
    if args.outFile:
        outFile = args.outFile
 
    # set scale default as 0.43 which suits
    # a Courier font
    scale = 0.50
    if args.scale:
        scale = float(args.scale)
 
    # set cols
    cols = 200
    if args.cols:
        cols = int(args.cols)
 
    print('generating ASCII art...')
    # convert image to ascii txt
    aimg = convert(imgFile, cols, scale, args.moreLevels)
 
    # open file
    f = open(outFile, 'w')
 
    # write to file
    for row in aimg:
        f.write(row + '\n')
 
    # cleanup
    f.close()
    print("ASCII art written to %s" % outFile)

    base = os.path.splitext(outFile)[0]
    os.rename(outFile, base + '.txt')

if __name__ == '__main__':
    main()



