from sympy import symbols, Poly
import random

x = symbols('x')


def buildGF(n, p):
    gfSize = p ** n
    gf = []
    for i in range(gfSize):
        element = []
        quotient = i
        for j in range(n):
            remainder = quotient % p
            element.insert(0, remainder)  # Добавляем элемент в начало массива
            quotient = quotient // p
        gf.append(element)
    return gf


def isIrreducible(f, p):
    irreducible = True
    GF = buildGF(n, p)
    polynomial = Poly(f, x)
    for i in range(p, len(GF)):
        tempArr = ((polynomial % Poly(GF[i], x)).all_coeffs())
        for j in range(len(tempArr)):
            tempArr[j] %= p
        if tempArr.count(0) == len(tempArr):
            irreducible = False
            break
    return irreducible


def transformation(irreducPoly):
    irredPoly = ''
    for i in range(len(irreducPoly)):
        if irreducPoly[i] != 0:
            if len(irreducPoly) - 1 - i != 0:
                irredPoly += f' {irreducPoly[i]}*x^{len(irreducPoly) - 1 - i} '
                irredPoly += '+'
            else:
                irredPoly += f' {irreducPoly[i]}'
    return irredPoly


def generateIrreduciblePoly(n, p):
    irredPoly = ''
    irreduciblePoly = Poly([random.randint(1, p - 1)] + [random.randint(0, p - 1) for _ in range(n)], x)
    if isIrreducible(irreduciblePoly, p):
        irreducPoly = irreduciblePoly.all_coeffs()
        irredPoly = transformation(irreducPoly)

        print(f'Сгенерирован неприводимый многочлен равный: {irredPoly}')
        return irreduciblePoly
    else:
        return generateIrreduciblePoly(n, p)


print('Введите значения чисел p и n:')
p = int(input())
notPrime = True
while notPrime:
    if p == 2:
        notPrime = False
    else:
        for i in range(2, p):
            if p % i == 0:
                print('Введенное число не является простым, попробуйте заново')
                p = int(input())
                break
        notPrime = False

n = int(input())
result = Poly(generateIrreduciblePoly(n, p), x)


def formativePolinom(irreduciblePolin, gf):
    arr1 = []
    arr2 = []
    max1 = 0
    for i in range(p, len(gf)):
        for pow in range(2, len(gf)):
            x1 = (((Poly(gf[i], x) ** pow) % irreduciblePolin).all_coeffs())
            for j in range(len(x1)):
                x1[j] %= p
            if x1 == (n - 1) * [0] + [1]:
                arr1.append(pow)
                arr2.append(gf[i])
                break
    for i in range(len(arr1)):
        if max1 < arr1[i]:
            max1 = arr1[i]
    count = 0
    for i in range(len(arr1)):

        if arr1[i] == len(gf) - 1:
            count += 1
            print(f'Образующий многочлен равен: {count}) {arr2[i]}')


def options():
    print('Введите действие, которое хотите выполнить с многочленами...')
    print('* : Умножение многочлена на многочлен')
    print('+ : Сложение многочленов')
    print('- : Вычитание многочлена из многочлена')
    print('fP : Нахождение образующего многочлена')
    print('gf: Вывод коэффициентов поля Галуа')


options()
option = input()


def recurse():
    print('Если хотите продолжить, то введите 1')
    clientDesire = input()
    if clientDesire == '1':
        options()
        newOption = input()
        action(newOption, result)
    else:
        exit()


def action(option, irreduciblePolinom):
    optionSign = ['+', '*', '-', 'fP', 'gf']
    while option not in optionSign:
        print('Вы ввели неверный оператор, попробуйте заново')
        option = input()
    if option == '+':
        print('Введите коэффициенты 1 многочлена через запятую')
        polinom1 = Poly(list(map(int, input().split(','))), x)
        print('Введите коэффициенты 2 многочлена через запятую')
        polinom2 = Poly(list(map(int, input().split(','))), x)
        PolyresPolinom = ((polinom1 + polinom2) % result).all_coeffs()
        for poly in range(len(PolyresPolinom)):
            PolyresPolinom[poly] %= p
        print(PolyresPolinom)
        recurse()
    elif option == '*':
        print('Введите коэффициенты 1 многочлена через запятую')
        polinom1 = Poly(list(map(int, input().split(','))), x)
        print('Введите коэффициенты 2 многочлена через запятую')
        polinom2 = Poly(list(map(int, input().split(','))), x)
        PolyresPolinom = ((polinom1 * polinom2) % result).all_coeffs()
        for poly in range(len(PolyresPolinom)):
            PolyresPolinom[poly] %= p
        print(PolyresPolinom)
        recurse()
    elif option == 'fP':
        formativePolinom(result, buildGF(n, p))
        recurse()
    elif option == 'gf':
        print('Элементы поля Галуа: ')
        print(buildGF(n, p))
        recurse()


action(option, result)
