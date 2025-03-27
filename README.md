# Морской бой
Это Морской бой, но в нём такие параметры, 
можно редактировать размер поля и количество кораблей.
Есть возможность поиграть с ботом, против друг друга, и даже посмотреть на бой бота против бота
# как скачать игру
1. склонируй репозиторий, или скачай эту программу.
2. У тебя скачан архив. Распакуй его, зайди в папку и открой "main.py"
# Функции
1. задавать размер поля(поле всегда симметричное).
2. задавать разное количество кораблей, с разной длиной:
* добавлено также рекомендованное количество кораблей, чтобы их не было слишком много, или слишком мало.
* при этом добавлены попытки разместить корабли, так как не всегда из возможно с первой попытки разместить
* их количество зависит от размера поля
* можно увеличить количество попыток в коде.
3. играть с ботами разных сложностей:
* лёгкая: выстрел в случайные клетки
* средняя: выстрелы всё ещё случайны, но добавлен алгоритм добивания кораблей
* высокая: высчитывается самая вероятная клетка нахождения корабля и выстреливается в эту клетку. 
При попадании в корабль, он добивается по алгоритму из среднего уровня сложности.
4. играть друг с другом
5. посмотреть на бой бота против бота:
* В консоли сохраняется весь бой, так что можно увидеть последовательно шаги
* можно для разных ботов выбрать разные сложности