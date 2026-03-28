from pathlib import Path

from fpdf import FPDF, XPos, YPos

from .fetch_cover import fetch_cover


def make_pdf_card(book_card_data: dict) -> str:
    """
    Create pdf file for book card

    ## Parameters
        **book_card_data**: Dictionnary with book informations

    ## Returns
        File path
    """

    if not isinstance(book_card_data, dict):
        raise TypeError('book_card_data must be dict')

    book_id = book_card_data.get('info', {}).get('id')
    if not isinstance(book_id, int):
        raise ValueError('book_card_data info must include an int id')

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=12)
    pdf.set_left_margin(12)
    pdf.set_right_margin(12)
    pdf.set_top_margin(12)
    pdf.add_page()

    try:
        fetch_cover(book_id, True)
        cover_path = Path(f'alice_assets/covers/cover_{book_id}.png')
        if cover_path.exists():
            pdf.image(str(cover_path), x=12, y=10, w=60)
            pdf.set_y(95)
            pdf.set_x(pdf.l_margin)
    except Exception:
        pdf.ln(10)

    pdf.set_font('Helvetica', size=12)

    def to_latin1(value: object) -> str:
        text = str(value)

        return text.encode('latin-1', errors='replace').decode('latin-1')

    def write_section(title: str, content: object) -> None:
        pdf.set_x(pdf.l_margin)
        pdf.set_font('Helvetica', style='B', size=12)
        pdf.cell(0, 8, to_latin1(title), new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.set_font('Helvetica', size=11)

        if isinstance(content, dict):
            for key, value in content.items():
                pdf.set_x(pdf.l_margin)
                pdf.multi_cell(0, 6, to_latin1(f"{key}: {value}"))
        elif isinstance(content, list):
            for item in content:
                pdf.set_x(pdf.l_margin)
                pdf.multi_cell(0, 6, to_latin1(f"- {item}"))
        else:
            pdf.set_x(pdf.l_margin)
            pdf.multi_cell(0, 6, to_latin1(content))

        pdf.ln(2)

    for section_name, section_data in book_card_data.items():
        write_section(section_name, section_data)

    output_dir = Path('alice_assets/book_cards')
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / f'card_{book_id}.pdf' # overwrite / operator with method __truediv__
    pdf.output(str(output_path))

    return str(output_path)
