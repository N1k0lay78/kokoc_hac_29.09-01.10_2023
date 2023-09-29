# Приложение для конвертации активности в пожертвования

## Что оно делает

Конвертирует физическую активность сотрудников компании в пожертвования на благотворительность.

## Что надо сделать

Приложение для различных групп физической активности будь-то бег, плаванье, ходьба, езда на велосипеде и др.
Физическая активность конвертируется в деньги на благотворительность.

## TODO: 
- Группировать направления физической активности
- Выставить цену для каждого вида физической активности

## Страницы

- Главная (Лидер борд компаний, топ из всех пользователей, база по использованию)
- Логин/регистрация
- Активности (поиск, выбор, сдача активности)
- Профиль пользователя (графики)
- Лидер борд компании
- Профиль администратора компании (графики)
- Лидер борд компаний
- Профиль администратора платформы (доступ ко всему)

*основной акцент на реализации бизнес логики, остальное понятно как реализовать*

## фронт

### Design

#### references

Тинькофф инвестиции - предоставление данных

#### Цвета

60% -  #FEF6ED<br>
30% -  #50A5B1<br>
10% -  #F1600D<br>
text - #1A265A<br>
`ref: https://ru.pinterest.com/pin/187180928257098351/`

#### Шрифт

Для заголовков Oswald 400/700<br>
`@import url('https://fonts.googleapis.com/css2?family=Oswald:wght@400;700&display=swap');` <br>
`font-family: 'Oswald', sans-serif;` <br>
<br>
Для текста Roboto <br>
`@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&display=swap');` <br>
`font-family: 'Roboto', sans-serif;` <br> <br>

Размеры: 18-32px

#### Отступы

5/10/20/40/80px

#### Скругления

Нет, возможны 50% для акцента

### UI kit

#### Сумма

Сумма за этот месяц + динамика в процентах

- красная если меньше
- серая если так же
- зелёная если больше

#### Графики

Графики за месяц

- Красная жирная - график за текущий месяц
- Серый тонкий - средний график
- Зелёный тонкий - средний график компании

#### Лидер борд

По умолчанию показывает топ 10, есть возможность развернуть топ 50/100<br>
Топ 3 выделяются размером/цветом<br>
Первые 10 мест нумеруются специальными знаками, дальше цифрами<br>
Есть возможность открывать статистику пользователей

### Архитектура

#### Регистрация

- да

#### Физическая активность

- Поиск физической активности по типам, названию
- Отчёт о выполнении упражнения (упражнение, количество) + предложение выполнить другие упражнения, которые дадут бонус

#### Работник компании

- Сколько заработал на благотворительность за месяц + динамика (динамика, за тот же период времени)
- Куда и сколько переводить (в процентах или сумма)
- Графики по группам упражнений + средний график за все месяцы пользователя + средний график всех работников компании
- Лидер борд работников компании и Ваше место в нём

#### Администратор компании

- Доступ к данным работника (открывается его страница)
- Сколько компания потратит на благотворительность + динамика
- График по группам упражнений + средний график других компаний
- Лидер борд компаний и Ваше место в нём

#### Администратор платформы

- Доступ к компаниям и их работникам
- Данные компаний
- Лидер борды

## сервер

что-то

## База данных

### Пользователи

- Обычный пользователь (не подтверждён компанией)
- Авторизованный пользователь (авторизован компанией) *мб их объединим*
- Администратор компании (имеет доступ к статистике всех работников компании)
- Администратор (имеет доступ ко всему, назначает администраторов компаний)

### Физические упражнения

- Группы мышц
- Название упражнения
- Тип (физическое упражнение или набор для тренировок)
- Иконка
- Теги (для велосипеда например: улица, ноги, велосипед)
- Группы в комбинации с которыми будет бонус
- описание для цены (за что дают деньги, например за 1 км на велосипеде)
- Цена

### Лог о выполнении физического упражнения

- Дата (с точностью до дня)
- ID упражнения
- количество (желательно суммировать данные за один день)

*если в один день выполнены упражнения которые дают бонус, то цена за каждую группу увеличивается*


## Идеи

### Упражнения, комбинации и наборы для тренировок

Чем больше групп мышц задействуется тем лучше:<br>
Однотипные упражнение < комбинации на разные группы мышц < наборы для тренировок<br>
Если сделал мало, обычное количество<br>
Если сделал рекомендованное количество немного больше<br>
Если сделал много то поменьше<br>
*зависит от физической подготовки человека*

#### Тренировки по отдельности и комбинирование

- например тренировки для ног в комбинации с тренировками для рук дают больший профит, чем отдельно тренировки для ног или рук, но меньше чем готовые наборы для тренировок
- показывать сколько денег даётся на счёт по благотворительности за отдельный вид упражнений, сколько будут давать в комбинации
- предлагать наборы для тренировок содержащие данное упражнение

#### Наборы для тренировок

- набор (например анжумания, прес качат, и подтягивания) в сумме даёт больше средств на счёт по благотворительности, чем по отдельности И полезен для работника

### Сделать на подобии банковского приложения или приложения для инвестиций:

- Общая сводка, по тому, какую сумму вы набрали в этом месяце и сравнение с предыдущей (например на 10% больше)
- Разбивки по видам физической активности и графики за последний месяц

### Геймификация

- Лидер борд в компании по местам, кто набрал больше всего средств для благотворительности
- Лидер борд компаний по местам, топ компаниям давать бонусы
- Улучшение условий труда

## Критерии оценки

- Желательно развернуть на хостинге
- Реализовать минимум 4 вида активности
- статистика (общая, дашборды, индивидуальная, рейтинги, админка)
- фишки, добавить что-то от себя, мб геймификацию, брендирование