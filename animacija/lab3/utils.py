import argparse
import numpy as np
import cv2
import imagesize

ANGLE_F_STR1 = 'np.random.randint(0, 360)'
ANGLE_F_STR2 = '0'
ANGLE_F_STR3 = 'np.random.randint(175, 185)'

SIZE_F_STR1 = 'np.random.randint(1, 10)'
SIZE_F_STR2 = '3'
SIZE_F_STR3 = 'np.abs(np.random.normal(0, 2)).astype(np.uint8)'
SIZE_F_STR4 = 'np.random.randint(0, (dim // (np.log10((i**6)+20))))'

KMEANS_CACHE = None

COLOR_STRAT_DICT = {
    'kmeans': lambda num_colors, img: generate_colors_k_means(num_colors, img),
    'random': lambda num_colors, img: generate_colors_random(num_colors, img)
}

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--width', type=int, default=None)
    parser.add_argument('--height', type=int, default=None)
    parser.add_argument('--original_path', type=str, default='./images/baltazar.jpg')
    parser.add_argument('--recreated_path', type=str, default='./recreated/baltazar_recreated.jpg')

    parser.add_argument('--angle_f', type=str, default=ANGLE_F_STR1, help='Expression that determines the angle defined between [0, 360] of the ellipse drawn and uses variables or i or no variable.')
    parser.add_argument('--size_f', type=str, default=SIZE_F_STR4, help='Expression that determines the size of the ellipse drawn and uses variables dim and i or neither.')
    parser.add_argument('--fitness_f', type=str, default='pixel_neg_rsse', help='One of \'img_neg_rsse\' or \'pixel_neg_rsse\'. \'img_neg_rsse\' works better with lighter pictures, \'pixel_neg_rsse\' with darker pictures.')
    parser.add_argument('--color_strat', type=str, default='kmeans')
    parser.add_argument('--num_colors', type=int, default=17)
    
    parser.add_argument('--num_iter', type=int, default=1000)
    parser.add_argument('--num_mutations', type=int, default=100)

    parser.add_argument('--verbose', type=bool, default=True)

    parser.add_argument('--seed', type=int, default=42)

    args = parser.parse_args()
    return args

def get_color_function(color_strat_str):
    return COLOR_STRAT_DICT[color_strat_str]

def get_usable_functions(size_f, angle_f):
    return eval(f'lambda dim, i: {size_f}'), eval(f'lambda i: {angle_f}')

def read_image_from_disk(path, height, width):
    img = cv2.imread(path)
    img = cv2.resize(img, (width, height), interpolation=cv2.INTER_CUBIC)
    return img

def generate_colors_k_means(num_colors, img):
    global KMEANS_CACHE
    if KMEANS_CACHE is not None:
        return KMEANS_CACHE
    img_reshaped = img.reshape((-1,3))
    img_reshaped = np.float32(img_reshaped)
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    _, _, center = cv2.kmeans(img_reshaped, num_colors, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
    KMEANS_CACHE = np.uint8(center)
    return KMEANS_CACHE

def generate_colors_random(num_colors, img):
    return np.random.randint(0, 255, size=(num_colors, 3)).astype(np.uint8)

def generate_empty_image(height, width):
    return np.full(shape=(height, width, 3),fill_value=255, dtype=np.uint8)

def get_width_and_height(args):
    if args.width is None and args.height is None:
        w, h = imagesize.get(args.original_path)
        args.width = w
        args.height = h
    return h, w

def set_seed(seed):
    if seed is not None:
        np.random.seed(seed)
        cv2.setRNGSeed(seed)
