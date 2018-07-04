from itertools import chain, groupby

import card_tools as ct

"""Масти, которые можно заменить джокером """
def suits_by_joker(hand):
    return ct.jokers_suit(ct.get_jokers(hand))

# Списки
"""Объединение списков"""
def join_lists(*lists):
    return list(chain(*lists))

"""Добавляем в current_list наибольшую из оставшихся карт"""
def find_last_card(hand, current_list):
    return sort_remain_list(hand, current_list)[0]

"""Список пар [числовое представление, строковое]"""
def get_card_list(hand):
    return [[ct.get_number(item[0]), item] for item in hand]

"""Отсортированный список разности списков"""
def sort_remain_list(hand, current_list):
    return get_sorted_list(list(set(hand) - set(current_list)))

"""Список оставшихся мастей"""
def get_remain_suits(current_suits):
    return list(set(list(ct.suit_list)) - set(current_suits))

"""Сортировка карт по их стоковому значению"""
def get_sorted_list(hand):
    # Список пар [числовое представление, строковое]
    cards_list = get_card_list(hand)
    sorted_list = sorted(cards_list, key = lambda item: item[0], reverse = True)

    return [item[1] for item in sorted_list]

"""Ранги карт масти, встречающейся cards_count раз"""
def cards_by_suit(hand, cards_count):
    return [ct.get_number(rank[0]) for rank in same_suit_list(hand, cards_count)]

"""Поиск 4 одинаковых карт"""
def find_four_cards(hand, current_list):
    return find_last_card(hand, join_lists(current_list, ct.get_jokers(hand)))

"""Возвращает больше min_count карт одной масти"""
def same_suit_list(hand, min_count):
    # Сортировка по масти
    sorted_hand = sorted(hand, key = lambda card: card[1])

    suit_groups = groupby(sorted_hand, lambda card: card[1])
    card_groups = [list(cards) for idx, cards in suit_groups]

    # Ищем группы > min_count
    search_groups = [group for group in card_groups if len(group) > min_count]
    if search_groups:
        return search_groups[0]

"""Проверяет оставшиеся масти на соответствие джокеру"""
def check_suits_by_joker(cards, suits):
    # Масти списка
    current_suits = [suit for rank, suit in cards]
    # Поиск оставшихся мастей
    remain_suits = get_remain_suits(current_suits)
    return [suit for suit in remain_suits if suit in suits]
    
"""Возвращает пару для карты по масти"""
def get_pair_by_suits(card, suits):
    card_suit = list(filter(lambda suit: suit != card[1], suits))
    return card[0] + card_suit[0]


# Ранги
"""Возвращает группы рангов длины n"""
def rank_groups(n, ranks):
    groups = groupby(ranks)
    # Убираем джокеры
    return [idx for idx, group in groups if len(list(group)) >= n and idx != 15]

"""Поиск всех карт ранга n"""
def equal_group(n, hand):
    return list(filter(lambda card: ct.get_rank(n) in card, hand))

"""Максимальный ранг"""
def get_max_rank(cards):
    return ct.get_rank(ct.max_card_from_straight(cards))

"""Возвращает True, если отсортированные ранги формируют последовательность 5ти,
где у 5ти карт ранги идут по порядку (стрит)"""
def straight(ranks):
    return bool(ct.max_card_from_straight(ranks))

"""Возвращает список рангов (его числовой эквивалент),
отсортированный от большего к меньшему"""
def card_ranks(hand):
    card_list = [ct.get_number(rank) for [rank, suit] in hand]
    
    card_list.sort(reverse = True)
    return card_list



"""Поиск места и вставка наибольшей возможной(произвольной) карты"""
def add_last_card(cards):
    max_rank, max_suit = cards[0]
    min_rank, min_suit = cards[-1] 
    max_rank = ct.rank_list.index(max_rank)
    # Если не максимальный ранг
    if len(ct.rank_list) > max_rank:
        return [ct.rank_list[max_rank + 1] + max_suit] + cards
    # Иначе ищем после последовательности
    else:
        min_rank = ct.rank_list.index(min_rank)
        return cards.append(ct.rank_list[min_rank - 1] + min_suit)