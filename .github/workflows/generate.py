import os
import requests
from datetime import datetime
from svgwrite import Drawing
from svgwrite.text import TSpan, TextPath
from svgwrite.path import Path
from PIL import Image

username = "your_github_username"
grid_size = 10
grid_width = 53
grid_height = 7
cell_size = 5

response = requests.get(f"https://github.com/users/{username}/contributions")
svg_data = response.text
drawing = Drawing(size=(f"{grid_width * grid_size}px", f"{grid_height * grid_size}px"))

with open("README.md", "r") as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if "github-contribution-grid-snake.svg" in line:
        lines[i] = f"![snake gif](https://github.com/{username}/{username}/blob/output/github-contribution-grid-snake.gif)\n"
        break

with open("README.md", "w") as f:
    f.writelines(lines)

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
        angle = count / sum([c !=
