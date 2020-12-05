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

# metric is a number from 0 to 1
# s_high is a set with metric higher than all the members of the set s_low
thresh_s_low = 0.6 # all members in s_low have the metric less than this number
# 7:3 => s_high : s_low split of resources
s_high_ratio = 0.7

# dicts containing (index,metric) key-value pairs for s_high and s_low sets
Dict_high = {}
Dict_low = {}

# indexing the s_high and s_low sets
high_count = 0
low_count = 0

# assign metrics to the resources randomly, albeit following the threshold
for i in range(0, num_resources):
	if i<=s_high_ratio*num_resources:
		random.seed(time.process_time())
		Dict_high[high_count]=float(random.uniform(thresh_s_low*10, 10)/10)
		high_count+=1
	else:
		random.seed(time.process_time())
		Dict_low[low_count]=float(random.uniform(0, thresh_s_low*10)/10)
		low_count+=1

w_s = s_high_ratio*num_resources # number of members in s_high set
w_s_prime = (1-s_high_ratio)*num_resources # number of members in s_low set
min_s = min(Dict_high.values()) # minimum value of metric in s_high set
min_s_prime = min(Dict_low.values()) # minimum value of metric in s_low set

# print statements for debugging
"""
print('min_s: '+str(min_s))
print('min_s_prime: '+str(min_s_prime))
print('w_s: '+str(w_s))
print('w_s_prime: '+str(w_s_prime))
print('w_s*min_s: '+str(w_s*min_s))
print('w_s_prime*min_s_prime: '+str(w_s_prime*min_s_prime))
print('subtrahend: '+str(((w_s*min_s) - (w_s_prime*min_s_prime))/w_s))
"""

# number of times a member in s_high set is to be hashed on to the ring
num_hash_high = 1+math.ceil(((w_s*min_s) - (w_s_prime*min_s_prime))/w_s)
print('num_hash_high: '+str(num_hash_high))

# dicts containing (index,position) key-value pairs for s_high and s_low sets
Dict_hash_high = {}
Dict_hash_low = {}

# indexing the s_high and s_low sets
high_count = 0
low_count = 0

for i in range(0, num_resources):
	if i<=s_high_ratio*num_resources:
		temp = []
		for j in range(0, num_hash_high):
			temp.append(my_hash(i, random.randint(0,num_pos-1)))
		Dict_hash_high[high_count]=temp
		high_count+=1
	else:
		Dict_hash_low[low_count]=my_hash(i,0)
		low_count+=1

# list storing the positions of the ring assigned to the members
temp_list = []
for i in range(0, len(Dict_hash_high)):
	for j in range(0, len(Dict_hash_high[i])):
		temp_list.append(Dict_hash_high[i][j])
temp_list = temp_list + list(Dict_hash_low.values())

# dict storing the frequency of members assigned to each position on the ring 
# (position,number of members assigned to that position) key-value pair
freq = {} 
for items in temp_list: 
	freq[items] = temp_list.count(items)

# print (position,number of members assigned to that position) key-value pairs
# for key, value in freq.items(): 
# 	print ("% d : % d"%(key, value))

# x (position) and y (number of members assigned to that position) axes for scatter plot 
x = [key[0] for key in freq.items()]
y = [key[1] for key in freq.items()]

# plot
plt.xlabel("Position on the ring")
plt.ylabel("Number of resources assigned to the position")
plt.scatter(x, y)
plt.savefig("./scatter_prop1.png")
# plt.show()
plt.close()

# x1 (resource) and y1 (number of positions hashed to on the ring) axes for scatter plot 
x11 = [key[0] for key in Dict_hash_high.items()] + [len(Dict_hash_high)+key[0] for key in Dict_hash_low.items()]
y11 = [len(key[1]) for key in Dict_hash_high.items()] + [len([key]) for key in Dict_hash_low.items()]
plt.xlabel("Resource")
plt.ylabel("Number of positions hashed to on the ring")
plt.scatter(x11, y11, color="orange")
plt.savefig("./scatter_prop1_a.png")
plt.close()
