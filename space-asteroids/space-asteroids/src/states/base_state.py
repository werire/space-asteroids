"""Інтерфейс який повинен реалізовувати кожен стан гри меню, ігровий процес, кінець гри
Це той самий шаблон станів про який йдеться в критеріях оцінювання
меню ігровий процес та екран завершення гри є повністю окремими об’єктами"""


class BaseState:
    def handle_events(self, events):
        raise NotImplementedError

    def update(self, dt):
        raise NotImplementedError

    def draw(self, surface):
        raise NotImplementedError
