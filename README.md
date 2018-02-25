# Игра «Pentix»
Версия 2.0

Автор: Ильющенко Анастасия


## Описание
Данное приложение является реализацией игры «Pentix».
По сути своей игра «Pentix» повторяет логику знакомого каждому тетриса,
но здесь падающие фигуры состоят не из 4 блоков, а из 5.
Следовательно, игра разнообразнее и сложнее.


## Требования
* Python версии не ниже 3.4
* PyQt 5


## Состав
* Графическая версия: `pentix.py`
* Модуль логики игры (модели): `game.py`
* Класс "полотна отрисовки" игры: `board.py`
* Класс: `shapes.py`
* Класс: `pentominoes.py`
* Тесты: `tests.py`
* Класс: `nextWindow.py`


## Графическая версия
Справка по запуску: `python pentix.py --help` или `python pentix.py -h`

Пример запуска на Windows: `python pentix.py`
Пример запуска на Linux: `python3 pentix.py`


## Подробности реализации
Главным модулем игры служит `pentix.py`, в котором находится точка входа (main) и класс главного окна (Pentix).
Логическая модель игры реализована классом Game. В классе Board, который наследует QFrame, происходит отрисовка игры. Также там находится таймер. Класс Shapes отвечает за создание фигур и взаимодейстие с ними (будь то их движение или поворот). Класс Next отображает фигуру, которая появится на поле после текущей.
Таблица результатов хранится в файле "Highscores". При первичном запуске рекорд равен 0 и таблица рекодов пуста.

## Дополнительно
* Посередине поля находится не имеющая ширины пластина, за которую может зацепиться фигура
* Есть окно предпросмотра следующей фигуры
* После удаления n линии скорость падения фигур увеличивается и количество получаемых очков за удаление линии увеличивается на 1 за каждую последующую линию (сейчас n = 3).
* Текущий результат и рекорд показываются на главном окне. Чтобы просмотреть таблицу рекордов, нажмите на пункт меню "Highscores".