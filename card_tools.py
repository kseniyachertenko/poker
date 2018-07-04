from itertools import zip_longest

"""Список старших карт и их числовых эквивалентов"""
high_ranks = dict(zip_longest(['T', 'J', 'Q', 'K', 'A', '?'], range(10,16)))

"""Список рангов"""
rank_list = [str(rank) for rank in range(2,11)] + ['T', 'J', 'Q', 'K', 'A']

"""Список мастей"""
suit_list = ['C', 'D', 'S', 'H']

"""Доступные масти для джокеров"""
equal_suits = {
  'B': 'CS',
  'R': 'HD'
}

"""Возвращает числовой эквивалент ранга карты"""
def get_number(rank):
    return int(rank) if rank.isdigit() else high_ranks[rank]

"""Возвращает строковое представление ранга"""
def get_rank(n):
    if n < 10:
        return str(n)
    # Значение из high_ranks
    return [rank for rank, number in high_ranks.items() if number == n][0]

"""Получаем максимальную карту из ранга"""
def max_card_from_straight(ranks, cards_count = 4):
    counter = 0
    for idx in range(1, len(ranks)):
        if ranks[idx - 1] - ranks[idx] == 1:
            counter += 1
            if counter == cards_count:
                return ranks[idx-cards_count]
        else:
            counter = 0
    return False

"""Поиск джокеров в числовой или строковой последовательности"""
def get_jokers(cards):
    return list(filter(lambda card: card == 15 or '?' in card, cards))

"""Доступные масти для всех джокеров"""
def jokers_suit(jokers):
    return ''.join([equal_suits[suit] for [rank, suit] in jokers])