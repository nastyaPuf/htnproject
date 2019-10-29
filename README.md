# Иерархическое планирование поведения, исследовательский проект
В ходе этого проекта моей задачей является реализация алгоритма планирования с прецендентами , основанного на иерархии, для решения пространственных задач на языке Python 3.0.


В папке domain_and_problem у меня расположены домен (В домене описывается всевозможные типы, которые могут принимать участие в задаче планировщика, параметры, примитивные действия, сложные действия, методы) и проблема. (В проблеме описываются конкретные объекты, которые могут участвовать в выполнении плана, начальное состояние и цель, состоящая из действия, которое планировщик должен реализовать)

В папке parser_and_grounder, расположен парсер для проблемы и домена( задача которого извлекать из PDDL файла нужную нам информацию и запись ее в соответствующие объекты Python.) и граундинг (выводит всевозможные комбинации действий и конкретных объектов, описанных в проблеме, если типы этих объектов есть в параметрах данного действия.)

В папке HTM_algorithm находится сам алгоритм, который предоставляет план действий для робота для исходной проблемы и задачи. Также в этой папке находится файл с прецендентами, в который записываются уже построенные планы, чтобы использовать их впоследствии.

Для запуска алгоритма есть main_file, в параметрах к которому нужно ввести файл домена и проблемы.
