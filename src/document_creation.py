from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement, ns

IMAGE_SCALING = 0.8

def emu_to_twips(emu):
    return int(emu * 1440 / 914400)

def add_preset_page(doc, page_photo_path):
    page = doc.add_paragraph()
    run = page.add_run()
    run.add_picture(coverImage, width=Inches(8))

def add_photo_grid_page(doc, photo_paths, photo_labels):
    section = doc.sections[-1]
    section.top_margin = Inches(0.25)
    section.bottom_margin = Inches(0.5)
    section.left_margin = Inches(0.25)
    section.right_margin = Inches(0.25)

    usable_width = (
        section.page_width
        - section.left_margin
        - section.right_margin
    )

    usable_height = (
        section.page_height
        - section.top_margin
        - section.bottom_margin
    )

    cell_width = usable_width / 3
    cell_height = usable_height / 4

    # Square photo size driven by height
    image_size = min(cell_width, cell_height) * IMAGE_SCALING

    table = doc.add_table(rows=4, cols=3)
    table.autofit = False


    photo_index = 0

    for row in table.rows:
        # Set the row height
        tr = row._tr
        trPr = tr.get_or_add_trPr()
        trHeight = OxmlElement('w:trHeight')
        trHeight.set(ns.qn('w:val'), str(emu_to_twips(cell_height)))
        trHeight.set(ns.qn('w:hRule'), 'exact')
        trPr.append(trHeight)

        for cell in row.cells:
            cell.width = cell_width

            if photo_index < len(photo_paths):
                # --- Photo ---
                p_img = cell.paragraphs[0]
                p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
                p_img.paragraph_format.space_before = 0
                p_img.paragraph_format.space_after = 0

                run = p_img.add_run()
                try:
                    run.add_picture(
                        photo_paths[photo_index],
                        width=image_size
                    )
                except:
                    print(photo_paths[photo_index])

                # --- Name labels ---
                p_label = cell.add_paragraph()
                p_label.alignment = WD_ALIGN_PARAGRAPH.LEFT
                p_label.paragraph_format.space_before = 0
                p_label.paragraph_format.space_after = 0

                label = photo_labels[photo_index].split(", ", maxsplit=1)
                lastname_run = p_label.add_run(label[0])
                lastname_run.font.size = Pt(14)
                lastname_run.font.bold = True
                lastname_run.font.underline = True

                rest_run = p_label.add_run(", "+label[1])
                rest_run.font.size = Pt(12)

                photo_index += 1
