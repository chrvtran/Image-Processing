"""
CS 311 Programming Assignment #2 - Python Edition
UMass Amherst 2021 Fall
Instructor: Professor Ramesh Sitaraman

Instructions: Complete the sections marked with # TODO
"""
import math
import numpy as np
from PIL import Image


# --------------------- TODO -------------------------------

# AFTER you implemented the two functions, return here and change
# "sample_image.png" to "InputImage.png" to generate your image
# for part 3, the written section

SAMPLE_IMAGE_PATH = "sample_image.png" # change this to img we want

# --------------------- END TODO ---------------------------


def compute_energy(image: np.ndarray):
    """
    Compute the energy of a given pixel on the image.

    The energy of a pixel in an RGB-channel image is defined as:
        1000, if the pixel is on the edge
        sum([
            delta_xr ** 2,
            delta_xg ** 2,
            delta_xb ** 2,
            delta_yr ** 2,
            delta_yg ** 2,
            delta_yb ** 2,
        ]) ** (1 / 2), otherwise

    Notation: delta_xr indicates the difference in the R channel between
    adjacent pixels in the x (width) direction.

    This is a specific example for an RGB-channel image. Your code
    should work with a 2D image with arbitrary number of channels.

    Input:
        image: int type np.ndarray of the shape:
            (image height, image width, number of color channels)

    Return:
        energy: array of energies of the shape:
            (image_height, image_width)
    """

    # --------------------- TODO -------------------------------
    # Begin your work here
    # initialize np.array to return result
    energy_matrix = np.zeros((image.shape[0],image.shape[1]))

    for row in range(image.shape[0]):
        for col in range(image.shape[1]): 
            energy = 0
            # all border vertex energy = 1000
            if (row == 0 or row == image.shape[0]-1 or col == 0 or col == image.shape[1]-1):
                energy = 1000
                energy_matrix[row][col] = energy
                continue
            # adapted to any # of color channels
            deltas_sqrd = []
            for i in range(image.shape[2]): # number of color channels
                row_delta_sqrd = (image[row-1][col][i] - image[row+1][col][i]) ** 2
                col_delta_sqrd = (image[row][col-1][i] - image[row][col+1][i]) ** 2
                deltas_sqrd.append(row_delta_sqrd)
                deltas_sqrd.append(col_delta_sqrd)
            energy = sum(deltas_sqrd) ** (1/2)
            energy_matrix[row][col] = energy
    return energy_matrix
    # Delete this line after you implemented your algorithm!
    # return np.zeros(image.shape[:-1])

    # --------------------- END TODO ---------------------------


def find_vertical_seam(image: np.ndarray, energy=None):
    """
    Find the vertical "seam" with the least cumulative energy and return
    a list/array of the horizontal indices of the seam

    Input:
        image: int type np.ndarray of the shape:
            (image height, image width, number of color channels)
        energy: double type np.ndarray of the shape:
            (image height, image width)
            used for grading purposes to circumvent energy calculation

    Return:
        An (image height, ) sized array of integers ranging between
        [0, image width - 1]
    """

    # compute energy if not provided.
    if energy is None:
        energy = compute_energy(image)

        # Add a small random noise to the energy, which is generated by
        # an image assumed to contain integer values between [0, 255]
        # (thus may contain many duplicate values), to avoid variations
        # between implementations yielding different results.

        # Storing the internal random state for later reversion
        random_state = np.random.get_state()
        # Seeding the random state to 0
        np.random.seed(0)
        # generating the random noise
        noise = np.random.randn(*energy.shape) / (1000 * (image.size ** (0.5)))
        energy = energy + noise
        # Reverting the random state to what we started with
        np.random.set_state(random_state)

    # --------------------- TODO -------------------------------

    # Adapt an efficient path-finding algorithm to find the seam with the
    # least cumulative energy.
    #
    # The vertical seam of least cumulative energy is defined as:
    #     A (image height, ) sized array of indices in the range
    #     [0, image width - 1], such that each pair of consecutive indices
    #     differ by no more than 1, and such that the sum of the energy on
    #     these pixels is the smallest that can be constructed from such a path
    #
    # This, when visualized on an image, would translate to a squiggly line
    # down an image. Deleting these pixels would yield 2 pieces of image
    # that, when pieced together, would result in an image exactly 1 pixel
    # narrower than the original

    # Nota bene: You shouldn't need to ever use the variable "image"!
    # Everything you need is already computed in the variable "energy".

    # Begin your work here
    prev_row = [] # list tuples (path, cost)
    for row in range(0, energy.shape[0]):
        # dynamic programming for every row
        prev_row = dynamic_lowestcost(row, energy, prev_row)
    
    # Find cheapest path and cost
    lowest_cost = math.inf
    costs = []
    for path,cost in prev_row:
        costs.append(cost)
    costs = np.array(costs)
    min_indices = np.where(costs == costs.min())
    return np.array(prev_row[int(min_indices[0])][0])
    # Delete this line after you implemented your algorithm!
    # return np.zeros(energy.shape[0], dtype=int)
    

    # --------------------- END TODO ---------------------------

