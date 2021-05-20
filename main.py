import numpy as np
import sys
import math

input_file = sys.argv[1] if len(sys.argv) > 1 else 'data.txt'

G = 6.6743015151515151515151515151515e-11
dt = 1000 # skok czasowy


def acceleration(F,m):
    return [F[0]/m, F[1]/m, F[2]/m]

def Force(body1, body2):
    F = G*(body1[0]*body2[0]/(distance(body1, body2)**2))
    wektor = get_wektor(body1, body2)
    wersor = get_wersor(wektor)
    return F*wersor

def get_wersor(wektor):
    wektor = np.array(wektor)
    return wektor / math.sqrt(abs(wektor[0]**2 + wektor[1]**2 + wektor[2]**2))

def get_wektor(body1, body2):
    x = body2[1] - body1[1]
    y = body2[2] - body1[2]
    z = body2[3] - body1[3]

    return [x,y,z]

def distance(body1, body2):
    return math.sqrt((body1[1]-body2[1])**2 + (body1[2]-body2[2])**2 + (body1[3] - body2[3])**2)

def read(input_file):
    data = []
    names = []
    with open(input_file) as f:
        for line in f.readlines()[2:]:
            bodies = []
            line = line.split()
            if len(line) < 8:
                raise ValueError("Zbyt mała ilość parametrów obiektu w linii " + line)
            names.append(line[0])
            for i in range(7):
                    bodies.append(int(line[i+1]))
            data.append(bodies)

    return names, data


def main():
    NUM_ITER = int(sys.argv[1]) if len(sys.argv) > 1 else 100 #ilość iteracji
    names, data = read("data.txt") 
    N = len(names)
    acceleration_table = np.zeros((N, N, 3))   
    for k in range(NUM_ITER):
        for i in range(N):
            mass = data[i][0]
            for j in range(N):
                if i==j:
                    continue
                F = Force(data[i], data[j]) #wyznaczanie sily grawitacji miedzy i,j
                a = acceleration(F, mass) #wyznaczanie przyspieszenia miedzy i,j
                acceleration_table[i][j] = a #zapisywanie przyspieszeń do tablicy

        body_acceleration = np.zeros((N,3))
        for i in range(N):
            for j in range(N):
                body_acceleration[i][0] += acceleration_table[i][j][0].sum() #sumowanie przyspieszenia x
                body_acceleration[i][1] += acceleration_table[i][j][1].sum() #sumowanie przyspieszenia y
                body_acceleration[i][2] += acceleration_table[i][j][2].sum() #sumowanie przyspieszenia z

        for i in range(N):
            data[i][1] += data[i][4] * dt + 0.5 * body_acceleration[i][0] * dt**2 # aktualizacja położenia x y z
            data[i][2] += data[i][5] * dt + 0.5 * body_acceleration[i][1] * dt**2
            data[i][3] += data[i][6] * dt + 0.5 * body_acceleration[i][2] * dt**2
            data[i][4] += body_acceleration[i][0] * dt #aktualizacja prędkości x y z
            data[i][5] += body_acceleration[i][1] * dt
            data[i][6] += body_acceleration[i][2] * dt

    f = open("python_output.txt", 'w')

    for i in range(N):
        f.write(str(names[i]) + " " + str(data[i][0]) + " " + str(data[i][1]) + "  " + str(data[i][2]) + "  " + str(data[i][3]) + "  " + str(data[i][4]) + "  " + str(data[i][5]) + "  " + str(data[i][6]) + "\n")
    f.close()

if __name__ == '__main__':
    main()