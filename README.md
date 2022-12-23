ЗВІТ
Тема проєкту: Аналіз зв'язності графів (5)
Команда 18: Олександра Симко, Олена Азарова, Юрій Сагайдак, Христина Дмитрів, Аліна Бабенко, Юлія Юрга

Нашим завданням було написання бібліотеки для аналізу зв'язності графів. Для цього бібліотека записує графи у словники, ключі яких - вершини графа, а значення ключів - це списки суміжних вершин.

Додаткові функції:
	bfs(graph, start)
	find_cycle(graph, vertex)
	del_edge(graph, edge)

Трохи теорії з дискретної математики:
	Граф називається зв’язним, якщо між кожними двома вершинами існує хоча б один шлях.
	Сильно зв’язний граф — орієнтований граф, для кожної вершини якого існує хоча б один цикл.
	Також ми користувались пошуком вшир. Під час такого алгоритму обходять всі вершини графа, досяжні з початкової, при чому спочатку переглядають всі сусідні вершини, після цього — сусіди сусідів, і так далі.

Детальніше про кожну з функцій:

read_graph(path, directed)
	Дана функція приймає позиційний аргумент path, який вказує шлях до csv-файлу і опціональний арумент directed, який вказує, чи граф орієнтований.  Далі читає інформацію про граф з csv-файлу і повертає словник, в якому: ключі - вершини графа, а значення кожного ключа - це список суміжних вершин.
	Алгоритм: по черзі читаємо рядки файлу, розбиваємо строку по комі й перевіряємо, чи перша вершина є в нашому словнику. Якщо немає, то створюється новий ключ, який буде відповідати першій вершині. Потім друга вершина додається в список значень до ключа першої вершини. Якщо заданий граф — неорієнтований, то до списку значень ключа другої вершини додаємо першу вершину. В кінці повертаємо словник.

write_graph(path, directed)
	Дана функція приймає позиційний аргумент graph, (граф у вигляді словника), позиційний аргумент path (він вказує на шлях до csv-файлу, в який треба записувати) і опціональний арумент directed (який вказує, чи граф орієнтований). Записує графік у файл csv. Якщо directed має значення False, ребра представлені як vert_1 - vert_2 і vert_2 - vert_1  вважаються однаковими і записуються у файл лише один раз.
	Алгоритм: проходимся по кожному значенню для кожного ключа, якщо такої пари вершин ще не було — записуємо в csv-файл.

find_connected_components(graph)
	Функція приймає словник graph (це позиційний аргумент, який репрезентує наш граф). Розбиває граф на зв’язані компоненти.
	Алгоритм: створюємо пустий список, в який будуть записуватися компоненти зв’язності. Далі ітеруємся по всіх вершинах графа та додаємо результат виконання допоміжної функції bfs до списку компонент. Повертає функція список компонентів, представлених найменшими вершинами компонент. 

виклик функції
  ітерування по вершинах графа
    виконання bfs для вершини
    якщо результат bfs ще не зустрічався:
      збереження результату до списку компонент
  повернення списку компонент

Допоміжна функція bfs(graph, start)
	Функція реалізує пошук вшир по графу, починаючи з вершини start.
	Алгоритм: створюємо список list_bfs, куди будемо додавати по черзі вершини, які проходимо, додаємо туди початкову вершину, створюємо список next_key, додаємо туди вершину start. Далі, поки список next_key не пустий: дістаємо звідти елемент з 0 індексом (вершину графа) і видаляємо його, після цього дивимось для всіх, суміжних з нею вершин, чи вони є в  list_bfs, якщо ні — додаємо туди і в  next_key. Повертаємо list_bfs — список вершин, які ми обійшли пошуком вшир, починаючи з заданої вершини.

find_strongly_connected_components(graph)
	Розбиває граф на сильно зв’язні компоненти.
	Приймає словник, в якому: ключі - вершини графа, а значення кожного ключа - це список суміжних вершин.
	Алгоритм: ітерування по вершинах графа -> виконання допоміжної функції find_cycle для вершини, якщо існує цикл з початком у вершині -> збереження результату до списку компонент, видалення вершин, які належать циклу, з списку всіх вершин. Функція повертає список компонент.

виклик функції
  ітерування по вершинах графа
    виконання find_cycle для вершини
    якщо існує цикл з початком у вершині:
      збереження результату до списку компонент
      видалення вершин, які належать циклу, з списку всіх вершин
   повернення списку компонент

Допоміжна функція  find_cycle(graph, vertex)
	Graph - позиційний аргумент, який репрезентує граф, vertex -  позиційний аргумент, який вказує на вершину, з якої має починатися цикл.
	Алгоритм: створюємо список path, в якому будуть зберігатися вершини, що є в одному циклі з вершиною vertex. Створюємо список stack, як відсортований за спаданням список вершин, суміжних з vertex. Далі, поки stack не пустий, беремо останню вершину з нього. Перевіряємо, чи серед суміжних з нею є vertex, якщо так, то цикл вже знайдено і функція повертає його (path, True). Якщо суміжних з нею вершин немає, то видаляємо її з path і продовжуємо пошук з попередньої вершини. Якщо ж в якийсь момент в списку  path залишилась лише vertex, то це означає, що циклу немає і функція поверне ([], False) 

find_connectivity_spots(graph)
  Функція приймає один агрумент, який репрезентує граф. Ідея, яку ми використовували: якщо при вилученні вершини з графа, кількість його компонент збільшується, то це точка сполучення

виклик функції
  ітерування по вершинах графа
    створення копії графа, у якій немає вершини
    перевірка кількості компонент копії
      збереження номеру вершини
  повернення списку точок сполучення
  
find_bridges(graph)
  Ідея, якою ми користувались: якщо при вилученні грані з графа, кількість його компонент зростає, то це міст.
  Дана функція приймає позиційний аргумент graph, який репрезентує граф.

виклик функції
  ітерування по ребрах графа
    створення копії графа, з видаленим ребром
    перевірка кількості компонент копії
      збереження ребра, як моста
повернення списку мостів

  Для видалення ребра з графа ми використовували додаткову функцію del_edge.

Допоміжна функція del_edge(graph, edge)
  Функція приймає словник, який репрезентує граф(graph), та кортеж, елементами якого є кінцеві вершини ребра, яке треба видалити.
   Алгоритм: по черзі перевіряємо, чи кінцеві вершини ребра є у графі, якщо так — видаляємо. 
   
   Враження від виконання завдання: цікавий формат для того, щоб перевірити свої знання з дискретної математики та програмування. Досвід роботи в команді теж дуже важливий для нас
