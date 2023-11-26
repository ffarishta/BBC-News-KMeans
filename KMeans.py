import math
import random

def get_weights(path):
    inv_index = {}
    tf = {}
    df = {}

    with open(path, "r") as bbc_tf:
        # Calculate index, tf, and df
        for line in bbc_tf.readlines()[1:]:
            term, doc, freq = line.split()
            doc = int(doc)
            freq = int(float(freq.strip()))

            inv_index.setdefault(doc, {})[term] = freq
            tf[term] = tf.get(term, 0) + freq
            df[term] = df.get(term, 0) + 1

    # Calculate idf
    N = len(inv_index)
    idf = {k: math.log(N/v, 10) for k, v in df.items()}

    # Calculate idf*tf {docID : {term:weight}}
    weights = {doc: {k: (1+math.log(v, 10)) * idf[k] for k, v in terms.items()} for doc, terms in inv_index.items()}

    # Sort the dictionary by docID
    weights = dict(sorted(weights.items()))

    return weights

def magnitude(vector):
    return math.sqrt(sum(x**2 for x in vector))

def cosine_simularity(doc, cluster):
    sim = {}
    dot_prod = 0
    #calculate dot product between two vectors
    for i in doc:
        if i in cluster:    
            dot_prod += doc[i] *cluster[i]
    return dot_prod/(magnitude(doc.values())*magnitude(cluster.values()))

def k_means(k, vals, tolerance=1e-4, max_iterations=100):
    N = len(vals)
    centroids = {i: vals[doc] for i, doc in enumerate(random.sample(list(vals.keys()), k))}
    
    for iteration in range(max_iterations):
        # new_centroids - {centroidID : vector of weights for that centroid (aka doc)}
        new_centroids = {}
        # centroid_count - {centroid_doc : [docIDs]}
        clusters = {i: [] for i in range(k)}

        for doc in vals:
            # Assign doc to cluster
            best_params = [cosine_simularity(vals[doc], centroids[x]) for x in centroids]
            max_centroid = best_params.index(max(best_params))

            # Sum vectors in cluster
            if max_centroid not in new_centroids:
                new_centroids[max_centroid] = vals[doc].copy()
            else:
                for key in vals[doc]:
                    new_centroids[max_centroid][key] = new_centroids[max_centroid].get(key, 0) + vals[doc][key]
            clusters[max_centroid].append(doc)
        #dividing to get avg
        for c in new_centroids:
            count = len(clusters[c])
            for key in new_centroids[c]:
                new_centroids[c][key] /= count

        #stop condition
        if all(cosine_simularity(centroids[i], new_centroids[i]) > (1 - tolerance) for i in range(k)):
            #print(centroid_count)
            centroids = new_centroids
            break
        centroids = new_centroids
        print(iteration)

    print("Converged after", iteration + 1, "iterations.")
    return clusters,centroids

def internal_criteria(clusters, centroid, docs):
    distances = {}
    for cluster, cluster_docs in clusters.items():
        centroid_terms = set(centroid[cluster])
        for doc in cluster_docs:
            doc_terms = set(docs[doc])
            common_terms = centroid_terms.intersection(doc_terms)
            squared_sum = sum((centroid[cluster][term] - docs[doc][term])**2 for term in common_terms)
            distances[doc] = squared_sum
    return distances

# clusters,centroids = k_means(5, vals)
# #print("centroid",print(centroids))
# print(internal_criteria(clusters,centroids,vals))


# external criteria: purity
# clusters - dictionary {centroid_doc : [docIDs]}
def purity(clusters):
    path = "bbc/bbc.classes"
    bbc_classes = open(path,"r")
    docID_classes = {}

    for i in bbc_classes.readlines()[4:]:
        line = i.split(" ")
        # adding 1 because classes start with first docid=0, but other files start with docid=1
        docID_classes[int(line[0])+1] = int(line[1].strip())

    majorityClass_arr = []
    for centroid_doc, doc_id_arr in clusters.items():
        classes_sum = {}
        for doc_id in doc_id_arr:
            classes_sum[docID_classes.get(doc_id)] = classes_sum.get(docID_classes.get(doc_id), 0) + 1
        majority_class = max(classes_sum, key=classes_sum.get)
        majorityClass_arr.append(classes_sum.get(majority_class))

    purity = (1/2225) * sum(majorityClass_arr)
    return purity

