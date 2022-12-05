# import random 
# import time 
class NodeX:
    def __init__(self,low,high):
        self.range =  [low,high] 
        self.left = self.right = self.y_list = None 

    def __str__(self):
        return self.range  
    
def merge_lists(l1,l2):
    l = [] 
    i = j = 0

    while (i < len(l1) and j <len(l2) ):
        if (l1[i][1] >=l2[j][1]):
            l.append(l2[j])
            j+=1
        else:
            l.append(l1[i]) 
            i += 1 
    
    while (i < len(l1)):
        l.append(l1[i])
        i += 1
    
    while (j < len(l2)):
        l.append(l2[j]) 
        j += 1 
    
    return l

def query_1_d_y(l,low,high): # returns a list of elements in range [low,high] in sorted list l
    n = len(l)
    if (n == 0): return [] 
    if (low == high):
        if (low < l[0][1] or low > l[n-1][1]):
            return [] 
        else:
            left,right = 0,n-1 
            mid = (left + right)//2 
            while(left < right): 
                if (l[mid][1] < low):
                    left = mid + 1
                    mid = (left+right)//2
                    
                elif (l[mid][1] > low):
                    right = mid - 1 
                    mid = (left + right)//2
                    
                else:
                    return [l[mid]] 
            if (l[left][1] == low):return [l[left]] 
            else:return [] 
        

    # low != high
    # finding low index
    
    if (low > high):return []

    low_index = 0
    if (low <= l[0][1]) : low_index = 0 
    elif (low > l[n-1][1]) : return [] 
    else:

        left = 0 
        right = n-1
        mid = (left + right)//2 
        while (left!=right):
            if (l[mid][1] > low):
                right = mid
                mid = (left + right)//2 
            elif (l[mid][1] < low):
                left = mid + 1 
                mid = (left + right)//2  

            else:
                low_index = mid 
                break 
        if (left == right):low_index = left 
    
    #finding high index 
    high_index = 0
    if (high < l[0][1]) : return []  
    elif (high >= l[n-1][1]) : high_index = n-1  
    else:

        left = 0 
        right = n-1
        mid = (left + right)//2 + 1
        while (left!=right):
            if (l[mid][1] > high):
                right = mid - 1
                mid = (left + right)//2 + 1
            elif (l[mid][1] < high):
                left = mid  
                mid = (left + right)//2  + 1

            else:
                high_index = mid 
                break
        
        if (left == right) : high_index = left
    return l[low_index:high_index+1] 

class PointDatabase:
    def __init__(self,pointlist):
        
        pointlist.sort(key = lambda x :x[0]) 
        
        
        self.x_list = pointlist
        #print(self.x_list)
        # y_list = pointlist.sort(key = lambda x : x[1]) 
        self.pointDB = self.make(0,len(self.x_list)-1,self.x_list) 

    def make(self,low,high,l):
        if (low > high):return None #  handling empty list case 
        if (low == high): # leaf node 
            node = NodeX(l[low],l[high])    
            node.y_list = [l[low]]    
            return node 
        
        median = (low + high)//2 

        left_tree = self.make(low,median,l) 
        right_tree = self.make(median+1,high,l) 

        node = NodeX(l[low],l[high])   
        node.y_list = merge_lists(left_tree.y_list , right_tree.y_list) 
        node.left = left_tree 
        node.right = right_tree 
        return node 
    
    def query_2_d(self,x_low,x_high,y_low,y_high,root,output):
        if (x_low > x_high):return 
        if (root.range[0] == root.range[1]): # root is a leaf 
            x = root.range[0][0] 
            y = root.range[0][1]
            if (x <= x_high and x>= x_low and y <= y_high and y >= y_low):
                output.append(root.range[0])   
                return 
        
        else:
            x1,x2 = root.range[0][0],root.range[1][0]
        
            if (x1 >= x_low and x2 <= x_high):
                ans = query_1_d_y(root.y_list,y_low,y_high) 
                output.extend(ans) 
                return 
            elif (x1 > x_high or x2 < x_low):
                 
                return 
            else:
                self.query_2_d(x_low,x_high,y_low,y_high,root.left,output)
                self.query_2_d(x_low,x_high,y_low,y_high,root.right,output)
                return
        return   
    
    def searchNearby(self, q, d):
        x_low,x_high = (q[0] - d) , (q[0] + d) 
        y_low,y_high = (q[1] - d) , (q[1] + d) 
        ans = [] 
        if (self.pointDB is None):return []

        if ((q[0] - d) <= self.x_list[0][0]):x_low = self.x_list[0][0]
        if ((q[0] + d) >= self.x_list[-1][0]):x_high = self.x_list[-1][0] 
        
        self.query_2_d(x_low,x_high,y_low,y_high,self.pointDB,ans) 
        return ans 





