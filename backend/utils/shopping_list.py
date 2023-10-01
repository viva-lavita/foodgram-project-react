from django.conf import settings
from django.http import HttpResponse
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas


def shopping_list(ingredients: list) -> HttpResponse:
    """Создание PDF-файла с списком покупок."""
    font_size_title = settings.FONT_SIZE_TITLE
    font_size = settings.FONT_SIZE
    indent_x = settings.INDENT_X
    indent_y = settings.INDENT_Y
    line_break_size = settings.LINE_BREAK_SIZE
    line_break_size_after_title = settings.LINE_BREAK_SIZE_AFTER_TITLE
    pdfmetrics.registerFont(TTFont('DejaVuSerif', 'DejaVuSerif.ttf', 'UTF-8'))
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = ('attachment; '
                                       'filename="shopping_list.pdf"')
    pdf_canvas = canvas.Canvas(response, pagesize=A4)
    pdf_canvas.setFont('DejaVuSerif', font_size_title)
    pdf_canvas.drawString(indent_x, indent_y, 'Список покупок:')
    indent_y -= line_break_size_after_title
    pdf_canvas.setFont('DejaVuSerif', font_size)
    for ingredient in ingredients:
        ingredient_name = ingredient['ingredient__name']
        measurement_unit = ingredient['ingredient__measurement_unit']
        amount = ingredient['amount']
        pdf_canvas.drawString(
            indent_x,
            indent_y,
            f'{ingredient_name} ({measurement_unit}) - {amount}'
        )
        indent_y -= line_break_size
    pdf_canvas.setTitle('Список покупок')
    pdf_canvas.showPage()
    pdf_canvas.save()
    return response
