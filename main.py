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
    # List to store all the highlighted texts
    highlight_text = []
    for pageNumber in range(0, len(doc)):
        page = doc[pageNumber]
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
                highlights.append((annot.rect, named_colour))
            annot = annot.next
        #
        all_words = page.get_text_words()
        for h in highlights:
            sentence = []
            for word in all_words:
                if fitz.Rect(word[0:4]).intersects(h[0]):
                    if not sentence:
                        first_word_number = word[7]
                    sentence.append(word[4])
                    last_word_number = word[7]
            highlight_text.append((" ".join(sentence), h[1], first_word_number, last_word_number))
    print_text(highlight_text)


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


def print_text(highlighted_text):
    with open('output.txt', 'w') as output:
        for sentence in highlighted_text:
            colour = sentence[1]
            if colour == 'khaki':
                output.write("-" + sentence[0] + " " + str(sentence[2]) + " " + str(sentence[3]) + "\n")
            elif colour == 'tomato':
                output.write("   -" + sentence[0] + " " + str(sentence[2]) + " " + str(sentence[3]) + "\n")
            elif colour == 'plum':
                output.write("       -" + sentence[0] + " " + str(sentence[2]) + " " + str(sentence[3]) + "\n")

# def sort_notes(highlighted_text):
#     for sentence in highlighted_text:




if __name__ == "__main__":
    main()
