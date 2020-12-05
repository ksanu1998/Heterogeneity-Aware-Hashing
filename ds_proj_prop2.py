import numpy as np  
import matplotlib.pyplot as plt  
import random
import time
import math

num_pos = 300 # number of positions on the ring
num_resources = 100 # number of resources

# simple uniform hashing function (modulo)
def my_hash(index, offset):
	return (((index%num_pos)+offset)%num_pos)

# dicts containing (index,metric) key-value pairs for set
Dict_high = {}
# indexing the set
high_count = 0

# metric is a number from 0 to 1
# assign metrics to the resources randomly, albeit following the threshold
for i in range(0, num_resources):
	random.seed(time.process_time())
	Dict_high[high_count]=float(random.uniform(0, 10)/10)
	high_count+=1
	
min_s = min(Dict_high.values()) # minimum value of metric in set

# dicts containing (index,position) key-value pairs for set
Dict_hash_high = {}

# indexing the set
high_count = 0

for i in range(0, num_resources):
	# number of times a member in set is to be hashed on to the ring
	num_hash_high = math.ceil(Dict_high[high_count]/min_s)
	temp = []
	for j in range(0, num_hash_high):
		temp.append(my_hash(i, random.randint(0,num_pos-1)))
	Dict_hash_high[high_count]=temp
	high_count+=1

# list storing the positions of the ring assigned to the members
temp_list = []
for i in range(0, len(Dict_hash_high)):
	for j in range(0, len(Dict_hash_high[i])):
		temp_list.append(Dict_hash_high[i][j])

# dict storing the frequency of members assigned to each position on the ring 
# (position,number of members assigned to that position) key-value pair
print(len(temp_list))
freq = {} 
for items in temp_list:
	freq[items] = temp_list.count(items)

# x (position) and y (number of members assigned to that position) axes for scatter plot 
x = [key[0] for key in freq.items()]
y = [key[1] for key in freq.items()]

# plot
plt.xlabel("Position on the ring")
plt.ylabel("Number of resources assigned to the position")
plt.scatter(x, y)
plt.savefig("./scatter_prop2.png")
# plt.show()
plt.close()

# x1 (resource) and y1 (number of positions hashed to on the ring) axes for scatter plot 
x1 = [key[0] for key in Dict_hash_high.items()]
y1 = [len(key[1]) for key in Dict_hash_high.items()]
plt.xlabel("Resource")
plt.ylabel("Number of positions hashed to on the ring")
plt.scatter(x1, y1, color="orange")
plt.savefig("./scatter_prop2_a.png")
plt.close()
