import os
import sys
import pickle
import pandas as pd
import numpy as np
import mlxtend.frequent_patterns # https://github.com/rasbt/mlxtend/blob/master/mlxtend/frequent_patterns/apriori.py


INTERESTED_CATEGORICAL_COLS = ['BORO_NM', 'LAW_CAT_CD', 'OFNS_DESC', 'PATROL_BORO', 'PREM_TYP_DESC', 'SUSP_AGE_GROUP', 'SUSP_RACE', 'SUSP_SEX', 'VIC_AGE_GROUP', 'VIC_RACE', 'VIC_SEX']

def generate_baskets(df, interested_columns):
    baskets = []
    for i, row in df.iterrows():
        basket = set(f'{col} / {row[col]}' for col in interested_columns if row[col] != 'UNKNOWN')
        baskets.append(basket)
    return baskets


def save_baskets(baskets, filename='baskets.pkl'):
    with open(filename, 'wb') as f:
        pickle.dump(baskets, f)


def load_baskets(filename='baskets.pkl'):
    if os.path.exists(filename):
        with open(filename, 'rb') as f:
            return pickle.load(f)
    return None

def apriori_gen(Lk_minus_1, k):
    """Generate Ck from Lk-1."""
    Ck = []
    
    # Join step
    for i in range(len(Lk_minus_1)):
        for j in range(i + 1, len(Lk_minus_1)):
            L1 = list(Lk_minus_1[i])
            L2 = list(Lk_minus_1[j])
            L1.sort()
            L2.sort()
            if L1[:-1] == L2[:-1] and L1[-1] < L2[-1]:  # ensure the first k-2 items are the same and the last items are in order
                candidate = frozenset(L1 + [L2[-1]])
                # Prune step
                if all(frozenset(candidate - {item}) in Lk_minus_1 for item in candidate):
                    Ck.append(candidate)
    return Ck


def apriori(baskets, min_sup):
    """Apriori algorithm to find all frequent itemsets."""
    total_baskets = len(baskets)
    # Initial pass to count individual items
    item_counts = {}
    for basket in baskets:
        for item in basket:
            item_counts[item] = item_counts.get(item, 0) + 1

    # Generate L1 from single item counts
    L1 = [frozenset([item]) for item, count in item_counts.items() if count / total_baskets >= min_sup]
    L = [L1] if L1 else []
    k = 2

    while L and k-2 < len(L):
        Ck = apriori_gen(L[k-2], k)
        item_counts = {itemset: 0 for itemset in Ck}
        for basket in baskets:
            for itemset in Ck:
                if itemset.issubset(basket):
                    item_counts[itemset] += 1
        
        Lk = [itemset for itemset, count in item_counts.items() if count / total_baskets >= min_sup]
        if Lk:
            L.append(Lk)
        k += 1
    return [item for sublist in L for item in sublist]  


def main():
    if len(sys.argv) != 4:
        print("Usage: python3 main.py <file_name> <min_sup> <min_conf>")
        return
    file_name, min_sup, min_conf = sys.argv[1], float(sys.argv[2]), float(sys.argv[3])

    if min_sup <= 0.0:
        raise ValueError(
            "`min_support` must be a positive number in the range of `(0, 1]`. "
        )
    encoded_df = pd.read_csv("encoded_data.csv")

    baskets = load_baskets() # save and load for convenience
    if baskets is None:
        df = pd.read_csv(file_name)
        baskets = generate_baskets(df, INTERESTED_CATEGORICAL_COLS)
        save_baskets(baskets)
    frequent_itemsets = apriori(baskets, min_sup)
    # frequent_itemsets = mlxtend.frequent_patterns.apriori(encoded_df, min_sup, use_colnames=True)['itemsets'] # for comparison

    print("Frequent Itemsets:")
    for itemset in frequent_itemsets:
        print(itemset)


if __name__ == "__main__":
    main()