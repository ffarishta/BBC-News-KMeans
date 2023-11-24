import math
import random

path = "bbc/bbc.mtx"

#Freq, Doc, Class?  
bbc_tf = open(path,"r")
#Create index {docid:{t1:freq,t2:freq...}...}
inv_index = {}
tf = {}
df = {}

#calculate index,tf,and df
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
    

#calculate idf 
N = len(inv_index)
idf =  {k: math.log(N/v,10) for (k, v) in df.items()}
# idf*tf
vals = {doc: {k: (1+math.log(v,10)) * idf[k] for k, v in inv_index[doc].items()} for doc in inv_index.keys()}

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
def k_means(k, vals, tolerance=1e-4, max_iterations=100):
    N = len(vals)
    centroids = {i: vals[doc] for i, doc in enumerate(random.sample(list(vals.keys()), k))}
    
    for iteration in range(max_iterations):
        new_centroids = {}
        centroid_count = {i: [] for i in range(k)}

        for doc in vals:
            
            # which cluster should each doc be assigned to
            best_params = [cosine_sim(vals[doc], centroids[x]) for x in centroids]
            max_centroid = best_params.index(max(best_params))

            # sum of cluster values
            if max_centroid not in new_centroids:
                new_centroids[max_centroid] = vals[doc].copy()
            else:
                for key in vals[doc]:
                    new_centroids[max_centroid][key] = new_centroids[max_centroid].get(key, 0) + vals[doc][key]
            centroid_count[max_centroid].append(doc)
        #dividing to get avg
        for c in new_centroids:
            count = len(centroid_count[c])
            for key in new_centroids[c]:
                new_centroids[c][key] /= count

        #stop condition
        if all(cosine_sim(centroids[i], new_centroids[i]) > (1 - tolerance) for i in range(k)):
            print(centroid_count)
            break

        centroids = new_centroids
        print(iteration)

    print("Converged after", iteration + 1, "iterations.")

# Example usage
k_means(5, vals)