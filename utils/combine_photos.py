from PIL import Image
import os

IMAGE_WIDTH = 612
IMAGE_PADDING = 32

BACKGROUND_WIDTH = 3 * IMAGE_WIDTH + 4 * IMAGE_PADDING

# number of images in row
N_IMAGES = 3

background = Image.new('RGBA', (BACKGROUND_WIDTH, BACKGROUND_WIDTH), (255, 255, 255, 255))

i = 0
j = 0

for root, dirs, files in os.walk('.'):
    for name in files:
        lname = name.lower()

        if (lname.endswith(".jpg") or lname.endswith(".gif") or lname.endswith(".png") and
                not 'out' in lname):
            print lname
            img = Image.open(name, 'r')
            print img.size
            offset = (
                int((IMAGE_PADDING + IMAGE_WIDTH) * i + IMAGE_PADDING),
                int((IMAGE_PADDING + IMAGE_WIDTH) * j + IMAGE_PADDING)
            )
            print i, j
            print offset
            i += 1
            if i > N_IMAGES - 1:
                j += 1
                i = 0
            background.paste(img, offset)

background.save('out.jpg')
