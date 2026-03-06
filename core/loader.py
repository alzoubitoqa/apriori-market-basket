from __future__ import annotations
from typing import List, Set, Optional
import os
import pandas as pd


def _split_items(s: str) -> Set[str]:
    items = {x.strip() for x in str(s).split(",") if x and str(x).strip()}
    return items


def load_transactions(
    file_path: Optional[str] = None,
    uploaded_file=None,
    items_col: str = "items",
) -> List[Set[str]]:
    """
    يحمل معاملات (Transactions) من:
    - مسار ملف (CSV أو XLSX)
    - أو ملف مرفوع من Streamlit (uploaded_file)

    صيغة البيانات المتوقعة الأفضل:
      عمود اسمه 'items' يحتوي عناصر مفصولة بفواصل مثل: milk,bread,butter

    أو One-Hot:
      أعمدة كثيرة 0/1 لكل عنصر.
    """
    if uploaded_file is None and file_path is None:
        raise ValueError("يجب تمرير file_path أو uploaded_file")

 
    if uploaded_file is not None:
        name = (uploaded_file.name or "").lower()
        if name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        elif name.endswith(".xlsx") or name.endswith(".xls"):
            df = pd.read_excel(uploaded_file)
        else:
            raise ValueError("الملف يجب أن يكون CSV أو Excel")
    else:
        ext = os.path.splitext(file_path)[1].lower()
        if ext == ".csv":
            df = pd.read_csv(file_path)
        elif ext in (".xlsx", ".xls"):
            df = pd.read_excel(file_path)
        else:
            raise ValueError("الملف يجب أن يكون CSV أو Excel")


    if items_col in df.columns:
        tx: List[Set[str]] = []
        for raw in df[items_col].fillna("").astype(str):
            items = _split_items(raw)
            if items:
                tx.append(items)
        return tx


    tx: List[Set[str]] = []
    for _, row in df.iterrows():
        items = set()
        for col in df.columns:
            val = str(row[col]).strip()
            if val in {"1", "1.0", "True", "true", "YES", "Yes"}:
                items.add(str(col).strip())
        if items:
            tx.append(items)
    return tx






