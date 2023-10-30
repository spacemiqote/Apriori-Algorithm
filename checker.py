from efficient_apriori import apriori
import argparse

# 載入數據
def load_data(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        data = []
        for line in f:
            line = line.strip().replace('\u200b', '')
            transaction = tuple(line.split())
            data.append(transaction)
    return data

# 匹配和比較兩個規則集
def compare_rules(ours, efficient_apriori):
    our_rules = set()
    with open(ours, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            our_rules.add(line)

    apriori_rules = set()
    for rule in efficient_apriori:
        lhs = ', '.join(rule.lhs)
        rhs = ', '.join(rule.rhs)
        absolute_support_lhs = int(rule.support * len(transactions) / rule.confidence)
        conf_ratio = (int(rule.support * len(transactions)), absolute_support_lhs)
        apriori_rules.add(f"{lhs} -> {rhs} ({conf_ratio[0]}/{conf_ratio[1]})")
    
    unmatched_from_ours = our_rules - apriori_rules
    unmatched_from_apriori = apriori_rules - our_rules

    print(f"不吻合的規則(簡單版實踐): {len(unmatched_from_ours)}")
    for rule in unmatched_from_ours:
        print(rule)
    
    print(f"\n不吻合的規則(efficient_apriori): {len(unmatched_from_apriori)}")
    for rule in unmatched_from_apriori:
        print(rule)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="檢查演算法正確性的腳本")
    parser.add_argument("input_data", help="測試用的資料檔名")
    parser.add_argument("min_support", type=float, help="最小支持度")
    parser.add_argument("min_confidence", type=float, help="最小自信度")
    parser.add_argument("output_data", help="我們簡單版的輸出規則檔名")
    args = parser.parse_args()

    transactions = load_data(args.input_data)
    itemsets, rules = apriori(transactions, min_support=args.min_support, min_confidence=args.min_confidence)
    compare_rules(args.output_data, rules)
