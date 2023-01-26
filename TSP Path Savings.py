import math
import matplotlib.pyplot as plt

#define function to return euclidean distance from 2 tuples of coordinates
def euclideanDistance(starting, ending):
    distance = math.sqrt((ending[0] - starting[0])**2 + (ending[1] - starting[1])**2)   
    return distance;


# plot all points on plot
x = [7,8.1,8.9,1.3,9.1,6.3,1,2.8,5.5,9.6,9.6]
y = [6,1.6,9.7,9.6,4.9,8,1.4,4.2,9.2,7.9,9.2]
plt.scatter(x,y)
plt.scatter(x[0], y[0], color = 'red')



locations = {
    'depo' : [7,6],
    'cust1' : [8.1, 1.6],
    'cust2' : [8.9, 9.7],
    'cust3' : [1.3, 9.6],
    'cust4' : [9.1, 4.9],
    'cust5' : [6.3, 8],
    'cust6' : [1, 1.4],
    'cust7' : [2.8, 4.2],
    'cust8' : [5.5, 9.2],
    'cust9' : [9.6, 7.9],
    'cust10' : [9.6, 9.2]
}

#plot annotations on plot
for key in locations:
        plt.annotate(key, (locations.get(key)[0], locations.get(key)[1]), (locations.get(key)[0] + .05, locations.get(key)[1] + .05), fontsize = 18)

plt.show()

savings = {}

#for each key we need to get the saving using distance as our cost measure
for key in locations:
    for key2 in locations:
        #checks that  the keys arent the same, they arent the depo, and that the opposite key isnt already chercked to save 
        # computation and not wastetime going through duplicate outputs 
        if key != key2 and key != 'depo' and key2 != 'depo' and (key2, key) not in savings:
            savings[(key,key2)] = euclideanDistance(locations.get('depo'), locations.get(key)) + euclideanDistance(locations.get('depo'), locations.get(key2)) - euclideanDistance(locations.get(key), locations.get(key2))

#weird but short pythonic way of sorting a dictionary using a lambda funtion
savings = dict(sorted(savings.items(), key=lambda item: item[1]))

#print the table using an f-string
for key in savings:
    print(f'{key[0]} | {key[1]} | {savings.get(key)}')

