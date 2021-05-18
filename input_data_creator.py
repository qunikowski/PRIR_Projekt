import random
import sys
#N = 100
#MAX_MASS = 1e10
#MAX_POSITION= 1e20
#MAX_VELOCITY= 1e10

N = int(sys.argv[1]) if len(sys.argv) > 1 else 100
MAX_MASS = int(sys.argv[2]) if len(sys.argv) > 2 else 1e15
MAX_POSITION= int(sys.argv[3]) if len(sys.argv) > 3 else 1e15
MAX_VELOCITY= int(sys.argv[4]) if len(sys.argv) > 4 else 1e15
output_file = 'data.txt'

f = open(output_file, 'w')

f.write("name/id  mass  pos_x  pos_y  pos_z vel_x  vel_y  vel_z\n")
for i in range(N):
    name = i
    mass = random.randint(1,MAX_MASS)
    pos_x = random.randint(-MAX_POSITION,MAX_POSITION)
    pos_y = random.randint(-MAX_POSITION, MAX_POSITION)
    pos_z = random.randint(-MAX_POSITION, MAX_POSITION)
    vel_x = random.randint(-MAX_VELOCITY, MAX_VELOCITY)
    vel_y = random.randint(-MAX_VELOCITY, MAX_VELOCITY)
    vel_z = random.randint(-MAX_VELOCITY, MAX_VELOCITY)
    
    f.write("" + str(name) + " " + str(mass) + " " + str(pos_x) + " " + str(pos_y) + " " + str(pos_z) + " " + str(vel_x) + " " + str(vel_y) + " " + str(vel_z) + "\n")

f.close()
