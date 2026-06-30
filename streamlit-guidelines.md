# Guideline for Converting My Jupyter Notebook into a Streamlit Application

## Objective

Convert the existing Jupyter Notebook into a maintainable Streamlit web application while preserving all scientific calculations.

The Streamlit application should:

* Allow users to upload their own CSV files.
* Include example CSV datasets stored in the GitHub repository.
* Produce the same calculations as the notebook.
* Display interactive figures and tables.
* Allow users to download calculation results.
* Be deployable on Streamlit Community Cloud.

---

# Overall Philosophy

The notebook should **NOT** be translated cell-by-cell.

Instead, separate the project into two independent layers:

```
User Interface (Streamlit)
        │
        ▼
Scientific Calculation Engine (Pure Python)
```

The Streamlit application should only:

* receive user input,
* call calculation functions,
* display results.

All engineering calculations should remain independent of Streamlit.

---

# Recommended Project Structure

```
project/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── data/
│   ├── examples/
│   │   ├── SWBM.csv
│   │   ├── scantling.csv
│   │   ├── corrosion.csv
│   │   └── ...
│   │
│   └── output/
│
├── src/
│   ├── loader.py
│   ├── preprocessing.py
│   ├── reliability.py
│   ├── statistics.py
│   ├── plotting.py
│   ├── export.py
│   └── utils.py
│
├── assets/
│   └── logo.png
│
└── notebooks/
    └── original_notebook.ipynb
```

The notebook should remain inside the repository only as documentation.

---

# Step 1 — Separate Imports

Move all imports into dedicated modules.

Avoid repeating imports throughout the project.

---

# Step 2 — Convert Notebook Cells into Functions

Instead of

```
Read CSV

↓

Calculate

↓

Plot

↓

Calculate

↓

Plot
```

Convert every logical block into reusable functions.

Example:

```
load_data()

preprocess_data()

calculate_section_modulus()

calculate_wave_bending()

calculate_probability()

calculate_reliability()

generate_plots()

export_results()
```

Every function should

* receive arguments
* return results

and should never read global variables.

---

# Step 3 — Create a Data Loader

Instead of reading files directly

```
pd.read_csv("SWBM.csv")
```

create

```
load_csv(uploaded_file)

or

load_example_data()
```

The loader should work with

* uploaded files
* GitHub example files

using exactly the same processing pipeline.

---

# Step 4 — Example Data

Keep several example CSV files inside

```
data/examples/
```

The application should provide two modes.

## Mode 1

Use example dataset

Useful for demonstration.

## Mode 2

Upload custom CSV files

Useful for real analysis.

Example sidebar

```
Input Source

○ Example Dataset

○ Upload CSV Files
```

---

# Step 5 — Sidebar Controls

The sidebar should contain all user inputs.

Example

```
Input Source

Analysis Case

Ship Length

Corrosion Model

Safety Target

Confidence Interval

Run Analysis
```

Avoid hardcoded values inside Python.

---

# Step 6 — Create a Single Analysis Function

Instead of calculations spread across many notebook cells

create one pipeline

```
run_analysis(inputs)

↓

returns

results
```

Results should include

```
DataFrames

statistics

probabilities

reliability index

figures

summary values
```

---

# Step 7 — Plot Module

Move every figure into its own function.

Example

```
plot_SWBM()

plot_WBM()

plot_PDF()

plot_CDF()

plot_corrosion()

plot_reliability()

plot_joint_distribution()
```

Each function returns

```
matplotlib Figure
```

instead of calling

```
plt.show()
```

The Streamlit app displays

```
st.pyplot(fig)
```

---

# Step 8 — Avoid Recomputing

Large engineering calculations should only execute when the user clicks

```
Run Analysis
```

not every time a widget changes.

Use

```
st.button()

or

st.form()
```

This greatly improves responsiveness.

---

# Step 9 — Cache Expensive Operations

Use Streamlit caching.

Example

```
@st.cache_data
```

for

* loading CSV

* preprocessing

Use

```
@st.cache_resource
```

if large objects must remain in memory.

---

# Step 10 — Organize the Interface

Recommended page layout

```
Title

Description

Sidebar

--------------------------

Summary

Statistics

--------------------------

Plots

--------------------------

Tables

--------------------------

Download Results
```

---

# Step 11 — Display Results

Instead of printing

```
print(df)
```

use

```
st.dataframe(df)
```

instead of

```
print(value)
```

use

```
st.metric()
```

for important engineering values.

Example

```
Reliability Index

Probability of Failure

Maximum Stress

Section Modulus
```

---

# Step 12 — Downloads

Allow users to download

* processed CSV
* summary tables
* figures
* PDF report (future)

using

```
st.download_button()
```

---

# Step 13 — Error Handling

The application should gracefully detect

* missing columns

* empty CSV

* invalid numbers

* incompatible datasets

Instead of crashing,

display meaningful messages.

---

# Step 14 — Performance

Do not generate every figure automatically.

Instead

```
☑ SWBM

☑ WBM

☑ Corrosion

☑ Reliability

☑ Joint PDF
```

Only generate the selected figures.

This reduces execution time significantly.

---

# Step 15 — Repository

The GitHub repository should contain

```
README.md

requirements.txt

example datasets

application source

notebook

documentation
```

Do NOT upload

```
.venv/

__pycache__/

.ipynb_checkpoints/
```

---

# Recommended User Workflow

```
Open App

↓

Choose

Example Dataset

or

Upload CSV Files

↓

Configure Parameters

↓

Run Analysis

↓

View Summary

↓

Inspect Plots

↓

Download Results
```

---

# Deployment Checklist

* Convert notebook into reusable Python modules.
* Keep engineering calculations independent of Streamlit.
* Store example CSV files in the repository.
* Provide both example and upload modes.
* Cache expensive operations.
* Use Streamlit widgets instead of notebook inputs.
* Replace plt.show() with st.pyplot().
* Replace print() with Streamlit components.
* Test locally using:

```
streamlit run app.py
```

* Push to GitHub.
* Deploy to Streamlit Community Cloud.
* Verify the example dataset works immediately after deployment.

---

# Long-Term Goal

The notebook should become a reusable engineering analysis package.

The Streamlit application should only be one interface to that package.

Future interfaces could include:

* Command-line interface (CLI)
* Desktop GUI
* FastAPI REST API
* Batch processing
* Docker deployment

By separating the computational engine from the user interface, future development becomes significantly easier, while ensuring the scientific calculations remain reusable and well tested.
