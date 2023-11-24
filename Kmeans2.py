import numpy as np 
import math
import random 
np.set_printoptions(threshold=np.inf)


# Import .mtx with format Freq, Doc, Class
path = "bbc/bbc.mtx"
bbc = open(path,"r")

index = np.zeros((2225, 9635))
df = np.zeros(9635)

for i in bbc.readlines()[1:]:
    line = i.split(" ")
    term = int(line[0]) -1
    doc = int(line[1])-1
    freq = int(float(line[2].strip()))

    index[doc][term] = freq

    df[term] += 1
N = len(index)
idf = np.log10(N / df)

#vals = (1 + np.log10(index)) * idf
#index[index>0] = (1 + np.log10(index[index>0])) * idf

result = np.where(index > 0, (1 + np.log10(np.maximum(1, index))) * idf, 0)

import numpy as np
def magnitude(vector):
    return math.sqrt(sum(x**2 for x in vector))

def cosine_similarity(vec1, vec2):
    dot_product = np.dot(vec1, vec2)
    magnitude_vec1 = magnitude(vec1)
    magnitude_vec2 = magnitude(vec2)

    similarity = dot_product / (magnitude_vec1 * magnitude_vec2)
    return similarity

def k_means_cosine_similarity(k, data, tolerance=1e-4, max_iterations=100):
    n, m = data.shape
    centroids = data[np.random.choice(n, k, replace=False)]

    for iteration in range(max_iterations):
        # Calculate distances based on cosine similarity
        distances = np.array([[cosine_similarity(data[i], centroids[j]) for j in range(k)] for i in range(n)])

        # Assign each data point to the nearest centroid
        labels = np.argmax(distances, axis=1)

        # Update centroids
        new_centroids = np.array([np.mean(data[labels == j], axis=0) for j in range(k)])

        # Check convergence
        if np.all(cosine_similarity(centroids[0], new_centroids[0]) > (1 - tolerance)):
            break

        centroids = new_centroids
        print(iteration)

    print(f"Converged after {iteration + 1} iterations.")
    return labels
    


k_means_cosine_similarity(5,result)



