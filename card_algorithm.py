from itertools import dropwhile, islice, filterfalse

import card_sort as cs
from card_tools import get_rank, suit_list, max_card_from_straight, get_jokers, rank_list

# Проверка корректности ввода
def check_cards(hand):
    # Правки для джокеров
    ranks = rank_list + ['?']
    suits = suit_list + ['R', 'B']
    # Поиск ошибок
    def check_card(card):
        return card[0] in ranks and card[1] in suits

    if list(filterfalse(check_card, hand)):
        raise Exception('Введены ошибочные данные')


# Без джокеров
"""Поиск карт для ситуаций 7,3,1"""
def hand_with_equal(hand, item, rank, remain_cards):
    current_list = cs.equal_group(rank, hand)
    # Сортировка оставшихся карт и обрезка до нужной длины
    sorted_list = cs.sort_remain_list(hand, current_list)
    sorted_list = islice(sorted_list, 5 - len(current_list))
    # Соединяем списки в один
    return cs.join_lists(current_list, sorted_list)

"""Поиск карт для ситуаций 6,2"""
def hand_with_two_equals(hand, item, card, remain_cards):
    first_card = card if item == 6 else card[0]
    secound_card = remain_cards if item == 6 else card[1]
    # Собираем две известные группы в один список
    current_list = cs.join_lists(cs.equal_group(first_card, hand), cs.equal_group(secound_card, hand))
    # Ищем недостающую карту
    if item == 2:
        current_list.append(cs.find_last_card(hand, current_list))
    return current_list

"""Поиск карт для ситуаций 5,0"""
def sorted_hand(hand):
    return list(islice(cs.get_sorted_list(hand), 5))

"""Поиск карт для ситуаций 8,4"""
def ordered_hand(hand, hand_rank_list, cards_count = 5):
    if len(hand_rank_list) == 3:
        # Получаем все карты искомой масти и сортируем
        cards_list = cs.cards_by_suit(hand, cards_count)
        hand_rank_list[1] = sorted(cards_list, reverse = True)

    max_rank = cs.get_max_rank(hand_rank_list[1])
    # Получение списка карт из интервала
    sorted_hand = cs.get_sorted_list(hand)
    ordered_list = list(dropwhile(lambda card: str(max_rank) not in card, sorted_hand))

    return list(islice(ordered_list, cards_count))


# С джокерами
"""Возвращает ранги и масти, которые может заменить джокер"""
def cards_with_joker_data(hand):
    return [cs.card_ranks(hand), cs.suits_by_joker(hand)]

"""Две пары и джокер"""
def two_pair_with_joker(hand, ranks, suits):
    search_first_rank, search_secound_rank = two_pair(ranks);
    # Объединяем найденные карты
    first_group = cs.equal_group(search_first_rank, hand);
    secound_group = cs.equal_group(search_secound_rank, hand)
    current_list = cs.join_lists(first_group, secound_group)
    # 3 карта для большей по рангу группы
    remain_suit = cs.check_suits_by_joker(first_group, suits)
    if remain_suit:
        current_list.append(first_group[0][0] + remain_suit[0])
        return current_list
    # 3 карта для меньшей по рангу группы
    remain_suit = cs.check_suits_by_joker(secound_group, suits)
    if remain_suit:
        current_list.append(secound_group[0][0] + remain_suit[0])
        return current_list

"""Если 4 подряд одной масти => 8"""
def find_five_same_suit(hand, ranks, suits):
    # Повторяющаяся масть
    equal_suit = cs.same_suit_list(hand, 4)[0][1]
    if equal_suit in suits:
        # Находим известные карты и добавляем недостающую
        return cs.add_last_card(ordered_hand(hand, [8, ranks, hand], 4))

"""Если 3 одинакового ранга => 7"""
def find_four_same_rank(hand, rank, suits):
    # 4 одинаковые карты разных мастей
    current_list = [rank + suit for suit in suit_list]
    current_list.append(cs.find_four_cards(hand, current_list))
    return current_list

"""Если 4 одинаковой масти => 5"""    
def five_same_suit(hand, ranks, suits):
    cards = cs.same_suit_list(hand, 3)
    # Если масть джокера подходит
    if cards[0][1] in suits:
        return cs.add_last_card(cards)

"""Если 4 подряд => 4"""
def five_straight_with_joker(hand, ranks, suits, straight_count = 3):
    max_rank = max_card_from_straight(ranks, straight_count)
    # Получение списка карт из интервала
    sorted_hand = cs.get_sorted_list(hand)
    ordered_list = islice(list(dropwhile(lambda card: get_rank(max_rank) not in card, sorted_hand)), straight_count + 1)

    return cs.add_last_card(list(ordered_list))

"""Если пара => 3"""
def three_same_rank(hand, ranks, suits):
    rank = kind(2, ranks)
    current_cards = cs.equal_group(rank, hand)
    accept_suits = cs.check_suits_by_joker(current_cards, suits)
    # Если масть джокера подходит
    if accept_suits:
        # Карта из джокера
        new_card = current_cards[0][0] + accept_suits[0];
        current_cards.append(new_card)
        # Сортировка оставшихся карт и обрезка до нужной длины
        sorted_list = cs.sort_remain_list(hand, current_cards+ get_jokers(hand))
        return cs.join_lists(current_cards, islice(sorted_list, 2))

"""Если одна пара => 2"""
def two_pairs(hand, ranks, suits):
    rank = kind(2, ranks)
    pair = cs.equal_group(rank, hand)
    # Поиск пары для max
    sorted_list = cs.sort_remain_list(hand, pair+ get_jokers(hand))
    last_card = cs.get_pair_by_suits(sorted_list[0], suits)
    # Возвращаем пару, новую пару и max оставшийся
    return cs.join_lists(pair, sorted_list[:2], [last_card])

"""Если все плохо и ничего нет) => 2"""
def one_pair(hand, ranks, suits):
    joker = get_jokers(hand)
    # Убираем джокеры
    hand = hand[len(joker):]

    max_card = hand[0]
    pair = [cs.get_pair_by_suits(max_card, suits), max_card]

    remain_len = len(joker)+3
    return cs.join_lists(pair, hand[1:remain_len])

"""Поиск 3 одинаковых карт"""
def get_three_same_from_one(hand, ranks, suits):
    # Ищем max карту
    remain_cards = cs.sort_remain_list(hand, get_jokers(hand))
    max_card = remain_cards[0]
    # Ищем еще 2 такого-же ранга
    two_cards = [max_card[0] + suit for suit in suit_list if suit != max_card[1]][:2]
    # Ищем 2 оставшиеся
    return cs.join_lists(two_cards, [max_card], remain_cards[1:3])

# Основные операции
"""Возвращает ранг, который n раз встречается в данной руке.
Возвращает None, если ничего не найдено"""
def kind(n, ranks, is_first = True):
    groups = cs.rank_groups(n, ranks)
    # Выбираем первую или вторую последовательность
    idx = 0 if is_first else 1

    return groups[idx] if len(groups) >= idx + 1 else None

"""Возвращает True, если все карты одной масти"""
def flush(hand, isStraight = False, count = 4):
    # Ищем группы > count карт одной масти
    flush_groups = cs.same_suit_list(hand, count)
    # Если стрит, проверяем на стрит данный диапазон
    if isStraight and flush_groups:
        return cs.straight(cs.card_ranks(flush_groups))

    return bool(flush_groups)

"""Если есть две пары, то возврщает два соответствующих ранга,
иначе возвращает None"""
def two_pair(ranks):
    groups = cs.rank_groups(2, ranks)

    if len(groups) >= 2:
        return list(islice(groups, 2))