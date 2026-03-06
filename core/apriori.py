from __future__ import annotations
import itertools
from collections import defaultdict
from typing import Dict, FrozenSet, Iterable, List, Set, Tuple

Itemset = FrozenSet[str]


def support_count(transactions: List[Set[str]], candidates: Iterable[Itemset]) -> Dict[Itemset, int]:
    counts = {c: 0 for c in candidates}
    for t in transactions:
        for c in counts.keys():
            if c.issubset(t):
                counts[c] += 1
    return counts


def apriori_frequent_itemsets(
    transactions: List[Set[str]],
    min_support: float,
    max_k: int = 4
) -> Tuple[Dict[Itemset, float], Dict[Itemset, int]]:
    """
    يرجّع:
      supports: itemset -> support (0..1)
      counts:   itemset -> count
    """
    n = len(transactions)
    if n == 0:
        return {}, {}

    item_counts = defaultdict(int)
    for t in transactions:
        for item in t:
            item_counts[frozenset([item])] += 1

    supports: Dict[Itemset, float] = {}
    counts: Dict[Itemset, int] = {}

    L = set()
    for it, c in item_counts.items():
        s = c / n
        if s >= min_support:
            L.add(it)
            supports[it] = s
            counts[it] = c

    k = 2
    while L and k <= max_k:
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

        cand_counts = support_count(transactions, candidates)

        L_next = set()
        for cset, ccount in cand_counts.items():
            s = ccount / n
            if s >= min_support:
                L_next.add(cset)
                supports[cset] = s
                counts[cset] = ccount

        L = L_next
        k += 1

    return supports, counts









