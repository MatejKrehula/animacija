import numpy as np
from copy import deepcopy
import cv2
 
def calculate_fitness(recreated_image, original_image):
    # -(sqrt((x1 - y1)**2) + sqrt((x2 - y2)**2) + ... + sqrt((xn - yn)**2))
    return -np.sqrt( (recreated_image.astype(np.float32) - original_image)**2 ).sum()

def calculate_alternate_fitness(recreated_image, original_image):
    return  -np.sqrt(  ((recreated_image - original_image)**2).sum() )

def mutation(img, i, colors, height, width, size_f, angle_f):
    lg, lt, s1, s2, angle, c = generate_solution(height, width, colors, i, size_f, angle_f)
    img_copy = deepcopy(img)
    cv2.ellipse(img_copy, (lg, lt), (s1, s2), angle, 0, 360, c, -1)
    return img_copy, (lg, lt, s1, s2, angle, c)

def generate_solution(height, width, colors, i, size_f, angle_f):
    c = colors[np.random.choice(colors.shape[0])]
    angle = angle_f(i)
    lt = np.random.randint(0, height)
    lg = np.random.randint(0, width)
    s1 = size_f(height, i)
    s2 = size_f(width, i)
    return (lg, lt, s1, s2, angle, c.tolist())

def draw_chromosome(recreated_image, chromosome):
    lg, lt, s1, s2, angle, c = chromosome
    cv2.ellipse(recreated_image, (lg, lt), (s1, s2), angle, 0, 360, c, -1)

def get_fitness_f(fitness_f_str):
    return FITNESS_F_DICT[fitness_f_str]

FITNESS_F_DICT = {
    'pixel_neg_rsse': calculate_fitness,
    'img_neg_rsse': calculate_alternate_fitness
}