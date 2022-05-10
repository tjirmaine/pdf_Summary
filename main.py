import fitz
from webcolors import rgb_to_name
from scipy.spatial import KDTree
from webcolors import (
    CSS3_HEX_TO_NAMES,
    hex_to_rgb,
)


def main():
    doc = fitz.open("sample.pdf")
    print(len(doc))

    page = doc[0]

    highlights = []

    annot = page.firstAnnot
    while annot:
        if annot.type[0] == 8:
            colours = annot.colors
            print(colours)
            if len(colours.get('stroke')) == 3:
                rgb = [round(x * 250) for x in colours.get('stroke')]
                # named_colour = rgb_to_name(rgb, spec='css3')
                named_colour = convert_rgb_to_names(rgb)
                print(named_colour)
            all_coordinates = annot.vertices
            if len(all_coordinates) == 4:
                highlight_coord = fitz.Quad(all_coordinates).rect
                highlights.append(highlight_coord)
            else:
                all_coordinates = [all_coordinates[x:x + 4] for x in
                                   range(0, len(all_coordinates), 4)]
                for i in range(0, len(all_coordinates)):
                    coord = fitz.Quad(all_coordinates[i]).rect
                    highlights.append(coord)
        annot = annot.next

    all_words = page.get_text_words()

    # List to store all the highlighted texts
    highlight_text = []
    for h in highlights:
        sentence = [w[4] for w in all_words if fitz.Rect(w[0:4]).intersect(h)]
        highlight_text.append(" ".join(sentence))

    print(highlight_text)


def convert_rgb_to_names(rgb_tuple):
    # a dictionary of all the hex and their respective names in css3
    css3_db = CSS3_HEX_TO_NAMES
    names = []
    rgb_values = []
    for color_hex, color_name in css3_db.items():
        names.append(color_name)
        rgb_values.append(hex_to_rgb(color_hex))

    kdt_db = KDTree(rgb_values)
    distance, index = kdt_db.query(rgb_tuple)
    return names[index]


if __name__ == "__main__":
    main()