def dynamic_lowestcost(row, energy, prev_row):
    # args(row, energy matrix, prev_row)
    # return: list of tuples(path, cost) for accumulated row
    cur_row = []
    if row == 0:
        # initalize first row as its value
        for col in range(0, energy.shape[1]):
            cur_row.append(([col], float(energy[0][col])))
        return cur_row
    else: 
        for col in range(0, energy.shape[1]):
            # for all col, choose best seam
            valid_col = []
            paths = []
            costs = []
            if (col-1 > -1): 
                path,cost = prev_row[col-1]
                valid_col.append(col-1)
                paths.append(path)
                costs.append(cost)
            path,cost = prev_row[col]
            valid_col.append(col)
            paths.append(path)
            costs.append(cost)
            if (col+1 < energy.shape[1]): 
                path,cost = prev_row[col+1]
                valid_col.append(col+1)
                paths.append(path)
                costs.append(cost)
            min_cost = min(costs)
            for i in range(0, len(valid_col)):
                if min_cost == costs[i]:
                    cur_row.append((paths[i]+[col], costs[i]+float(energy[row][col])))
                    break
        return cur_row
    


def find_horizontal_seam(image: np.ndarray, energy=None):
    """
    Find the horizontal "seam" with the least cumulative energy and return
    a list/array of the vertical indices of the seam

    Input:
        image: int type np.ndarray of the shape:
            (image height, image width, number of color channels)
        energy: double type np.ndarray of the shape:
            (image height, image width)
            used for grading purposes to circumvent energy calculation

    Return:
        An (image width, ) sized array of integers ranging between
        [0, image height - 1]
    """

    # this is equivalent to finding the vertical seam on the transposed image
    # so we don't need to repeat ourselves
    return find_vertical_seam(image.transpose(1, 0, 2), energy=energy)


