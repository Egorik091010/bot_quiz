from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

class SPORT:
    SPORTS = ["Футбол", "Баскетбол", "Тенис", "Бег", "Плаванье","Хоккей","Бокс","Гандбол","Волейбол","Водное поло","Гольф","Пинг-понг"]

    def __init__(self, text,*options):
        self.__text = text
        self.options = options

    @property
    def text(self):
        return self.__text

    def gen_markup(self):
        markup = InlineKeyboardMarkup()
        markup.row_width = len(self.options)

        for option in self.options:
            markup.add(InlineKeyboardButton(option, callback_data=option))

        markup.add(InlineKeyboardButton("✅ Done", callback_data="done"))
        return markup
    
