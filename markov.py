import random
import collections

import random
import collections

class MarkovChainGenerator:
    """
    Класс для работы с цепями Маркова.
    Поддерживает два режима: равномерный и вероятностный.
    """

    def __init__(self, mode='probabilistic'):
        """
        Инициализация генератора.

        Параметры:
        mode (str): Режим работы:
                   'uniform' - равномерное распределение
                   'probabilistic' - с учётом частот
        """
        self.mode = mode
        self.chain = None
        self.chain_size = None

    def train(self, text, chain_size=2):
        """
        Обучает цепь Маркова на тексте.

        Параметры:
        text (str): Текст для обучения
        chain_size (int): Длина цепочки
        """
        words = text.split()
        self.chain_size = chain_size

        if self.mode == 'uniform':
            self.chain = collections.defaultdict(list)
            for i in range(len(words) - chain_size):
                key = tuple(words[i:i + chain_size])
                next_word = words[i + chain_size]
                self.chain[key].append(next_word)

        else:  # probabilistic mode
            freq_chain = collections.defaultdict(lambda: collections.defaultdict(int))
            for i in range(len(words) - chain_size):
                key = tuple(words[i:i + chain_size])
                next_word = words[i + chain_size]
                freq_chain[key][next_word] += 1

            # Преобразуем частоты в удобный для выборки формат
            self.chain = {}
            for key, word_counts in freq_chain.items():
                # Создаём список, где слова повторяются пропорционально частоте
                weighted_list = []
                for word, count in word_counts.items():
                    weighted_list.extend([word] * count)
                self.chain[key] = weighted_list

        # Преобразуем defaultdict в обычный dict для ясности
        self.chain = dict(self.chain)

    def generate(self, length=50, seed=None):
        """
        Генерирует текст.

        Параметры:
        length (int): Длина текста в словах
        seed (int): Seed для random (для воспроизводимости)

        Возвращает:
        str: Сгенерированный текст
        """
        if seed is not None:
            random.seed(seed)

        if not self.chain:
            return "Обучите модель перед генерацией!"

        # Выбираем случайную начальную цепочку
        start_key = random.choice(list(self.chain.keys()))
        key = list(start_key)
        result = key.copy()

        for _ in range(length - self.chain_size):
            possible_next_words = self.chain.get(tuple(key))
            if not possible_next_words:
                break

            # Выбираем следующее слово
            if self.mode == 'uniform' and isinstance(possible_next_words, list):
                # Убираем дубликаты для равномерного распределения
                unique_words = list(set(possible_next_words))
                next_word = random.choice(unique_words)
            else:
                # Для вероятностного режима или если список уже с весами
                next_word = random.choice(possible_next_words)

            result.append(next_word)
            key = key[1:] + [next_word]

        return ' '.join(result)

    def get_stats(self):
        """Возвращает статистику по обученной цепи."""
        if not self.chain:
            return "Модель не обучена."

        total_keys = len(self.chain)
        total_transitions = sum(len(words) for words in self.chain.values())

        stats = f"""
        Статистика цепи Маркова:
        - Режим: {self.mode}
        - Размер цепочки (N): {self.chain_size}
        - Уникальных ключей: {total_keys}
        - Всего переходов: {total_transitions}
        - Среднее количество вариантов на ключ: {total_transitions / total_keys:.1f}
        """
        return stats
        
def read_text(filename):
    """Читает текст из файла."""
    with open(filename, 'r', encoding='utf-8') as f:
        text = f.read()
    return text
    
# ==== ИЗМЕНЯЕМ ЭТИ ПАРАМЕТРЫ ====
TRAIN_FILES = [
    'gete.txt',
    'geyne.txt',
    'okudzhava.txt',
    'cvetaeva.txt',
    'ahmatova.txt',
    'blok.txt',
    'mayakovskiy.txt',
    'pushkin.txt',
    'lermontov.txt',
    'tutchev.txt'
]
CHAIN_SIZE = 2            # Длина цепочки
TEXT_LENGTH = 30          # Сколько слов сгенерировать
# ================================

training_text = ""
for filename in TRAIN_FILES:
  training_text += read_text(filename)

markov_chain = MarkovChainGenerator(mode='probalistic')
markov_chain.train(text=training_text, chain_size=CHAIN_SIZE)

#print(markov_chain.get_stats())

generated_text = markov_chain.generate(length=TEXT_LENGTH)
print(generated_text)