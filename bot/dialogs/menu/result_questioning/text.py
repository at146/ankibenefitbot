from aiogram.utils.text_decorations import html_decoration

FINISH_TEXT = f"""Спасибо за заполнение анкеты!

За участие дарим обещанный подарок ↓↓

"{html_decoration.bold("Пошаговый план роста продаж на 243%: реальный кейс ANKI и 5 шагов для развития бренда весной 2025")}"

А ещё ты можешь подписаться на личный канал Андрея Кима, в котором он делится тонкостями производства, рассказывает об опыте в предпринимательстве и о том, как гореть своим делом сквозь года.
"""

def get_after_5_minutes_text(name: str) -> str:
    return f"""
Статья с планом роста {html_decoration.bold("исчезнет через 24 часа!")}

{name}, сообщаем, если не изучил(а) материал, что осталось всего 24 часа, чтобы забрать пошаговый план роста продаж на 243%!
После этого мы убираем её из открытого доступа.
"""

TEXT_AFTER_23_HOURS = f"""
Закрываем доступ через 1 час!

В статье:
• 5 конкретных шагов, которые увеличили продажи ANKI на 243% 
"""
