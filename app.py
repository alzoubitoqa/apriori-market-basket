import os
import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt

from core.loader import load_transactions
from core.apriori import apriori_frequent_itemsets
from core.rules import generate_rules
from utils.helpers import supports_to_dataframe


st.set_page_config(page_title="Apriori Demo", page_icon="🧺", layout="wide")
st.title("🧺 Apriori Market Basket Analyzer")

st.write("يرفع CSV/Excel، ثم يطلع Frequent Itemsets و Association Rules مع رسم شبكة العلاقات.")

# =========================
# Sidebar Settings
# =========================
with st.sidebar:
    st.header("Settings")

    min_support = st.slider("Min support", 0.01, 0.90, 0.10, 0.01)
    min_conf = st.slider("Min confidence", 0.05, 0.99, 0.60, 0.05)
    max_k = st.slider("Max itemset size (k)", 2, 6, 4, 1)

    st.divider()
    st.caption("صيغة CSV المفضلة:")
    st.code("items\nmilk,bread,butter\nbeer,diapers,bread", language="text")

# =========================
# File Upload
# =========================
uploaded = st.file_uploader("Upload CSV أو Excel", type=["csv", "xlsx", "xls"])

default_path_csv = os.path.join("data", "transactions.csv")
default_path_xlsx = os.path.join("data", "transactions.xlsx")

transactions = None

try:
    if uploaded is not None:
        transactions = load_transactions(uploaded_file=uploaded)
        st.success(f"تم تحميل {len(transactions)} معاملة من الملف المرفوع.")
    else:
        if os.path.exists(default_path_csv):
            transactions = load_transactions(file_path=default_path_csv)
            st.info(f"لا يوجد ملف مرفوع — تم استخدام {default_path_csv} وفيه {len(transactions)} معاملة.")
        elif os.path.exists(default_path_xlsx):
            transactions = load_transactions(file_path=default_path_xlsx)
            st.info(f"لا يوجد ملف مرفوع — تم استخدام {default_path_xlsx} وفيه {len(transactions)} معاملة.")
        else:
            st.warning("ارفعي ملف CSV/Excel أو ضعي ملف داخل data باسم transactions.csv أو transactions.xlsx")
            st.stop()

except Exception as e:
    st.error(f"خطأ بقراءة البيانات: {e}")
    st.stop()

if not transactions:
    st.error("لم يتم العثور على معاملات صالحة داخل الملف.")
    st.stop()

# =========================
# Apriori
# =========================
supports, counts = apriori_frequent_itemsets(
    transactions,
    min_support=min_support,
    max_k=max_k
)

# =========================
# Frequent Itemsets
# =========================
st.subheader("1) Frequent Itemsets")

if not supports:
    st.warning("لم يتم العثور على Frequent Itemsets. جرّبي تقليل Min support.")
else:
    itemsets_df = supports_to_dataframe(supports, counts)
    st.dataframe(itemsets_df, use_container_width=True)

# =========================
# Association Rules
# =========================
st.subheader("2) Association Rules")

rules_df = generate_rules(supports, min_confidence=min_conf)

if rules_df.empty:
    st.warning("لم يتم العثور على Rules. جرّبي تقليل Min confidence أو Min support.")
else:
    st.dataframe(rules_df, use_container_width=True)

# =========================
# Network Graph
# =========================
st.subheader("3) Network Graph (Top Rules)")

if rules_df.empty:
    st.info("لا يوجد Rules لرسمها. جرّبي تقليل Min support أو Min confidence.")
else:
    col1, col2 = st.columns([1, 2])

    with col1:
        top_n = st.slider("عدد القواعد المراد رسمها", 5, 50, 15, 1)
        sort_by = st.selectbox("ترتيب القواعد حسب", ["lift", "confidence", "support"], index=0)

    top_rules = rules_df.sort_values(sort_by, ascending=False).head(top_n)

    G = nx.DiGraph()

    for _, row in top_rules.iterrows():
        antecedent = row["antecedent"]
        consequent = row["consequent"]
        G.add_edge(
            antecedent,
            consequent,
            lift=float(row["lift"]),
            confidence=float(row["confidence"]),
            support=float(row["support"])
        )

    fig, ax = plt.subplots(figsize=(12, 7))
    pos = nx.spring_layout(G, seed=42, k=1.0)

    nx.draw_networkx_nodes(G, pos, ax=ax, node_size=2000)
    nx.draw_networkx_labels(G, pos, ax=ax, font_size=9)
    nx.draw_networkx_edges(G, pos, ax=ax, arrows=True, arrowstyle="->", width=1.8)

    edge_labels = {
        (u, v): f"lift={d['lift']:.2f}"
        for u, v, d in G.edges(data=True)
    }
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, ax=ax, font_size=8)

    ax.set_axis_off()
    st.pyplot(fig)

    st.caption("كل سهم يمثل Rule من antecedent إلى consequent، والقيمة المكتوبة على السهم هي Lift.")