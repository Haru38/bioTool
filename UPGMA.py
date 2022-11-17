# https://ja.wikipedia.org/wiki/%E9%9D%9E%E5%8A%A0%E9%87%8D%E7%B5%90%E5%90%88%E6%B3%95


class Cluster():
    def __init__(self,name,numOfElements):
        #cluster name
        self.name = name
        #Number of clusters belonging to the cluster
        self.elements = numOfElements

    #Distance from other clusters 
    def set_distance(self,distance):
        self.distance = distance
        
    #Distance between clusters belonging to a cluster
    def set_distance_between_elements(self,dbe):
        self.dbe = dbe
    
    #Objects of clusters belonging to the cluster
    def set_elementsObject(self,elements):
        self.elements_object = elements

        
#Function to output the result
def print_tree(child,parent):
    if len(child.elements_object) != 0:
        if parent != "":
            print("parent :",parent.name,">>","child : ",child.name)
            print("\tHeight of contact point",parent.dbe/2)
        for o in child.elements_object:
            print_tree(o,child)
    else:
        print("parent :",parent.name,">>","child : ",child.name)
        print("\tHeight of contact point",parent.dbe/2)

class UPGMA():
    def search_minvalue(self,distance_matrix):
        '''
        Find the minimum value and the corresponding pair in the distance matrix.
        '''
        min_distances = []
        #Find the minimum value for each row
        for name in distance_matrix:
            distance = distance_matrix[name]
            min_distances.append([min(distance, key=distance.get),min(distance.values())])
        #Minimum value in the distance matrix
        minvalue = min([e[1] for e in min_distances])
        #Pairs corresponding to the minimum value
        pair = [e[0] for e in min_distances if e[1] ==  minvalue]
        
        return pair,minvalue
    
    def make_new_cluster(self,clusters,pair,minvalue):
        '''
        Merging two clusters to create a new cluster.
        '''
        new_cluster = []
        elements = []
        newname = "{"
        newcluster_num_of_elements = 0
        for i,p in enumerate(pair):
            e = search_cluster(clusters,p)
            newcluster_num_of_elements+=e.elements
            if i+1 == len(pair):
                newname += p + "}"
            else:
                newname += p+","
            elements.append(e)
        
        #new cluster
        c = Cluster(newname,newcluster_num_of_elements)
        #Distance between elements
        c.set_distance_between_elements(minvalue)
        #Adding an element object
        c.set_elementsObject(elements)
        clusters.append(c)
        
        return newname
    
    
    def make_new_distance_matrix(self,newname,distance_matrix,pair,clusters):
        '''
        Recalculate the distance between the new cluster and the others
        '''
        newclusters = [newname]#New cluster name group
        newcluster_distance = {}
        for name in list(distance_matrix.keys()):
            if name not in pair:
                newclusters.append(name)
                sum_distance = 0
                num_of_elements = 0
                for element in pair:
                    ec = search_cluster(clusters,element)
                    num_of_elements += ec.elements
                    #Calculating the average distance
                    sum_distance += ec.distance[name] * ec.elements
                resultdistance = sum_distance/num_of_elements
                newcluster_distance[name] = resultdistance
        search_cluster(clusters,newname).set_distance(newcluster_distance)
    
        #Creating a Distance Matrix
        distance_matrix  = {newname : newcluster_distance}
        for name1 in newclusters:
            if name1 != newname:
                newdistancemat = {}
                c = search_cluster(clusters,name1)
                for name2 in newclusters:
                    if name1 != name2:
                        if name2 == newname:#Distance to the new cluster
                            newdistancemat[newname] = newcluster_distance[name1]
                        else:#Distance from existing clusters
                            newdistancemat[name2] = c.distance[name2]
                c.set_distance(newdistancemat)
                distance_matrix[name1] = newdistancemat
                
        return distance_matrix

#Function to find the corresponding clusters
def search_cluster(clusters,name):
    for cluster in clusters:
        if cluster.name == name:
            return cluster

if __name__ == "__main__":
    distance_matrix = {"A":{ "B":6,"C":7,"D":3,"E":7,"F":4},
                                      "B":{"A":6,"C":4,"D":4,"E":6,"F":5},
                                      "C":{ "A":7,"B":0.04,"D":0.11},
                                      "D":{ "A":0.21,"B":0.13,"C":0.11}}
    all_culusters = len(distance_matrix)

    #Initialize the cluster
    clusters = []
    for name in distance_matrix :
        c = Cluster(name,1)
        c.set_distance(distance_matrix[name])
        c.set_elementsObject([])
        clusters.append(c)

    upgma=UPGMA()
    print(">>distance matrix")
    loop = 0
    while True:
        loop += 1
        #Find the minimum value in a matrix
        pair,minvalue = upgma.search_minvalue(distance_matrix)
        #Create a new cluster and get its name
        newname = upgma.make_new_cluster(clusters,pair,minvalue)
        if search_cluster(clusters,newname).elements ==all_culusters:
            break
        #Creating a Distance Matrix
        distance_matrix = upgma.make_new_distance_matrix(newname,distance_matrix,pair,clusters)
        print("loop : ",loop,">", distance_matrix)
    print("-------------------------------")
    print(">>tree")
    print_tree(search_cluster(clusters,newname),"")



