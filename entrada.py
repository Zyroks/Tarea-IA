def entrada():
    with open("arbol.txt", "r") as archivo:
        datos = []
        init = archivo.readline().split(' ')[1].strip()
        goal = archivo.readline().split(' ')[1].strip()
        h = []
        e = []
        for it in archivo:
            dato = it.strip().split() if ' ' in it else it.strip().split(',')
            if(len(dato)==2):
                dic = [dato[0],int(dato[1])]
                h.append(dic)
            elif(len(dato) == 3):
                e.append([dato[0],dato[1],int(dato[2])])
    datos.append(init)
    datos.append(goal)
    datos.append(h)
    datos.append(e)
    return datos