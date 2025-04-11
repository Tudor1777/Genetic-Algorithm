import random
import math
import matplotlib.pyplot as plt


def generarePopulatie(a, b, nrCromozomi, prec):
    populatie = []
    nr = (b - a) * (10**prec)
    l = math.ceil(math.log2(nr))
    for i in range(nrCromozomi):
        crom = ''.join(random.choice('01') for j in range(l))
        populatie.append(crom)
    return populatie, l


def decodificare(crom, a, b, prec):
    l = len(crom)
    crom10 = int(crom, 2)
    crom = ((b - a) * crom10) / (2**l - 1) + a
    return round(crom, prec)


def functie(x, grad, coef):
    y = 0
    g = grad
    for c in coef:
        y += c * (x ** g)
        g -= 1
    return y
# print(functie(2, 4, 1, 1, 1, 1, 1))


def performantaTotala(pop, a, b, prec, grad, coef):
    F = 0
    for crom in pop:
        crom = decodificare(crom, a, b, prec)
        F += functie(crom, grad, coef)
    return F


def probabilitateIndivid(crom, grad,  coef, perftotal, a, b, prec):
    crom = decodificare(crom, a, b, prec)
    return functie(crom, grad, coef)/perftotal


def selectie(pop, a, b, prec, grad, coef, bestIndex, file = None, primaEtapa = False):
    perftotal = performantaTotala(pop, a, b, prec, grad, coef)
    probabilitati = [probabilitateIndivid(crom, grad, coef, perftotal, a, b, prec) for crom in pop]
    q = [0] *len(pop)
    q[0] = probabilitati[0]
    if file and primaEtapa:
        file.write(f'{q[0]}')
    for i in range(1, len(probabilitati)):
        q[i] = q[i - 1] + probabilitati[i]
        if file and primaEtapa:
            file.write(f' {q[i]}')
    pop_interm = [pop[bestIndex]]
    j = bestIndex
    for i in range(len(pop)):
        u = random.random()
        st, dr = 0, len(q) - 1
        while st <= dr:
            p = (st + dr) // 2
            if q[p] <= u <= q[p + 1]:
                j = p
                break
            elif u > q[p]:
                st = p + 1
            else:
                dr = p - 1
        if j != bestIndex:
            pop_interm.append(pop[j])
            if file and primaEtapa:
                file.write(f'u = {u} selectam cromozomul ')
                file.write(f'{j + 1} \n')
    return pop_interm


def incrucisare(pop, pc, l,  file = None, primaEtapa = False):
    marcat = [0] * len(pop)
    if file and primaEtapa:
        file.write(f'1: {pop[0]} Nu participa(are fitness maxim)\n')
    for i in range(1, len(pop)):
        u = random.random()
        if file and primaEtapa:
            file.write(f'{i + 1}: {pop[i]} u = {u}')
        if u < pc:
            marcat[i] = 1
            if file and primaEtapa:
                file.write(f'<{pc} participa la incrucisare \n')
        else:
            if file and primaEtapa:
                file.write('\n')
    for i in range(1, len(pop)):
        if marcat[i] == 1:
            for j in range(i + 1, len(pop)):
                if marcat[j] == 1:
                    t = random.randrange(0, l - 2)
                    # print(t)
                    c1, c2 = pop[i], pop[j]
                    c3 = c1[:t + 1] + c2[t + 1:]
                    c4 = c2[:t + 1] + c1[t + 1:]
                    pop[i], pop[j] = c3, c4
                    marcat[i] = marcat[j] = 0
                    if file and primaEtapa:
                        file.write(f'Incrucisare intre cromozomul {i + 1} cu cromozomul {j + 1}:\n{c1} {c2}, taiere la {t}\nRezultat {c3} {c4}\n')
                    break
    # print(pop)
    return pop


def mutatie(pop, pm,  file = None, primaEtapa = False):
    pop_noua = [pop[0]]
    for i in range(1, len(pop)):
        crom = list(pop[i])
        flag = 0
        for j in range(len(crom)):
            u = random.random()
            if u < pm:
                flag = 1
                if crom[j] == '0':
                    crom[j] = '1'
                else:
                    crom[j] = '0'
        pop_noua.append(''.join(crom))
        if flag and file and primaEtapa:
            file.write(f'{i + 1}\n')
    return pop_noua


