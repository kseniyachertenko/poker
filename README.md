# Poker

## Функция best_hand
принимает на вход покерную "руку" (hand) из 7ми карт и возвращает лучшую (относительно значения, возвращаемого hand_rank) "руку" из 5ти карт. У каждой карты есть масть(suit) и ранг(rank)

### Масти: трефы(clubs, C), пики(spades, S), червы(hearts, H), бубны(diamonds, D)
### Ранги: 2, 3, 4, 5, 6, 7, 8, 9, 10 (ten, T), валет (jack, J), дама (queen, Q), король (king, K), туз (ace, A)
### Например: AS - туз пик (ace of spades), TH - дестяка черв (ten of hearts), 3C - тройка треф (three of clubs)

## Функция best_wild_hand
принимает на вход покерную "руку" (hand) из 7ми карт и возвращает лучшую (относительно значения, возвращаемого hand_rank) "руку" из 5ти карт. Кроме прочего в данном варианте "рука" может включать джокера. Джокеры могут заменить карту любой масти и ранга того же цвета, в колоде два джокерва.

* Черный джокер '?B' может быть использован в качестве трефили пик любого ранга. 
* Красный джокер '?R' - в качестве черв и бубен любого ранга.


## Запуск тестов
```
$ python main.py
```