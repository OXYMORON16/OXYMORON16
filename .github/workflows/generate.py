import os
import requests
from datetime import datetime
from svgwrite import Drawing
from svgwrite.text import TSpan, TextPath
from svgwrite.path import Path
from PIL import Image

username = "OXYMORON16"
grid_size = 10
grid_width = 53
grid_height = 7
cell_size = 5

response = requests.get(f"https://github.com/users/{username}/contributions")
svg_data = response.text
drawing = Drawing(size=(f"{grid_width * grid_size}px", f"{grid_height * grid_size}px"))

contributions = svg_data.split("<g transform=")[1:]

for y in range(grid_height):
    for x in range(grid_width):
        index = x + y * grid_width
        if index >= len(contributions):
            continue

        contribution = contributions[index]
        count = int(contribution.split('data-count="')[1].split('"')[0])
        color = contribution.split('fill="')[1].split('"')[0]

        if count == 0:
            continue

        center_x = x * grid_size + grid_size / 2
        center_y = y * grid_size + grid_size / 2

        radius = (count * cell_size) / 2
        circumference = 2 * radius * 3.14
        angle = count / sum([int(c.split('data-count="')[1].split('"')[0]) for c in contributions]) * 360

        start_x = center_x + radius
        start_y = center_y

        end_x = center_x + radius
        end_y = center_y

        path = Path(stroke=color, stroke_width=grid_size / 3, fill="none")
        path.push(f"M {start_x},{start_y}")
        path.push_arc(
            rx=radius,
            ry=radius,
            rotation=0,
            arc_flag=int(angle > 180),
            sweep_flag=1,
            to=("{},{}".format(end_x, end_y)),
        )

        drawing.add(path)

image = Image.new("RGB", (grid_width * grid_size, grid_height * grid_size), color="#282828")
drawing.draw(image)

timestamp = datetime.now().strftime("%s")
image_path = os.path.join("images", f"{timestamp}.png")
image.save(image_path)

os.system(f"convert -delay 10 -loop 0 images/*.png images/animation.gif")
os.system(f"convert images/animation.gif -alpha set -background transparent -layers OptimizePlus -set dispose previous -quality 100 github-contribution-grid-snake.gif")
os.remove("images/animation.gif")
