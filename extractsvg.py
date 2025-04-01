import os
import json
import xml.etree.ElementTree as ET
import pyperclip
import shutil

CONFIG_FILE = "config.json"

def get_svg_files():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return [os.path.join(current_dir, f) for f in os.listdir(current_dir) if f.endswith(".svg")]

def extract_svg_values(svg_file):
    tree = ET.parse(svg_file)
    root = tree.getroot()
    d_value = root.find('.//{http://www.w3.org/2000/svg}path').get('d')
    viewBox_value = root.get('viewBox')
    return d_value, viewBox_value

def load_config():
    config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), CONFIG_FILE)
    if os.path.exists(config_path):
        with open(config_path, "r") as f:
            return json.load(f)
    return {}

def get_valid_output_path():
    config = load_config()
    output_path = config.get("output_tsx_path")

    if output_path and os.path.isfile(output_path):
        return output_path
    else:
        print("No valid output path configured or file does not exist.")
        print("To enable auto-saving, create config.json like:")
        print('{\n  "output_tsx_path": "C:/path/to/your/component.tsx"\n}\n')
        return None

def append_to_component(content: str, output_path: str):
    if output_path:
        with open(output_path, "a", encoding="utf-8") as f:
            f.write("\n\n" + content)
        print(f"Appended component to {output_path}")

def create_react_component(svg_file, output_path: str):
    file_name = os.path.basename(svg_file)
    icon_name = input(f"icon name for '{file_name}': ")
    icon_name = icon_name[:1].upper() + icon_name[1:]
    d, viewBox = extract_svg_values(svg_file)

    returnValue = f'export const Svg{icon_name} = forwardRef<SVGSVGElement, SVGProps<SVGSVGElement>>((props, ref) => {{\n' \
                  f'\treturn (\n' \
                  f'\t\t<svg ref={{ref}} xmlns="http://www.w3.org/2000/svg" viewBox="{viewBox}" {{...props}}>\n' \
                  f'\t\t\t<path d="{d}" />\n' \
                  f'\t\t</svg>\n' \
                  f'\t);\n' \
                  f'}});'

    print(returnValue)
    pyperclip.copy(returnValue)
    append_to_component(returnValue, output_path)
    print(f"\nCopied '{icon_name}' component to clipboard.\n")

    old_dir = os.path.join(os.path.dirname(svg_file), "old")
    os.makedirs(old_dir, exist_ok=True)
    shutil.move(svg_file, os.path.join(old_dir, file_name))

if __name__ == "__main__":
    output_path = get_valid_output_path()
    svg_files = get_svg_files()

    if svg_files:
        for svg_file in svg_files:
            create_react_component(svg_file, output_path)
    else:
        print("No SVG file in the directory.")