def grafic(maxim):
    generatii = list(range(len(maxim)))
    plt.figure(figsize=(10, 5))
    plt.plot(generatii, maxim, label='Fitness maxim', color='green')
    plt.title('Evoluția fitness-ului in timp')
    plt.xlabel('Generatie')
    plt.ylabel('Valoare fitness')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()


f = open("alg_genetici.in", 'r')
dimPop = int(f.readline())
print('Dimensiunea populatiei: ', dimPop)
a, b = [float(x) for x in f.readline().split()]
print('Domeniul de definitie:', a, b)
grad = int(f.readline())
print('Grad: ', grad)
coeficienti = list(map(int, f.readline().split()))
print('Coeficienti: ', *coeficienti)
precizie = int(f.readline())
print('Precizie: ', precizie)
probRecombinare = float(f.readline())
print('Probabilitate recombinare: ', probRecombinare)
probMutatie = float(f.readline())
print('Probabilitate mutatie: ', probMutatie)
nrEtape = int(f.readline())
print('Numar etape: ', nrEtape)


# Algoritm
g = open('alg_genetici.out', 'w')
populatie, l = generarePopulatie(a, b, dimPop, precizie)
g.write('Populatie initiala: \n')
for i in range(len(populatie)):
    x = decodificare(populatie[i], a, b, precizie)
    g.write(f'{i + 1}: {populatie[i]} x = {x} f = {functie(x, grad, coeficienti)} \n')

# Gasim cel mai bun individ
indivizi = [decodificare(c, a, b, precizie) for c in populatie]
fitness = [functie(x, grad, coeficienti) for x in indivizi]
bestIndex = fitness.index(max(fitness))
best = populatie[bestIndex]
# print(populatie)
# Etapa 1
g.write('Probabilitati selectie: \n')
ptotal = performantaTotala(populatie, a, b, precizie, grad, coeficienti)
for i in range(len(populatie)):
    g.write(f'cromozom {i + 1} probabilitate {probabilitateIndivid(populatie[i], grad, coeficienti,ptotal, a, b, precizie)} \n')
g.write('Intervale probabilitati selectie: \n')
popInterm = selectie(populatie, a, b, precizie, grad, coeficienti, bestIndex, g, primaEtapa=True)
g.write(f'\nDupa selectie:\n')
for i in range(len(popInterm)):
    x = decodificare(popInterm[i], a, b, precizie)
    g.write(f'{i + 1}: {popInterm[i]} x = {x} f = {functie(x, grad, coeficienti)} \n')
g.write(f'Probabilitatea de incrucisare {probRecombinare}\n')
popInterm = incrucisare(popInterm, probRecombinare, l, g, primaEtapa=True)
g.write('Dupa incrucisare: \n')
for i in range(len(popInterm)):
    x = decodificare(popInterm[i], a, b, precizie)
    g.write(f'{i + 1}: {popInterm[i]} x = {x} f = {functie(x, grad, coeficienti)} \n')
g.write(f'Probabilitate de mutatie pentru fiecare gena {probMutatie}\nAu fost modificati cromozomii:\n')
popNoua = mutatie(popInterm, probMutatie, g, primaEtapa=True)
g.write('Dupa mutatie: \n')
for i in range(len(popNoua)):
    x = decodificare(popNoua[i], a, b, precizie)
    g.write(f'{i + 1}: {popNoua[i]} x = {x} f = {functie(x, grad, coeficienti)} \n')
g.write('Evolutia maximului:\n')

maxim = [functie(decodificare(best, a, b, precizie), grad, coeficienti)]



for etapa in range(nrEtape - 1):
    populatie = popNoua
    indivizi = [decodificare(c, a, b, precizie) for c in populatie]
    fitness = [functie(x, grad, coeficienti) for x in indivizi]
    bestIndex = fitness.index(max(fitness))
    # best = populatie[bestIndex]
    ptotal = performantaTotala(populatie, a, b, precizie, grad, coeficienti)
    popInterm = selectie(populatie, a, b, precizie, grad, coeficienti, bestIndex, g)
    popInterm = incrucisare(popInterm, probRecombinare, l, g)
    popNoua = mutatie(popInterm, probMutatie, g)
    indivizi = [decodificare(c, a, b, precizie) for c in popNoua]
    fitness = [functie(x, grad, coeficienti) for x in indivizi]
    bestIndex = fitness.index(max(fitness))
    best = populatie[bestIndex]
    maxim.append(functie(decodificare(best, a, b, precizie), grad, coeficienti))
    g.write(f'{functie(decodificare(best, a, b, precizie), grad, coeficienti)} \n')

grafic(maxim)
