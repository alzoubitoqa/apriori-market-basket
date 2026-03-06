🧺 Apriori Market Basket Analyzer


📌 Project Overview

This project implements the Apriori algorithm to perform Market Basket Analysis on transactional datasets.
The goal is to discover frequent itemsets and generate association rules that reveal relationships between products purchased together.

The application is built using Python and provides an interactive web interface using Streamlit.

It allows users to:

Upload transactional datasets (CSV or Excel)

Discover frequent itemsets

Generate association rules

Measure rule strength using Support, Confidence, and Lift

Visualize relationships between products using a Network Graph

⚙️ Technologies Used

Python

Streamlit

Pandas

NetworkX

Matplotlib

📂 Project Structure
apriori-market-basket
│
├── .venv
│
├── core
│   ├── apriori.py
│   ├── loader.py
│   └── rules.py
│
├── data
│   └── transactions.csv
│
├── utils
│   └── helpers.py
│
├── app.py
├── calc_metrics.py
├── README.md
└── requirements.txt
📊 Dataset Format

The dataset must contain a column named items, where each row represents a transaction.

Example:

items
milk,bread,butter
beer,diapers,bread
milk,diapers,beer,bread
chips,soda
pasta,tomato_sauce

Each row represents one customer purchase.

🔎 Apriori Algorithm

The Apriori algorithm is used to identify frequent itemsets within transactional data.

It works by:

Identifying items that appear frequently in transactions

Expanding them into larger item combinations

Filtering combinations based on minimum support

After frequent itemsets are discovered, association rules are generated.

Example rule:

cereal → milk

Meaning:

Customers who purchase cereal are highly likely to also purchase milk.

📏 Evaluation Metrics

The strength of association rules is evaluated using three metrics:

1️⃣ Support

Measures how frequently an itemset appears in the dataset.

Support(A ∪ B) = Transactions containing A and B / Total transactions
2️⃣ Confidence

Measures how often item B appears in transactions that contain A.

Confidence(A → B) = Support(A ∪ B) / Support(A)
3️⃣ Lift

Measures how much more likely B is purchased when A is purchased.

Lift(A → B) = Confidence(A → B) / Support(B)

Interpretation:

Lift > 1 → Positive relationship

Lift = 1 → Independent items

Lift < 1 → Negative relationship

📈 Visualization

The project includes a network graph visualization that represents association rules.

Each node represents a product

Each edge represents a rule

Edge labels display the lift value

Example:

cereal ─────► milk
lift = 4.49

This indicates a strong relationship between cereal and milk purchases.

🚀 Installation

Clone the repository:

git clone https://github.com/alzoubitoqa/apriori-market-basket.git

cd apriori-market-basket

python -m venv .venv

.venv\Scripts\activate

pip install -r requirements.txt

streamlit run app.py

The application will open in your browser:

http://localhost:8501
📊 Application Features

The application allows users to:

Upload transactional datasets

Adjust minimum support

Adjust minimum confidence

Control maximum itemset size

View frequent itemsets

Explore association rules

Visualize product relationships

📌 Example Output

Frequent Itemsets:

Item	Support
butter	0.212
milk	0.182
soda	0.178

Association Rule:

cereal → milk
Support: 0.108
Confidence: 0.818
Lift: 4.49

This indicates a strong purchasing relationship between cereal and milk.

🎯 Use Cases

Market basket analysis is widely used in:

Retail recommendation systems

E-commerce product suggestions

Store layout optimization

Cross-selling strategies

Customer behavior analysis

📚 References

Agrawal, R., & Srikant, R. (1994). Fast algorithms for mining association rules.

Tan, Steinbach, Kumar — Introduction to Data Mining

Han, Kamber, Pei — Data Mining: Concepts and Techniques

👩‍💻 Author

**Toqa Mahmoud Tawfiq Al-Zoubi**

GitHub: https://github.com/alzoubitoqa













