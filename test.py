from sympy import symbols, Poly
import random

x = symbols('x')
p = int(input("Введите простое число p: "))
n = int(input("Введите степень поля n: "))


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


print(generateIrreduciblePoly(n, p))
