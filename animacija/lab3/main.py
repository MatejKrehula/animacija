import numpy as np
from utils import *
from alg_utils import *

def main(): 
    args = parse_arguments()
    set_seed(args.seed)

    size_f, angle_f = get_usable_functions(args.size_f, args.angle_f)
    color_strat_f = get_color_function(args.color_strat)

    height, width = get_width_and_height(args)
    original_image = read_image_from_disk(args.original_path, height, width)
    recreated_image = generate_empty_image(height, width)
 
    fitness_f = get_fitness_f(args.fitness_f)

    for i in range(args.num_iter):
        colors = color_strat_f(args.num_colors, original_image)

        for j in range(args.num_mutations):
            mutated, chromosome = mutation(recreated_image, i, colors, height, width, size_f, angle_f)
            fitness = fitness_f(mutated, original_image)
            if j == 0 or fitness > best_fitness:
                best_fitness = fitness
                best_chromosome = chromosome
                
        if i == 0 or best_fitness > curr_fitness:
            curr_fitness = best_fitness
            draw_chromosome(recreated_image, best_chromosome)

        if args.verbose and i % 50 == 0:
           print(f'{i}: fitness - {curr_fitness}')
           pass

        cv2.imshow('Recreated image', recreated_image)
        if cv2.waitKey(1) == ord('q'):
            cv2.destroyAllWindows()
            break
    
    cv2.imwrite(args.recreated_path, recreated_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

main()