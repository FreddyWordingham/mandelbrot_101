from helpers import grid_sample, colour_data, save_image


def foo(x, y, max_iterations):
    if y < x:
        return max_iterations
    else:
        return 0


def mandelbrot(x, y, max_iterations):
    c = complex(x, y)
    z = 0 + 0j
    for i in range(max_iterations):
        if abs(z) > 2.0:
            return i
        z = z * z + c
    return max_iterations


centre = [-0.768955894, 0.1]
# zoom = 0.000000000000005
zoom = 0.0000000000005
# zoom = 4.0
resolution = [2000, 1000]
max_iterations = 1000

colours = ["#301D7D", "#6A0487", "#A8186E", "#C91853", "#F2541B", "#ffbf15"]


data = grid_sample(centre, zoom, resolution, mandelbrot, max_iterations, 3)
colours = colour_data(data, max_iterations, colours)

save_image(colours, "output.png")
