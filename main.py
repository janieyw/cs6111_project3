import os
import sys
import pickle
import pandas as pd


INTERESTED_CATEGORICAL_COLS = ['BORO_NM', 'LAW_CAT_CD', 'OFNS_DESC', 'PATROL_BORO', 'PREM_TYP_DESC', 'SUSP_AGE_GROUP', 'SUSP_RACE', 'SUSP_SEX', 'VIC_AGE_GROUP', 'VIC_RACE', 'VIC_SEX']

def generate_baskets(df, interested_columns):
    """Create baskets from df"""
    baskets = []
    for i, row in df.iterrows():
        basket = set(f'{col} / {row[col]}' for col in interested_columns if row[col] != 'UNKNOWN')
        baskets.append(basket)
    return baskets


def save_baskets(baskets, filename='baskets.pkl'):
    """Save the generated baskets to a pickle file, which is purely for convenience in case of multiple generations"""
    with open(filename, 'wb') as f:
        pickle.dump(baskets, f)


def load_baskets(filename='baskets.pkl'):
    """Load baskets from a pickle file if it exists"""
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
    L1 = [(frozenset([item]), count / total_baskets) for item, count in item_counts.items() if count / total_baskets >= min_sup]
    L = [[], L1] # Initialize L to store all levels of frequent itemsets; start with L1
    k = 2 # Start looking for pairs of items

    while L[-1]: # Continue until no more frequent itemsets are found
        Ck = apriori_gen([x[0] for x in L[k-1]], k) # Generate candidate itemsets from the last level of frequent itemsets
        item_counts = {itemset: 0 for itemset in Ck} # Initialize counts for candidate itemsets
        for basket in baskets:
            for itemset in Ck:
                if itemset.issubset(basket): # Check if the candidate itemset is in the basket
                    item_counts[itemset] += 1
        
        # Filter candidates to find frequent itemsets at level k
        Lk = [(itemset, count / total_baskets) for itemset, count in item_counts.items() if count / total_baskets >= min_sup]
        L.append(Lk) # Add new level to L
        k += 1 # Increment to search for larger sets
    return sorted(sum(L, []), key=lambda x: x[1], reverse=True)

def get_all_subsets(items):
    """Generates all possible subsets of a given itemset, excluding the empty set."""
    items = list(items)
    current = set()
    subsets = []
    def _recur(i, current):
        """Recursive helper function to generate subsets."""
        if i == len(items):
            if current:
                subsets.append(list(current))
            return
        _recur(i+1, current) # Explore the subset without the current item
        current.add(items[i])
        _recur(i+1, current) # Explore the subset with the current item
        current.remove(items[i])
    _recur(0, current)
    return subsets

def get_association_rules(frequent_itemsets, min_conf):
    """Generate all high-confidence association rules from the frequent itemsets."""
    # output format: [(lhs, rhs, conf, support)]
    sup_map = {frozenset(x[0]): x[1] for x in frequent_itemsets}
    rules = []
    checked_rels = set() # set((lhs, rhs)) # Set to track already evaluated rule combinations
    for itemset, sup in frequent_itemsets:
        if len(itemset) < 2: # Only consider itemsets with at least two items
            continue
        for rhs in itemset:
            for lhs in get_all_subsets(itemset - set([rhs])):
                if (frozenset(lhs), rhs) in checked_rels:
                    continue
                conf = sup_map[frozenset([rhs] + lhs)] / sup_map[frozenset(lhs)]
                if conf >= min_conf:
                    rules.append((lhs, rhs, conf, sup_map[frozenset([rhs] + lhs)])) # Add rule if it meets the confidence threshold
                checked_rels.add((frozenset(lhs), rhs))
    return sorted(rules, key=lambda x: x[2], reverse=True) # Return rules sorted by confidence

def main():
    if len(sys.argv) != 4:
        print("Usage: python3 main.py <file_name> <min_sup> <min_conf>")
        return
    file_name, min_sup, min_conf = sys.argv[1], float(sys.argv[2]), float(sys.argv[3])

    # Ensure user input validity
    if min_sup <= 0 or min_sup > 1:
        raise ValueError("`min_support` must be a positive number in the range of (0, 1].")
    if min_conf <= 0 or min_conf > 1:
        raise ValueError("`min_confidence` must be a positive number in the range of (0, 1].")

    baskets = load_baskets() # save and load for convenience
    if baskets is None:
        df = pd.read_csv(file_name)
        baskets = generate_baskets(df, INTERESTED_CATEGORICAL_COLS)
        save_baskets(baskets)
    frequent_itemsets = apriori(baskets, min_sup)
    
    # Redirect the standard output to a file
    original_stdout = sys.stdout
    with open('output.txt', 'w') as f:
        sys.stdout = f

        print(f"==Frequent itemsets (min_sup={min_sup * 100}%)")
        for itemset, support in frequent_itemsets:
            print(f"{list(itemset)}, {support * 100:.4f}%")
        
        association_rules = get_association_rules(frequent_itemsets, min_conf)
        print(f"==High-confidence association rules (min_conf={min_conf * 100}%)")
        for lhs, rhs, conf, supp in association_rules:
            print(f"{lhs} => [{rhs}] (Conf: {conf * 100:.4f}%, Supp: {supp * 100:.4f}%)")

        sys.stdout = original_stdout

    print("Output has been saved to output.txt.")    


if __name__ == "__main__":
    main()
