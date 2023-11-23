import math
import random

path = "bbc/bbc.mtx"

#Freq, Doc, Class?  
bbc_tf = open(path,"r")
#Create index {docid:{t1:freq,t2:freq...}...}
inv_index = {}
tf = {}
df = {}

for i in bbc_tf.readlines()[1:]:
    line = i.split(" ")

    term = line[0]
    doc = int(line[1])
    freq = int(float(line[2].strip()))
    
    if doc not in inv_index:
            inv_index[doc] = {term: freq}
    else:
        inv_index[doc][term] = freq
    
    tf[term] = tf.get(term, 0) + freq
    df[term] = df.get(term, 0) + 1
    

#calculate cosine simularity 
N = len(inv_index)
idf =  {k: math.log(N/v,10) for (k, v) in df.items()}

# idf*tf
vals = {doc: {k: v * idf[term] for k, v in inv_index[doc].items()} for doc in inv_index.keys()}
vals = dict(sorted(vals.items()))

def magnitude(vector):
    return math.sqrt(sum(x**2 for x in vector))

def cosine_sim(doc, cluster):
    sim = {}
    dot_prod = 0
    for i in doc:
        if i in cluster:    
            dot_prod += doc[i] *cluster[i]
    return dot_prod/(magnitude(doc.values())*magnitude(cluster.values()))
            

#work in progress 
def k_means(k,vals):
    centroids = []
    # Intialize Centroids
    for i in range(k):
        centroids.append(vals[random.randint(1, N)])

    while True:
        # Assignment step using cosine similarity 

        #Calculate cosine simularities 
        similarities = [[cosine_sim(vals[i],centroid) for centroid in centroids] for i in vals]
        #assign a centroid to each doc 
        labels = [max(enumerate(sim), key=lambda x: x[1])[0] for sim in similarities]
        
        #calculate the new centroids
        new_centroids = {} 
        
        """
        for j, c in enumerate(labels):
            if j not in new_centroids:
                new_centroids[j] = vals[c]
            else:
                for key in vals[c]:
                    # combine keys 
        """
k_means(3,vals)
           



    




            
            

 
        

    
    


