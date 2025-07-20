# Cognitive Map Graph Construction for Bipolar Disorder Knowledge Extraction

This project transforms unstructured medical text on **bipolar disorder** into structured knowledge using **Natural Language Processing (NLP)**, **ChatGPT**, and **Cognitive Map Graphs (CMGs)**. The structured data is visualized and analyzed using tools like **Neo4j** and **NetworkX**, aiming to support more accurate and scalable decision-making in mental health.

---

## 📘 Abstract

Bipolar disorder presents complex challenges in diagnosis and treatment due to its varied symptoms and triggers. This project uses Cognitive Map Graphs (CMGs) and advanced NLP techniques to convert unstructured medical text into structured, graph-based knowledge. Using ChatGPT for key information extraction and structuring, the system maps relationships such as symptoms, treatments, and outcomes. The resulting knowledge graphs improve interpretability and enable AI-driven clinical decision support.

---

## 🧠 Key Features

- 🔍 **Data Collection**: Scrapes and curates data from MSD Manuals and medical articles.
- 🧹 **Data Cleaning**: Removes multimedia content, standardizes formatting, and organizes text.
- 🤖 **NLP Processing**:
  - Paragraph segmentation
  - Key-point summarization
  - Triplet extraction (`head`, `relation`, `tail`) using ChatGPT
- 🧭 **Graph Construction**:
  - Neo4j: For scalable and interactive visualizations
  - NetworkX: For lightweight local graph construction and subset analysis
- 📊 **Prompt Engineering**: Refined prompts to increase domain-specific relation accuracy from 271 to 528.

---

## 🧰 Tech Stack

- Python 3.10+
- OpenAI (ChatGPT API)
- Neo4j (Community Edition)
- NetworkX
- Pandas
- Matplotlib
- Jupyter Notebooks

---

## 📁 Project Structure

```
bipolar-nlp-graph-project/
├── final_report/
│   └── s4680495_Final_Report.pdf
├── data/
│   └── articles.xlsx
│   └── cleaned_data.csv
├── notebooks/
│   └── 01_data_cleaning.ipynb
│   └── 02_chatgpt_extraction.ipynb
│   └── 03_graph_creation.ipynb
├── scripts/
│   └── chatgpt_prompting.py
│   └── neo4j_export.py
├── README.md
├── requirements.txt
```

---

## 🚀 Getting Started

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/bipolar-nlp-graph-project.git
   cd bipolar-nlp-graph-project
   ```

2. Create a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Setup OpenAI API Key:
   ```bash
   export OPENAI_API_KEY=your_key_here
   ```

4. Launch notebooks or run scripts as needed.

---

## 📸 Sample Outputs

### 📌 Knowledge Triplet Format:
```
Head: Manic Episodes
Relation: involve
Tail: elevated mood, increased activity, impulsive behavior
```

### 🧠 Graph Visualizations:
- ✅ Neo4j: Full graph with 500+ relationships
- ✅ NetworkX: Subgraph with interactive layout

---


---

## 🙌 Acknowledgements

- Medical content source: MSD Manuals
- Powered by: OpenAI, Neo4j, NetworkX

---

