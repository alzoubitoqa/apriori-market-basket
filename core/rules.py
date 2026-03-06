from __future__ import annotations
import itertools
from typing import Dict, FrozenSet
import pandas as pd

Itemset = FrozenSet[str]


def generate_rules(
    supports: Dict[Itemset, float],
    min_confidence: float
) -> pd.DataFrame:
    """
    يولّد Association Rules من الـ frequent itemsets.
    المقاييس:
      support(S)
      confidence(A->B) = support(S) / support(A)
      lift(A->B) = confidence / support(B)
    """
    rows = []

    for itemset, sup_s in supports.items():
        if len(itemset) < 2:
            continue

        items = list(itemset)
        for r in range(1, len(items)):
            for antecedent_tuple in itertools.combinations(items, r):
                A = frozenset(antecedent_tuple)
                B = itemset - A

                sup_a = supports.get(A)
                sup_b = supports.get(B)
                if not sup_a or not sup_b:
                    continue

                confidence = sup_s / sup_a
                if confidence + 1e-12 < min_confidence:
                    continue

                lift = confidence / sup_b

                rows.append({
                    "antecedent": ", ".join(sorted(A)),
                    "consequent": ", ".join(sorted(B)),
                    "support": round(sup_s, 4),
                    "confidence": round(confidence, 4),
                    "lift": round(lift, 4),
                    "itemset_size": len(itemset),
                })

    df = pd.DataFrame(rows)
    if df.empty:
        return df
    return df.sort_values(["lift", "confidence", "support"], ascending=False).reset_index(drop=True)









    