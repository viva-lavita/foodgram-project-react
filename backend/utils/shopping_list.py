from django.http import HttpResponse
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas


def shopping_list(ingredients) -> HttpResponse:
    """Создание PDF-файла с списком покупок."""
    pdfmetrics.registerFont(TTFont('DejaVuSerif', 'DejaVuSerif.ttf', 'UTF-8'))
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = ('attachment; '
                                       'filename="shopping_list.pdf"')
    p = canvas.Canvas(response, pagesize=A4)
    x = 100
    y = 700
    p.setFont("DejaVuSerif", 14)
    p.drawString(x, y, "Список покупок:")
    y -= 20
    p.setFont("DejaVuSerif", 12)
    for ingredient in ingredients:
        ingredient_name = ingredient["ingredient__name"]
        measurement_unit = ingredient["ingredient__measurement_unit"]
        amount = ingredient["amount"]
        p.drawString(
            x, y, f"{ingredient_name} ({measurement_unit}) - {amount}"
        )
        y -= 15
    p.showPage()
    p.save()
    return response
