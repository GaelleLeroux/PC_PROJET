import multiprocessing as mp
import time,random

def tache_controleur(verrou,go_chauffage,go_pompe,seuil_T,seuil_P):
    verrou.acquire()
    P = mem_xx[0]
    T = mem_xx[1]
    verrou.release()
    if (T > seuil_T):
        go_chauffage = False
        if (P > seuil_P):
            go_pompe = True
        else:
            go_pompe = False
    elif (T < seuil_T):
        go_pompe = True
        go_chauffage = True
    else:
        go_chauffage = False
        if (P > seuil_P):
            go_pompe = True
        else:
            go_pompe = False
    return go_pompe,go_chauffage

def tache_chauffage(go_chauffage,Vt):
    if go_chauffage:
        print('Mettre le chauffage en route')
        Vt += random.uniform(0,2)
    else:
        print("Veuillez arreter le chauffage")
        Vt -= random.uniform(0,2)
        while Vt < 0:
            Vt -= random.uniform(0,2)
    return Vt

def tache_pompe(go_pompe,Vp):
    if go_pompe:
        print('Il faut pomper monsieur')
        Vp -= random.uniform(0,2)
    else:
        print("Arreter la pompe")
        Vp += random.uniform(0,2)
        while Vp < 0:
            Vp += random.uniform(0,2)
    return Vp

def temperature(verrou,Vt):
    T = Vt*100 - 273
    verrou.acquire()
    mem_xx[1] = T
    verrou.release()


def pression(verrou,Vp):
    P = Vp*100
    verrou.acquire()
    mem_xx[0] = P
    verrou.release()

def tache_ecran(verrou):
    verrou.acquire()
    T = mem_xx[1]
    P = mem_xx[0]
    verrou.release()
    print("La température est de " + str(round(T,2)) +"°C et la pression est de " +str(round(P,2)) + "hPa")

if __name__ == '__main__':
    #Déclarations:
    verrou = mp.Semaphore(1)
    seuil_P,seuil_T = 5000.0,500.0
    go_pompe = False
    go_chauffage = False
    mem_xx = mp.Array('f',2)
    mem_xx[0] = 50.0
    mem_xx[1] = 500
    Vt = 2.73
    Vp = 1.30

    while True:
        temperature(verrou,Vt)
        time.sleep(0.5)
        pression(verrou,Vp)
        time.sleep(0.5)
        go_pompe,go_chauffage = tache_controleur(verrou,go_chauffage,go_pompe,seuil_T,seuil_P)
        time.sleep(0.5)
        tache_ecran(verrou)
        Vt = tache_chauffage(go_chauffage,Vt)
        Vp = tache_pompe(go_pompe,Vp)
        time.sleep(0.5)