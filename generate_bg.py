#!/usr/bin/env python3

import os


def main():
    backgrounds = [x for x in os.listdir("backgrounds") if x not in [".", ".."]]

    css = ""
    bg_classes = []
    js = ""
    i = 0

    for bg in backgrounds:
        css += f"""
.bg-{i} {{
    background: url("backgrounds/{bg}");
}}
"""
        bg_classes.append(f"\"bg-{i}\"")
        i += 1

    classes_as_js = ", ".join(bg_classes)
    js = f"""function randomBackground() {{
    var backgrounds = [{classes_as_js}];

    var bg = backgrounds[Math.floor(Math.random() * backgrounds.length)];
    document.getElementsByTagName("body")[0].setAttribute("class", bg);
}}"""

    with open("backgrounds.css", "w") as f:
        f.write(css)
    
    with open("backgrounds.js", "w") as f:
        f.write(js)

if __name__ == "__main__":
    main()
