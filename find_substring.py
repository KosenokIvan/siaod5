import time
from knuth_morris_pratt import knuth_morris_pratt
from boyer_moore import boyer_moore


def main():
    string_filename = input("Введите имя файла: ")
    substring = input("Введите шаблон для поиска: ")
    while True:
        case_sensitivity_str = input("Учитывать регистр? [Y/N]: ").lower()
        if case_sensitivity_str == "y":
            case_sensitivity = True
            break
        elif case_sensitivity_str == "n":
            case_sensitivity = False
            break
        else:
            print("Некорректный ввод!")
    with open(string_filename, encoding="utf-8") as file:
        string = file.read()
    measure_time(knuth_morris_pratt, "Алгоритм Кнута-Морриса-Пратта", string, substring, case_sensitivity)
    measure_time(boyer_moore, "Упрощенный алгоритм Бойера-Мура", string, substring, case_sensitivity)
    measure_time(standard_func, "Стандартная функция поиска", string, substring, case_sensitivity)


def standard_func(string, substring, case_sensitivity=True):
    if not case_sensitivity:
        string = string.lower()
        substring = substring.lower()
    try:
        return string.index(substring)
    except ValueError:
        return -1


def measure_time(func, name, *args):
    start_time = time.time()
    print(f"{name}: {func(*args)}")
    print("--- {0} ms ---".format(round((time.time() - start_time) * 1000)))


if __name__ == '__main__':
    main()
