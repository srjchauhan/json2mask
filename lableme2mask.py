import os
import json
import pprint
from PIL import Image, ImageDraw

savedir = 'data/mask'
fgcolor = (255, 255, 255)
bgcolor = (0, 0, 0)
polygons = []


def generateImage(filename, preview=False, save=True):
    img = Image.new('RGB', (imageWidth, imageHeight), bgcolor)
    pixels = img.load()
    draw = ImageDraw.Draw(img)
    for polygon in polygons:
        draw.polygon(polygon, fill=fgcolor)
    if preview:
        print('Opening preview')
        img.show()
    if save:
        print('Saving image ' + filename)
        img.save(str(os.path.join(savedir, filename)))


def parseJSON(file):
    global polygons, numFound, filename, imageWidth, imageHeight
    with open(file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    imageHeight = data['imageHeight']
    imageWidth = data['imageWidth']
    for shape in data['shapes']:
        points = []
        for point in shape['points']:
            x = point[0]
            y = point[1]
            points.append((float(x), float(y)))
        polygons.append(points)


def run_from_dir(json_path='data/json', img_path='data/image'):
    image_list = [os.path.splitext(path)[0] for path in os.listdir(img_path)]
    for file in os.listdir(json_path):
        if os.path.splitext(file)[0] in image_list:
            parseJSON(os.path.join(json_path, file))
            generateImage(os.path.splitext(file)[0] + '.jpg')


if __name__ == "__main__":
    run_from_dir()