# l = [(1,5),(2,5),(3,5),(7,5),(8,5),(9,5),(5,1),(5,2),(5,3),(5,7),(5,8),(5,9)]
# pointDbObject = PointDatabase(l) 
# print(pointDbObject.searchNearby((5,5), 1))

# l = [(4,8),(6,8),(8,8),(8,6),(8,4),(6,4),(4,4),(4,6)]
# pointDbObject = PointDatabase(l) 
# print(pointDbObject.searchNearby((6,6), 2))




# l = [(1,6), (2,4), (3,7), (4,9), (5,1), (6,3), (7,8), (8,10),(9,2), (10,5)] 

# pointDbObject = PointDatabase(l)
# print(pointDbObject.searchNearby((6,6),2))
# print(pointDbObject.searchNearby((-3,1),3)) 
# print(pointDbObject.searchNearby((12,5),1))
# print(pointDbObject.searchNearby((8,12),2))
# print(pointDbObject.searchNearby((5,-2),2))
# print(pointDbObject.searchNearby((-3,5),7))
# print(pointDbObject.searchNearby((13,1),2))
# print(pointDbObject.searchNearby((5,23),4))
# print(pointDbObject.searchNearby((5,-4),3))
# print(pointDbObject.searchNearby((0,6),4))    
# print(pointDbObject.searchNearby((3,1),20))
# print(pointDbObject.searchNearby((-3,1),20)) 
# print(pointDbObject.searchNearby((3,1),0))
# print(pointDbObject.searchNearby((3,1),1))
# print(pointDbObject.searchNearby((-1,6),5))
# print(pointDbObject.searchNearby((6,6),4)) 
# print(pointDbObject.searchNearby((6,6),0))
# print(pointDbObject.searchNearby((-1,-1),0))
# print(pointDbObject.searchNearby((11,11),0))

 
# print(pointDbObject.searchNearby((5,1),0)) 
# l.sort(key = lambda x:x[1] )
# print(query_1_d_y(l,19,23))
# for i in range(1,11):
#     print(query_1_d_y(l,i,i))

#pointDbObject = PointDatabase([(1,6), (2,4), (3,7), (4,9), (5,1), (6,3), (7,8), (8,10),(9,2), (10,5)])


# print(pointDbObject.searchNearby((5,5), 1))
# print(pointDbObject.searchNearby((4,8), 2)) 
# print(pointDbObject.searchNearby((10,2), 1.5)) 

# l = [(1,6), (2,4), (3,7), (4,9), (5,1), (6,3), (7,8), (8,10),(9,2), (10,5),(12,35),(23,20),(45,15)] 
# l.sort(key = lambda x : x[1])
# print(query_1_d_y(l,3,11))
#l = [(0,3),(1,6), (2,4), (3,7), (4,9), (5,0), (6,3), (7,8), (8,10),(9,2), (10,5)]
#l = [(4,8),(6,8),(8,8),(8,6),(8,4),(6,4),(4,4),(4,6)]
# random.shuffle(l)
# print(l) 
# pointDbObject = PointDatabase(l)
# print(pointDbObject.searchNearby((6,6),2))
# print(pointDbObject.searchNearby((-3,1),3)) 
# print(pointDbObject.searchNearby((12,5),1))
# print(pointDbObject.searchNearby((8,12),2))
# print(pointDbObject.searchNearby((5,-2),2))
# print(pointDbObject.searchNearby((-3,5),7))
# print(pointDbObject.searchNearby((13,1),2))
# print(pointDbObject.searchNearby((5,23),4))
# print(pointDbObject.searchNearby((5,-4),3))
# print(pointDbObject.searchNearby((0,6),4))    
# print(pointDbObject.searchNearby((3,1),20))
# print(pointDbObject.searchNearby((-3,1),20)) 
# print(pointDbObject.searchNearby((3,1),0))
# print(pointDbObject.searchNearby((3,1),1))
# print(pointDbObject.searchNearby((-1,6),5))
# print(pointDbObject.searchNearby((6,6),4))
 
# print(pointDbObject.searchNearby((5,1),0))  

# l2 = [(23,3),(3,4),(4,4.56),(36,6)] 
# l1 = [(23,1),(3,2),(4,4.5),(36,7)] 
# print(merge_lists(l1,l2))  


# import ast 
# start1 = time.time()  
# list = [] 
# file_name = "./testcases.txt" 
# with  open(file_name,"r") as f:
#     while (True):
#         s = f.read(1024) 
#         if (not s):break 
#         for i in s.split():
#             list.append(i) 
# input_str = ''.join(list) 
# input = ast.literal_eval(input_str)
# start2 = time.time() 

# print(f'time taken to generate input is {(start2-start1)} seconds')

# db = PointDatabase(input) 
# end = time.time() 

# print(f"time taken to make database is {(end-start2)} second")  
# f.close() 