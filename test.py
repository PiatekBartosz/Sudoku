def tablica(m, n):
    tablica = []
    for i in range(m):
        tablica_chiwlowa = []
        for j in range(n):
            tablica_chiwlowa.append(0)
        tablica.append(tablica_chiwlowa)
    return tablica

print(tablica(2, 3))
