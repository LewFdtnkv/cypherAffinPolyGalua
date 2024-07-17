from sympy import symbols, Poly

x = symbols('x')

if __name__ != '__main__':
    pass
else:
    def buildGf(p, n, irreducibleFunction=None):
        gfSize = p ** n
        gf = []
        if irreducibleFunction is not None:
            if not isIrreducible(irreducibleFunction, p):
                print("Введенный многочлен не является неприводимым над полем Fp.")
                exit()
        for quotient in range(gfSize):
            element = []
            for _ in range(n):
                remainder = quotient % p
                element.insert(0, remainder)
                quotient //= p
            gf.append(element)
        return gf


    def isIrreducible(f, p):
        irreducible = True
        GF = buildGf(n, p)
        polynomial = Poly(f, x)
        for i in range(p, len(GF)):
            tempArr = ((polynomial % Poly(GF[i], x)).all_coeffs())
            for j in range(len(tempArr)):
                tempArr[j] %= p
            if tempArr.count(0) == len(tempArr):
                irreducible = False
                break
        return irreducible


    p = int(input("Введите простое число p: "))
    n = int(input("Введите степень поля n: "))
    irreducibleFunction = list(
        map(int,
            input(f'Введите коэффициенты неприводимого многочлена степени {n}(если есть) через запятую: ').split(',')))
    irreducibleFunctionPoly = Poly(irreducibleFunction, x)
    gf = buildGf(p, n, irreducibleFunctionPoly)
    print("Элементы поля Галуа:")
    print(gf)
    print(
        f'Из данного списка выберете {p ** n} символов для зашифровки и расшифровки: abcdefghijklmnopqrstuvwxyzабвгдеёжзийклмнопрстуфхцчшщъыьэюя')
    alphabet = input()
    if len(alphabet) > p ** n:
        alphabet = alphabet[:p ** n]
    print(f'Итоговый алфавит для зашифровки: {alphabet}')
    print('Введите коэффициенты аддитивного ключа через запятую:')
    additiveKey = list(map(int, input().split(',')))
    print('Введите коэффициенты мультипликативного ключа через запятую:')
    multiplicativeKey = list(map(int, input().split(',')))
    polyMultiplicativeKey = Poly(multiplicativeKey, x)
    print('Введите текст для зашифровки...')
    inputText = input()
    polyAdditiveKey = Poly(additiveKey, x)
    InverseMultiplicativeKey = []
    for i in range(len(gf)):
        InverseMultiplicativeKey = ((polyMultiplicativeKey * Poly(gf[i], x)) % irreducibleFunctionPoly).all_coeffs()
        for j in range(len(InverseMultiplicativeKey)):
            InverseMultiplicativeKey[j] %= p
        if len(InverseMultiplicativeKey) < (n + 1):
            while len(InverseMultiplicativeKey) != (n + 1):
                InverseMultiplicativeKey.insert(0, 0)
        if InverseMultiplicativeKey == [0] * n + [1]:
            InverseMultiplicativeKey = gf[i]
            break
    print(f'Обратный мультипликативный ключ имеет коэффициенты: {InverseMultiplicativeKey}')


    def encryptCipher(gf, a, b):
        decryptText = ''
        for i in range(len(inputText)):
            if inputText[i].isalpha():
                if inputText[i] not in alphabet:
                    continue
                j = alphabet.index(inputText[i])
                polyAdditiveKey = Poly(b, x)
                polyMultiplicatiVeKey = Poly(a, x)
                symbol = Poly(gf[j], x)
                tempElem = (((polyMultiplicatiVeKey * symbol) + polyAdditiveKey) % irreducibleFunctionPoly).all_coeffs()
                for ind in range(len(tempElem)):
                    tempElem[ind] %= p
                if len(tempElem) != n:
                    while len(tempElem) != n:
                        tempElem.insert(0, 0)
                for elem in range(len(gf)):
                    if tempElem == gf[elem]:
                        decryptText += alphabet[elem]
            else:
                decryptText += inputText[i]
        return decryptText


    print(f'Зашифрованный текст: {encryptCipher(gf, multiplicativeKey, additiveKey)}')


    def decryptCipher(gf, b, a):
        encryptText = ''
        for i in range(len(cypherText)):
            if cypherText[i].isalpha():
                if cypherText[i] not in alphabet:
                    continue
                j = alphabet.index(cypherText[i])
                polyAdditKey = Poly(b, x)
                polyInverseMultiplicativeKey = Poly(InverseMultiplicativeKey, x)
                symbol = Poly(gf[j], x)
                tempElem = (((
                                     symbol - polyAdditKey) * polyInverseMultiplicativeKey) % irreducibleFunctionPoly).all_coeffs()
                for ind in range(len(tempElem)):
                    tempElem[ind] %= p
                if len(tempElem) != n:
                    while len(tempElem) != n:
                        tempElem.insert(0, 0)
                for elem in range(len(gf)):
                    if tempElem == gf[elem]:
                        encryptText += alphabet[elem]
            else:
                encryptText += inputText[i]
        return encryptText


    print('Введите текст для расшифровки')
    cypherText = input()
    InverseMultiplicativeKey = list(
        map(int, input(f'Введите коэффициенты обратного ключа ').split(',')))

    print(f'Расшифрованный текст: {decryptCipher(gf, additiveKey, InverseMultiplicativeKey)}')
