from django.http import HttpResponse


def shopping_list(ingredients):
    shopping_list = 'Список покупок:\n'
    for ingredient in ingredients:
        shopping_list += (
            f'\n{ingredient["ingredient__name"]} '
            f'({ingredient["ingredient__measurement_unit"]}) - '
            f'{ingredient["amount"]}')
    return HttpResponse(
        shopping_list,
        headers={
            'Content-Type': 'text/plain',
            'Content-Disposition': 'attachment; '
                                   'filename="shopping_list.txt"',
        },
    )
