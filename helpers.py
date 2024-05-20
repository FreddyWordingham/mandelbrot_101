from PIL import Image
from tqdm import tqdm
import numpy as np


def grid_sample(
    centre, zoom, resolution, func, max_iterations, super_samples_per_axis=1
):
    width, height = resolution

    aspect_ratio = width / height

    min_x = centre[0] - (zoom * 0.5)
    max_x = min_x + zoom

    min_y = centre[1] - (zoom * 0.5) / aspect_ratio
    max_y = min_y + zoom / aspect_ratio

    x_values = np.linspace(min_x, max_x, width)
    y_values = np.linspace(min_y, max_y, height)

    x_grid, y_grid = np.meshgrid(x_values, y_values)

    result = np.zeros((height, width))

    if super_samples_per_axis > 1:
        offsets = np.linspace(-0.5, 0.5, super_samples_per_axis + 1)[1:-1]

        for j in tqdm(range(height), desc="Processing rows"):
            for i in range(width):
                samples = []
                for dx in offsets:
                    for dy in offsets:
                        x_sample = (
                            x_grid[j, i]
                            + dx * (x_values[1] - x_values[0]) / super_samples_per_axis
                        )
                        y_sample = (
                            y_grid[j, i]
                            + dy * (y_values[1] - y_values[0]) / super_samples_per_axis
                        )
                        samples.append(func(x_sample, y_sample, max_iterations))
                result[j, i] = np.mean(samples)
    else:
        for j in tqdm(range(height), desc="Processing rows"):
            for i in range(width):
                result[j, i] = func(x_grid[j, i], y_grid[j, i], max_iterations)

    return result


def colour_data(data, max_iterations, colours):
    height, width = data.shape[:2]

    result = np.zeros((height, width, 3), dtype=np.uint8)

    for j in range(height):
        for i in range(width):
            result[height - j - 1, i] = colour_map(data[j, i], max_iterations, colours)

    return result


def save_image(data, filename):
    image = Image.fromarray(data)
    image.save(filename)


def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip("#")
    return [int(hex_color[i : i + 2], 16) for i in (0, 2, 4)]


def interpolate_color(c1, c2, t):
    return [int(a + (b - a) * t) for a, b in zip(c1, c2)]


def colour_map(value, max_iterations, hex_colors):
    if value == max_iterations:
        return hex_to_rgb(hex_colors[-1])

    num_colors = len(hex_colors)
    segment = value / max_iterations * (num_colors - 1)
    i = int(segment)
    t = segment - i

    c1 = hex_to_rgb(hex_colors[i])
    c2 = hex_to_rgb(hex_colors[i + 1])

    return interpolate_color(c1, c2, t)
