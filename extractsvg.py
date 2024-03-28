import os
import xml.etree.ElementTree as ET
import pyperclip

def find_svg_file():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    for filename in os.listdir(current_dir):
        if filename.endswith(".svg"):
            return os.path.join(current_dir, filename)
    return None

def extract_svg_values(svg_file):
    tree = ET.parse(svg_file)
    root = tree.getroot()
    d_value = root.find('.//{http://www.w3.org/2000/svg}path').get('d')
    viewBox_value = root.get('viewBox')
    return d_value, viewBox_value

if __name__ == "__main__":
    svg_file = find_svg_file()
    if svg_file:
        icon_name = input("icon name: ")
        icon_name = icon_name[:1].upper() + icon_name[1:]
        d, viewBox = extract_svg_values(svg_file)
        returnValue = f'export const Svg{icon_name} = forwardRef<SVGSVGElement, SVGProps<SVGSVGElement>>((props, ref: Ref<SVGSVGElement>) => {{\n' \
                        f'\treturn (\n' \
                        f'\t\t<svg ref={{ref}} xmlns="http://www.w3.org/2000/svg" viewBox="{viewBox}" {{...props}}>\n' \
                        f'\t\t\t <path d="{d}" />\n' \
                        f'\t\t</svg>\n' \
                        f'\t);\n' \
                        f'}});'
        print(returnValue)

        print("\n\n Copied to clipboard")
        pyperclip.copy(returnValue)
    else: print("NO SVG file in the directory.")
