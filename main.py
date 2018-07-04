import card_algorithm as ca
from card_sort import card_ranks, straight, get_sorted_list, add_last_card
from card_tools import max_card_from_straight, get_jokers, get_rank

def hand_rank(hand):
    """Возвращает значение определяющее ранг 'руки'"""
    ranks = card_ranks(hand)
    if straight(ranks) and ca.flush(hand, True):
        return (8, ranks, hand)
    elif ca.kind(4, ranks):
        return (7, ca.kind(4, ranks), ca.kind(1, ranks))
    elif ca.kind(3, ranks) and ca.kind(2, ranks, False):
        return (6, ca.kind(3, ranks), ca.kind(2, ranks, False))
    elif ca.flush(hand):
        return (5, ranks)
    elif straight(ranks):
        return (4, ranks)
    elif ca.kind(3, ranks):
        return (3, ca.kind(3, ranks), ranks)
    elif ca.two_pair(ranks):
        return (2, ca.two_pair(ranks), ranks)
    elif ca.kind(2, ranks):
        return (1, ca.kind(2, ranks), ranks)
    else:
        return (0, ranks)

def best_hand(hand):
    jokers = get_jokers(hand)
    # Если джокеры
    if jokers:
        return best_wild_hand(hand)
    try:
        ca.check_cards(hand)
        return best_hand_algorithm(hand)
    except:
        print('Введены ошибочные данные')

def best_wild_hand(hand):
    jokers = get_jokers(hand)
    # Если нет джокеров
    if not jokers: 
        return best_hand(hand)
    try:
        ca.check_cards(hand)
        return best_wild_hand_algorithm(hand)
    except:
        print('Введены ошибочные данные')

def best_hand_algorithm(hand):
    """Из "руки" в 7 карт возвращает лучшую "руку" в 5 карт """
    hand_rank_list = list(hand_rank(hand))
    item = hand_rank_list[0]

    if item in [7, 3, 1]:
        return ca.hand_with_equal(hand, *hand_rank_list)
    if item in [6, 2]:
        return ca.hand_with_two_equals(hand, *hand_rank_list)
    if item in [5, 0]:
        return ca.sorted_hand(hand)
    if item in [8, 4]:
        return ca.ordered_hand(hand, hand_rank_list)
    return

def best_wild_hand_algorithm(hand):
    """best_hand но с джокерами"""
    hand = get_sorted_list(hand)
    ranks, suits = ca.cards_with_joker_data(hand)
    jokers = get_jokers(hand)
    
    main_params = [hand, ranks, suits]

    # Если 4 подряд одной масти => 8
    if ca.flush(hand, True, 3):
        cards = ca.find_five_same_suit(*main_params)
        if cards: return cards 
    # Если пара и 2 джокера => 8
    if len(jokers) == 2 and ca.kind(2, ranks):
        current_rank = get_rank(ca.kind(2, ranks))
        return ca.find_four_same_rank(hand, current_rank, suits)
    # Если 3 одинакового ранга => 7
    if ca.kind(3, ranks):
        rank = get_rank(ca.kind(3, ranks))
        cards = ca.find_four_same_rank(hand, rank, suits)
        if cards: return cards
    # Если две пары => 6
    if ca.two_pair(ranks):
        cards = ca.two_pair_with_joker(*main_params)
        if cards: return cards
    # Если 4 одинаковой масти => 5
    if ca.flush(hand, False, 3):
        cards = ca.five_same_suit(*main_params)
        if cards: return cards
    # Если 3 подряд и 2 джокера => 4
    if len(jokers) == 2 and max_card_from_straight(ranks,2):
        return add_last_card(ca.five_straight_with_joker(*main_params,2))
    # Если 4 подряд => 4
    if max_card_from_straight(ranks,3):
        cards = ca.five_straight_with_joker(*main_params)
        if cards: return cards
    
    # Если пара => 3 or 2
    if ca.kind(2, ranks):
        cards = ca.three_same_rank(*main_params) or ca.two_pairs(*main_params)
        if cards: return cards
    # Ничего
    if len(jokers) == 2:
        return ca.get_three_same_from_one(*main_params)
    
    return ca.one_pair(*main_params)

def test_best_hand():
    print("test_best_hand...")
    assert (sorted(best_hand("6C 7C 8C 9C TC 5C JS".split()))
            == ['6C', '7C', '8C', '9C', 'TC'])
    assert (sorted(best_hand("TD TC TH 7C 7D 8C 8S".split()))
            == ['8C', '8S', 'TC', 'TD', 'TH'])
    assert (sorted(best_hand("JD TC TH 7C 7D 7S 7H".split()))
            == ['7C', '7D', '7H', '7S', 'JD'])
    print('OK')


def test_best_wild_hand():
    print("test_best_wild_hand...")
    assert (sorted(best_wild_hand("6C 7C 8C 9C TC 5C ?B".split()))
            == ['7C', '8C', '9C', 'JC', 'TC'])
    assert (sorted(best_wild_hand("TD TC 5H 5C 7C ?R ?B".split()))
            == ['7C', 'TC', 'TD', 'TH', 'TS'])
    assert (sorted(best_wild_hand("JD TC TH 7C 7D 7S 7H".split()))
            == ['7C', '7D', '7H', '7S', 'JD'])
    print('OK')

if __name__ == '__main__':
    test_best_hand()
    test_best_wild_hand()
