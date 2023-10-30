import itertools
from collections import defaultdict

# 從文件中讀取資料
def load_data(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        data = []
        for line in f:
            # 移除多餘的空白和特殊字符
            line = line.strip().replace('\u200b', '')
            # 將每行資料轉換為整數集合
            transaction = set(map(int, line.split()))
            data.append(transaction)
    return data

# 獲取頻繁項集
def get_frequent_itemsets(data, min_support):
    single_items = defaultdict(int)

    # 計算每個物品的出現次數
    for transaction in data:
        for item in transaction:
            single_items[frozenset([item])] += 1

    # 計算交易的總數
    num_transactions = len(data)
    # 移除低於最小支持度的物品
    single_items = {k: v for k, v in single_items.items() if v/num_transactions >= min_support}

    # 裁剪候選項集
    def prune_candidates(candidates, prev_frequent):
        pruned = []
        for itemset in candidates:
            all_subsets = list(itertools.combinations(itemset, len(itemset)-1))
            if all(frozenset(sub) in prev_frequent for sub in all_subsets):
                pruned.append(itemset)
        return pruned

    # 計算候選項集的支持度
    def count_candidates(data, candidates):
        count = defaultdict(int)
        for transaction in data:
            for candidate in candidates:
                if set(candidate).issubset(transaction):
                    count[frozenset(candidate)] += 1
        return count

    # 計算所有的頻繁項集
    frequent_itemsets = [single_items]
    while frequent_itemsets[-1]:
        next_size = len(list(frequent_itemsets[-1].keys())[0]) + 1
        next_candidates = list(itertools.combinations(set().union(*frequent_itemsets[-1].keys()), next_size))
        next_candidates = prune_candidates(next_candidates, frequent_itemsets[-1])

        counts = count_candidates(data, next_candidates)
        counts = {k: v for k, v in counts.items() if v/num_transactions >= min_support}
        frequent_itemsets.append(counts)

    return {k: v for freq in frequent_itemsets for k, v in freq.items()}

# 根據頻繁項集獲取關聯規則
def get_rules(frequent_itemsets, min_confidence):
    rules = []
    for itemset, support in frequent_itemsets.items():
        for size in range(1, len(itemset)):
            lhs_candidates = itertools.combinations(itemset, size)
            for lhs in lhs_candidates:
                rhs_set = frozenset(itemset) - frozenset(lhs)
                
                lhs_count = frequent_itemsets[frozenset(lhs)]
                confidence_ratio = (support, lhs_count)
                
                if support / lhs_count >= min_confidence:
                    rules.append((set(lhs), set(itemset) - set(lhs), confidence_ratio))
    return rules

def sorted_join(items):
    return ', '.join(sorted(items, key=int))

# 寫入規則到文件
def write_output(rules, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        for lhs, rhs, conf_ratio in rules:
            lhs_str = sorted_join(map(str, lhs))
            rhs_str = sorted_join(map(str, rhs))
            f.write(f"{lhs_str} -> {rhs_str} ({conf_ratio[0]}/{conf_ratio[1]})\n")

# 主函式
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="在交易資料中發現關聯規則。")
    parser.add_argument("input_data", help="輸入資料文件的路徑。")
    parser.add_argument("min_support", type=float, help="最小支持度。")
    parser.add_argument("min_confidence", type=float, help="最小信賴度。")
    args = parser.parse_args()

    data = load_data(args.input_data)
    frequent_itemsets = get_frequent_itemsets(data, args.min_support)
    rules = get_rules(frequent_itemsets, args.min_confidence)
    write_output(rules, "output_rules.txt")
