from PIL import Image
import math
import os
import unicodedata
import sys

# Usage:
# $python3 ascii_pixels.py [mode] [input] [output]
# modes: t -> text to image, i -> image to text
# example: $python3 t input.txt output.png


color_encode = {'red': [1, 0, 0], 'green': [0, 1, 0], 'blue': [0, 0, 1], 'magenta': [1, 0, 1], 'none': [0, 0, 0]}


def convert_to_image(text_file, save_as='result', size=1, color='none'):
    save_as = save_as.split('.')[0]
    if os.path.isfile(text_file) and text_file[-4:] == '.txt':
        try:
            file = open(text_file, 'r')
            text = file.read()
        except UnicodeError:
            file = open(text_file, encoding='utf8')
            text = unicodedata.normalize('NFKD', file.read()).encode('ascii', 'ignore').decode()
    else:
        text = text_file
    color_list = []
    # Inserting null characters to make the string length a multiple of three
    if len(text) % 3:
        text += '\00' * (3-len(text) % 3)

    c_count = 0
    for i in text:
        color_list.append(ord(i)+color_encode[color][c_count % 3] * 120)
        c_count += 1

    # Grouping every 3 item in a tuple
    color_list = [tuple(color_list[i:i+3]) for i in range(0, len(color_list), 3)]

    # Determining the size of the final image
    largest_square = int(len(color_list)**0.5)
    if (len(color_list)**0.5) % 1:
        largest_square = int(((math.floor(math.sqrt(len(color_list))) + 1)**2)**0.5)

    height = largest_square - ((largest_square**2 - len(color_list))//largest_square)

    img = Image.new('RGB', (largest_square*size, height*size), color=(0, 0, 0))
    pixels = img.load()

    count = 0
    for y in range(largest_square):
        for x in range(largest_square):
            for i in range(size):
                for j in range(size):
                    pixels[size*x+j, size*y+i] = color_list[count]
            count += 1
            if count == len(color_list):
                break
        if count == len(color_list):
            break
    if os.path.isfile(text_file):
        file.close()
    # img.show()
    img.save(save_as + '.png')


def convert_to_text(image_path, save_as, color='none'):
    save_as = save_as.split('.')[0]
    file = open(save_as + '.txt', 'w')
    text = ""
    img = Image.open(image_path)
    width, height = img.size
    count = 0
    for y in range(height):
        for x in range(width):
            for i in img.getpixel((x, y)):
                text += chr(i-120*color_encode[color][count % 3])
                count += 1
    file.write(text)

    file.close()


# def find_text(image_path, save_as):
#     # save_as = save_as.split('.')[0]
#     # file = open(save_as + '.txt', 'w')
#     text = ""
#     img = Image.open(image_path)
#     pixels = img.load()
#     width, height = img.size
#     for y in range(height):
#         for x in range(width):
#             pixels[x,y] = (img.getpixel((x, y))[0]//2, img.getpixel((x, y))[1]//2, img.getpixel((x, y))[2]//2)
#     width, height = img.size
#     for y in range(height):
#         for x in range(width):
#             for i in img.getpixel((x, y)):
#                 text += chr(i)
#
#     dictionary = set(open('words.txt', 'r').read().lower().split())
#     max_len = max(map(len, dictionary))  # longest word in the set of words
#
#     words_found = set()  # set of words found, starts empty
#     for i in range(len(text)):  # for each possible starting position in the corpus
#         chunk = text[i:i + max_len + 1]  # chunk that is the size of the longest word
#         for j in range(1, len(chunk) + 1):  # loop to check each possible subchunk
#             word = chunk[:j]  # subchunk
#             if word in dictionary:  # constant time hash lookup if it's in dictionary
#                 words_found.add(word)  # add to set of words
#
#     print(words_found)


if sys.argv[1] == 't':
    convert_to_image(sys.argv[2], sys.argv[3])

elif sys.argv[1] == 'i':
    convert_to_text(sys.argv[2], sys.argv[3])
