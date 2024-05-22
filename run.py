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
zoom = 4.0
zoom = 0.000000000005
resolution = [1000, 1000]
max_iterations = 1000

sunset = ["#301D7D", "#6A0487", "#A8186E", "#C91853", "#F2541B", "#ffbf15"]
ocean = ["#0072ff", "#00c6ff", "#61c0bf", "#abd3c9", "#ffedbc", "#ff5722"]
forest = ["#004d00", "#007a33", "#00b359", "#00e680", "#4dff4d", "#99ff99"]
desert = ["#331800", "#994d00", "#cc6600", "#ff9933", "#ffcc66", "#ffed99"]
arctic = ["#000033", "#003399", "#0066cc", "#0099ff", "#00ccff", "#66ffff"]
sunrise = ["#ffcc33", "#ff9966", "#ff6666", "#ff3399", "#cc33ff", "#9966ff"]


data = grid_sample(centre, zoom, resolution, mandelbrot, max_iterations, 3)
colours = colour_data(data, max_iterations, sunrise)

save_image(colours, "output.png")
