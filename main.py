
from visualize_gates import draw_gate_packing
import heapq
"""
Create dictionary for the gate dimensions (gate_dimensions) and
gates coordinates (gates)
"""
max_height=100
min_area=1000000000000
max_width=100
gate_dimensions = {}
gate_dimensions_list=[]
max_height=0
sum_heights=0
total_area=0
error=0
a=0
b=0
with open("input.txt" , 'r') as f:
    l = f.readlines()
for i in l:
    i = i.split()
    gate_dimensions[i[0]] = [int(i[1]) , int(i[2])]
    gate_dimensions_list.append([int(i[1]),int(i[2]),i[0]])
    total_area+=int(i[1])*int(i[2])
    if max_height<int(i[2]):
        max_height=int(i[2])
    sum_heights+=int(i[2])

def naiveapproach1(gate_dimensions):
    gates = {}
    maxi = 0
    x = 0
    y = 0
    for i in gate_dimensions.items():
        gates[i[0]] = [x , y]
        x+=i[1][0]
        maxi = max(maxi , i[1][1])
    gates = {'bounding_box' : [x , maxi] , **gates}
    return gates

def naiveapproach2(gate_dimensions):
    gates = {}
    maxi = 0
    x = 0
    y = 0
    for i in gate_dimensions.items():
        gates[i[0]] = [x , y]
        y+=i[1][1]
        maxi = max(maxi , i[1][0])
    gates = {'bounding_box' : [maxi , y] , **gates}
    return gates
def optimal_packing_square(gates_list):
    global error,a,b,min_area
    height=max_height
    total_width=0
    min_height=101
    max_stack_height=0
    for i in gates_list:
        if min_height>i[1]:
            min_height=i[1]
    gates={}
    used_points=[] #stores list as [possible x, -possible y, max width, max height]
    heapq.heappush(used_points,(0,0,max_width + 1,height))
    sorted_gates_list=(sorted(gates_list, key=lambda x:x[0],reverse =True))
    for i in sorted_gates_list:
        l=[]
        change_in_height=False
        while (used_points):
            k=heapq.heappop(used_points)
            if(k[1]==0):
                total_width+=i[0]
                height=max(height,total_width)
                gates[i[2]]=[k[0],k[1]]
                heapq.heappush(used_points,(k[0],-i[1],i[0],height-i[1]))
                heapq.heappush(used_points,(total_width,0,max_width+1,height))
                if max_stack_height<i[1]:
                    max_stack_height=i[1]
                change_in_height=True
                break
            elif(i[0]<=k[2] and i[1]<=k[3]):
                gates[i[2]]=[k[0],-k[1]]
                heapq.heappush(used_points,(k[0],k[1]-i[1],i[0],height+k[1]-i[1]))
                if (k[2]-i[0]>0):
                    heapq.heappush(used_points,(k[0]+i[0],k[1],k[2]-i[0],height+k[1]))
                if max_stack_height<i[1]-k[1]:
                    max_stack_height=i[1]-k[1]
                break
            else:
                l.append(k)
        for j in l:
            if (change_in_height):
                heapq.heappush(used_points,(j[0],j[1],j[2],height+j[1]))
            else:
                heapq.heappush(used_points,j)
    gates={'bounding_box':[total_width, max_stack_height],**gates}
        
    error=(gates['bounding_box'][0]*gates['bounding_box'][1]-total_area)*100/total_area
    a=gates['bounding_box'][0]
    b=gates['bounding_box'][1]
    min_area=a+b
    return gates
def optimal_packing(gates_list):
    global error,a,b,min_area
    final={}
    
    step=1
    if(len(gates_list)>=100):
        step=10
    for height in range(max(max_height,int(1/2 * total_area**0.5)), min(sum_heights,int(2*(total_area)**0.5))+1,step):
        total_width=0
        min_height=101
        max_stack_height=0
        for i in gates_list:
            if min_height>i[1]:
                min_height=i[1]
        gates={}
        used_points=[] #stores list as [possible x, -possible y, max width, max height]
        heapq.heappush(used_points,(0,0,max_width + 1,height))
        sorted_gates_list=(sorted(gates_list, key=lambda x:x[0],reverse =True))
        for i in sorted_gates_list:
            l=[]
            while (used_points):
                k=heapq.heappop(used_points)
                if(k[1]==0):
                    total_width+=i[0]
                    gates[i[2]]=[k[0],k[1]]
                    heapq.heappush(used_points,(k[0],-i[1],i[0],height-i[1]))
                    heapq.heappush(used_points,(total_width,0,max_width+1,height))
                    if max_stack_height<i[1]:
                        max_stack_height=i[1]
                    break
                elif(i[0]<=k[2] and i[1]<=k[3]):
                    gates[i[2]]=[k[0],-k[1]]
                    if (k[3]-i[1])>=min_height:
                        heapq.heappush(used_points,(k[0],k[1]-i[1],i[0],k[3]-i[1]))
                    if(k[2]-i[0]!=0):
                        heapq.heappush(used_points,(k[0]+i[0],k[1],k[2]-i[0],k[3]))
                    if max_stack_height<i[1]-k[1]:
                        max_stack_height=i[1]-k[1]
                    break
                else:
                    l.append(k)
            for j in l:
                heapq.heappush(used_points,j)
        gates={'bounding_box':[total_width, max_stack_height],**gates}
        if (total_width+max_stack_height)<min_area:
            min_area=total_width+max_stack_height
            final=gates
    error=(final['bounding_box'][0]*final['bounding_box'][1]-total_area)*100/total_area
    a=final['bounding_box'][0]
    b=final['bounding_box'][1]
    return final



root = draw_gate_packing(gate_dimensions, optimal_packing(gate_dimensions_list), (110,110))
print(error,a,b,min_area)
root.mainloop()
