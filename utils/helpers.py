from __future__ import annotations
from typing import Dict, FrozenSet, List
import pandas as pd

Itemset = FrozenSet[str]


def supports_to_dataframe(supports: Dict[Itemset, float], counts: Dict[Itemset, int]) -> pd.DataFrame:
    rows: List[dict] = []
    for iset, sup in supports.items():
        rows.append({
            "itemset": ", ".join(sorted(iset)),
            "size": len(iset),
            "support": round(sup, 4),
            "count": counts.get(iset, 0),
        })
    if not rows:
        return pd.DataFrame(columns=["itemset", "size", "support", "count"])
    df = pd.DataFrame(rows)
    return df.sort_values(["size", "support"], ascending=[True, False]).reset_index(drop=True)




    \

    