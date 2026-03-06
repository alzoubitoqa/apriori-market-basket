import pandas as pd
import itertools
from collections import defaultdict

# ======================
# إعدادات
# ======================
CSV_PATH = "data/transactions.csv"   # عدّلي المسار إذا ملفك بمكان مختلف
MIN_SUPPORT = 0.05
MIN_CONFIDENCE = 0.50
MAX_K = 4   # أقصى حجم itemset

# ======================
# قراءة البيانات
# ======================
df = pd.read_csv(CSV_PATH)

transactions = []
for s in df["items"].fillna("").astype(str):
    items = {x.strip() for x in s.split(",") if x.strip()}
    if items:
        transactions.append(items)

n = len(transactions)
print(f"Loaded {n} transactions")

# ======================
# Apriori (Frequent Itemsets)
# ======================
def support_count(candidates):
    counts = {c: 0 for c in candidates}
    for t in transactions:
        for c in counts:
            if c.issubset(t):
                counts[c] += 1
    return counts

supports = {}
counts = {}

# L1
item_counts = defaultdict(int)
for t in transactions:
    for item in t:
        item_counts[frozenset([item])] += 1

L = set()
for it, c in item_counts.items():
    sup = c / n
    if sup >= MIN_SUPPORT:
        L.add(it)
        supports[it] = sup
        counts[it] = c

k = 2
while L and k <= MAX_K:
    prev = sorted(L)
    candidates = set()

    for i in range(len(prev)):
        for j in range(i + 1, len(prev)):
            union = prev[i] | prev[j]
            if len(union) == k:
                ok = all(frozenset(sub) in L for sub in itertools.combinations(union, k - 1))
                if ok:
                    candidates.add(union)

    if not candidates:
        break

    cand_counts = support_count(candidates)
    L_next = set()

    for cset, ccount in cand_counts.items():
        sup = ccount / n
        if sup >= MIN_SUPPORT:
            L_next.add(cset)
            supports[cset] = sup
            counts[cset] = ccount

    L = L_next
    k += 1

print(f"Frequent itemsets found: {len(supports)}")

# ======================
# توليد القواعد + حساب المقاييس
# ======================
rules = []

for itemset, sup_s in supports.items():
    if len(itemset) < 2:
        continue

    items = list(itemset)
    for r in range(1, len(items)):
        for A_tuple in itertools.combinations(items, r):
            A = frozenset(A_tuple)
            B = itemset - A

            sup_a = supports.get(A)
            sup_b = supports.get(B)
            if not sup_a or not sup_b:
                continue

            confidence = sup_s / sup_a
            if confidence < MIN_CONFIDENCE:
                continue

            lift = confidence / sup_b

            rules.append({
                "antecedent": ", ".join(sorted(A)),
                "consequent": ", ".join(sorted(B)),
                "support": round(sup_s, 4),
                "confidence": round(confidence, 4),
                "lift": round(lift, 4),
                "count_AB": counts[itemset],
                "count_A": counts[A],
                "count_B": counts[B],
            })

rules_df = pd.DataFrame(rules)

if rules_df.empty:
    print("No rules found. Try lowering MIN_SUPPORT or MIN_CONFIDENCE.")
else:
    rules_df = rules_df.sort_values(["lift", "confidence", "support"], ascending=False)
    print("\nTop 10 rules by lift:\n")
    print(rules_df.head(10).to_string(index=False))

    # حفظ النتائج كملف
    out_path = "rules_results.csv"
    rules_df.to_csv(out_path, index=False)
    print(f"\nSaved all rules to: {out_path}")









    