def main():
    """
    Generate a visualization of the energy and 2 visualizations
    of the seam carving algorithm.
    """

    # open image with pillow, an active fork of the defunct PIL library
    p = Image.open(SAMPLE_IMAGE_PATH)
    # image could be other modes like RGBA, YCbCr, or L or something
    p = p.convert(mode="RGB")
    # limit max size
    p.thumbnail(size=(800, 500))
    R, G, B = 0, 1, 2

    # -------------------- energy -------------------------------

    # convert image to an array. Since default datatype for an RGB
    # image is in unsigned 8 bit integer, convert it to a regular int
    # to avoid hard-to-debug shenanigans like over/underflow
    image = np.array(p).astype(int)
    # compute the energy. Since the boundary is 1000 and would reduce
    # the visibility of the more interesting parts after normalization,
    # crop the "frame" to improve visualization
    energy = compute_energy(image)[1:-1, 1:-1]
    # uncomment to see the log-adjusted intensity.
    # energy = np.log(energy + 1)

    # normalization for visualization
    # darken the least value to black
    energy -= np.min(energy)
    # lighten the greatest value to white
    energy = energy / np.max(energy)
    # fit the value between [0, 255]
    energy *= 256
    energy = np.floor(energy)
    energy[energy == 256] = 255

    # convert values to an image
    energy_visualization = Image.fromarray(energy.astype(np.uint8), mode="L")
    energy_visualization.save("energy.png")

    # -------------------- vertical carving ---------------------

    # for an image of shape (height, width, channel)
    # build a visualization by gradually carving axis 1
    image = np.array(p).astype(int)
    original_shape = image.shape

    # sequence of frames to be animated
    sequence = []

    # cap number of seams to carve at 200
    for _ in range(min([200, original_shape[1]])):
        # Create a frame for the seam to be carved away in red
        vertical_indices = tuple(np.arange(image.shape[0]))
        horizontal_indices = tuple(find_vertical_seam(image))
        image[vertical_indices, horizontal_indices, R] = 255
        image[vertical_indices, horizontal_indices, G] = 0
        image[vertical_indices, horizontal_indices, B] = 0

        # append black pixels to make up for pixels carved away
        sequence.append(Image.fromarray(
            np.append(image, np.zeros((
                original_shape[0],
                original_shape[1] - image.shape[1],
                original_shape[2],
            )), axis=1).astype(np.uint8)
        ))

        # carve the seam with a mask and reshape operation
        mask = np.full(image.shape, True, dtype=bool)
        mask[vertical_indices, horizontal_indices] = False

        image = image[mask].reshape((
            image.shape[0],
            image.shape[1] - 1,
            image.shape[2]
        ))

        # append black pixels to make up for pixels carved away
        sequence.append(Image.fromarray(
            np.append(image, np.zeros((
                original_shape[0],
                original_shape[1] - image.shape[1],
                original_shape[2],
            )), axis=1).astype(np.uint8)
        ))

    # save the final, carved image
    final_image = Image.fromarray(image.astype(np.uint8))
    final_image.save("vertical_carving_final.png")

    # build GIF
    p.save(
        "vertical_carving.gif",
        save_all=True,
        append_images=sequence,
        # uncomment this line to create infinite looping GIF
        # loop=0,
        # uncomment this line to control the speed of GIF
        # duration=40,
    )

    # -------------------- horizontal carving -------------------

    # for an image of shape (height, width, channel)
    # build a visualization by gradually carving axis 0
    image = np.array(p).astype(int)
    original_shape = image.shape

    # sequence of frames to be animated
    sequence = []

    # cap number of seams to carve at 200
    for _ in range(min([200, original_shape[0]])):
        # Create a frame for the seam to be carved away in red
        vertical_indices = tuple(find_horizontal_seam(image))
        horizontal_indices = tuple(np.arange(image.shape[1]))
        image[vertical_indices, horizontal_indices, R] = 255
        image[vertical_indices, horizontal_indices, G] = 0
        image[vertical_indices, horizontal_indices, B] = 0

        # append black pixels to make up for pixels carved away
        sequence.append(Image.fromarray(
            np.append(image, np.zeros((
                original_shape[0] - image.shape[0],
                original_shape[1],
                original_shape[2],
            )), axis=0).astype(np.uint8)
        ))

        # carve the seam with a mask and reshape operation
        mask = np.full(image.shape, True, dtype=bool)
        mask[vertical_indices, horizontal_indices] = False

        # don't look at me I am hideous
        # (weird hack to make sure that pixels line up right)
        image = image.transpose(1, 0, 2)[mask.transpose(1, 0, 2)].reshape((
            image.shape[1],
            image.shape[0] - 1,
            image.shape[2],
        )).transpose(1, 0, 2)

        # append black pixels to make up for pixels carved away
        sequence.append(Image.fromarray(
            np.append(image, np.zeros((
                original_shape[0] - image.shape[0],
                original_shape[1],
                original_shape[2],
            )), axis=0).astype(np.uint8)
        ))

    # save the final, carved image
    final_image = Image.fromarray(image.astype(np.uint8))
    final_image.save("horizontal_carving_final.png")

    # build GIF
    p.save(
        "horizontal_carving.gif",
        save_all=True,
        append_images=sequence,
        # uncomment this line to create infinite looping GIF
        # loop=0,
        # uncomment this line to control the speed of GIF
        # duration=40,
    )


if __name__ == "__main__":
    main()