def docID_format(id):
    new_id = ""
    if (id <= 9):
        new_id = "00" + str(id)
    elif (id > 9 and id <= 99):
        new_id = "0" + str(id)
    else:
        new_id = str(id)
    return new_id

def print_cluster_docs(user_select,cluster_docIDs):
    # id 1-510 | class (0-509)
    business_path = "bbc-fulltext/bbc/business"
    # id 511-896 | class (510-895) | 001-386 --> -510
    entertainment_path = "bbc-fulltext/bbc/entertainment"
    # id 897-1313 | class (896-1312) | --> -896
    politics_path = "bbc-fulltext/bbc/politics"
    # id 1314-1824 | class (1313-1823) | --> -1313
    sport_path = "bbc-fulltext/bbc/sport"
    # id 1825-2225 | class (1824-2224) | --> -1824
    tech_path = "bbc-fulltext/bbc/tech"

    # centroid : {c : [docID1, docID2]}
    print(user_select,cluster_docIDs.get(user_select))
    selected_cluster = cluster_docIDs.get(user_select)
    for i in range(len(selected_cluster)):
        if (selected_cluster[i] > 0 and selected_cluster[i] <= 510):
            doc_class = "business"
            id = selected_cluster[i]
            path = business_path + "/" + docID_format(id) + ".txt"
        elif (selected_cluster[i] > 510 and selected_cluster[i] <= 896):
            doc_class = "entertainment"
            id = selected_cluster[i] - 510
            path = entertainment_path + "/" + docID_format(id) + ".txt"
        elif (selected_cluster[i] > 896 and selected_cluster[i] <= 1313):
            doc_class = "politics"
            id = selected_cluster[i] - 896
            path = politics_path + "/" + docID_format(id) + ".txt"
        elif (selected_cluster[i] > 1313 and selected_cluster[i] <= 1824):
            doc_class = "sport"
            id = selected_cluster[i] - 1313
            path = sport_path + "/" + docID_format(id) + ".txt"
        else:
            doc_class = "tech"
            id = selected_cluster[i] - 1824
            path = tech_path + "/" + docID_format(id) + ".txt"
        
        doc_title = open(path).readline().strip()
        print("docID: " +  str(selected_cluster[i]) + " | title: " + doc_title + " | class: " + doc_class)

def top_5_terms(user_select, cluster_term_weights):
    # add the tfidf values of a term from all the documents in that cluster
    # selected_clus {centroid_doc_id : {term_id : weight}}

    terms_path = "bbc/bbc.terms"
    bbc_terms = open(terms_path,"r")
    termID_term = {}

    iter=1
    for i in bbc_terms.readlines():
        termID_term[iter] = i.strip()
        iter+=1
    
    selected_clus = cluster_term_weights.get(user_select)
    sorted_by_weights = sorted(selected_clus.items(), key=lambda x:x[1],reverse=True)

    print("Top 5 terms with highest TF-IDF (weight) values:")
    i=1
    for termID,weight in sorted_by_weights:
        print(str(i) + ". " + termID_term.get(int(termID)) + " | weight: " + str(weight))
        if i==5:
            break
        i+=1

def run(doc_term_weights):
    print ("Please enter a K-value.")
    while True:
        try:
            user_k = int(input())
            break
        except ValueError:
            print("Please enter a valid integer for the K value.")

    print("Running K-means...")
    cluster_docIDs, cluster_term_weights = k_means(user_k, doc_term_weights, tolerance=1e-4, max_iterations=100)
    
    cluster_display = "Choose a cluster: \n"
    for i in range(user_k):
        if (i+1==user_k):
            cluster_display += "C" + str(i+1)
        else:
            cluster_display += "C" + str(i+1) + ", "
    print(cluster_display)

    while True:
        try:
            selected_cluster = input().lower()
            if selected_cluster == "end":
                break
            selected_cluster = int(selected_cluster)
            if (selected_cluster > user_k):
                print("Please enter a valid integer that is less than or equal to " + str(user_k) + ".")
            else:
                print_cluster_docs(selected_cluster-1, cluster_docIDs)
                top_5_terms(selected_cluster-1, cluster_term_weights)
        except ValueError:
            print("Please enter a valid integer.")
        print(cluster_display)

    print("Purity:", purity(cluster_docIDs))
    print(internal_criteria(cluster_docIDs,doc_term_weights,doc_term_weights))

def main():
    path = "bbc/bbc.mtx"
    doc_term_weights = get_weights(path)
    run(doc_term_weights)

if __name__ == "__main__":
    main()


