# GridGuard AI

### Explainable AI-Based Predictive Maintenance for Power Transformers

GridGuard AI is a machine learning-based predictive maintenance prototype developed to assess the health condition of power transformers using diagnostic and oil-quality parameters.

The system analyzes transformer measurements and classifies transformer health into four conditions:

- **Excellent**
- **Good**
- **Poor**
- **Critical**

Beyond producing a health classification, the system incorporates Explainable AI (XAI) techniques to provide insight into the factors influencing individual predictions. This is intended to make model outputs more understandable and useful for transformer maintenance decision support.

> **Current Version:** v1.0 Prototype  
> This version represents the initial working prototype developed before the engineer-focused interface redesign.

---

## Project Motivation

Power transformers are critical and expensive components of electrical power infrastructure. Unexpected transformer failures can result in power outages, equipment damage, costly repairs, and safety concerns.

Conventional reactive and scheduled maintenance approaches may either respond to faults after they occur or perform maintenance regardless of the transformer's actual condition.

This project explores the use of machine learning as a condition-based decision-support approach, where available transformer diagnostic measurements are used to estimate the current health condition of a transformer.

---

## How the System Works

The current prototype follows the general workflow:

```text
Transformer Diagnostic Data
          │
          ▼
   Input Validation
          │
          ▼
    Preprocessing
          │
          ▼
 Machine Learning Model
          │
          ▼
 Transformer Health Class
          │
          ▼
 Explainable AI Analysis
          │
          ▼
 Maintenance Decision Support
```

The application currently accepts transformer measurements through **manual data entry**.

Preset test profiles are also provided to simplify demonstration and testing. These presets populate the input fields with example values and should not be interpreted as live transformer measurements.

Real-time acquisition from IoT sensors, online monitoring equipment, or SCADA infrastructure is outside the scope of the current implementation.

---

## Input Parameters

The application uses transformer diagnostic measurements that include Dissolved Gas Analysis (DGA) and oil-condition indicators.

### Dissolved Gas Analysis (DGA)

DGA examines gases dissolved in transformer insulating oil. Changes in the concentration and combination of these gases can provide useful information about thermal and electrical activity occurring inside a transformer.

Examples of gases represented in the system include:

- Hydrogen (H₂)
- Methane (CH₄)
- Ethylene (C₂H₄)
- Ethane (C₂H₆)
- Acetylene (C₂H₂)
- Carbon Monoxide (CO)
- Carbon Dioxide (CO₂)

### Oil and Insulation Condition Indicators

Additional diagnostic variables provide information about the condition of the transformer oil and insulation system.

These include parameters such as:

- Dielectric rigidity
- Water content
- Interfacial characteristics
- Power factor
- Other available transformer condition measurements

Together, these measurements provide the feature inputs used by the predictive model.

---

## Machine Learning

The research compares multiple machine learning approaches for transformer health classification.

The current application prototype deploys a trained **XGBoost classifier** as its prediction engine.

The deployed model artifact is stored in:

```text
models/smote_xgboost.json
```

The application separates the prediction engine from the user interface so that the underlying model can be updated without redesigning the entire application.

---

## Handling Class Imbalance

Transformer health datasets may contain significantly fewer observations representing deteriorating conditions than healthy operating conditions.

During model development, **Synthetic Minority Over-sampling Technique (SMOTE)** was used on the training data to improve representation of minority health classes.

SMOTE was applied only after separating the training and test data to prevent synthetic observations from leaking into the unseen test set.

```text
Train/Test Split
       │
       ▼
Training Data
       │
       ▼
Preprocessing
       │
       ▼
SMOTE
       │
       ▼
Model Training
       │
       ▼
Evaluation on Unseen Test Data
```

---

## Explainable AI

Prediction accuracy alone does not necessarily explain why a transformer has been assigned a particular health condition.

GridGuard AI therefore incorporates Explainable AI techniques, including **SHAP (SHapley Additive exPlanations)**, to provide additional insight into model predictions.

The explainability component helps identify which transformer measurements contributed most strongly to a particular health assessment.

Instead of providing only:

```text
Predicted Condition: Critical
```

the system can additionally help answer:

```text
Why was this transformer classified as Critical?
```

This provides greater transparency and makes the prediction more useful as a maintenance decision-support tool.

---

## Model Evaluation

The machine learning models are evaluated using multiple classification metrics rather than relying solely on overall accuracy.

Evaluation includes:

- Confusion Matrix
- Accuracy
- Precision
- Recall
- F1-Score
- ROC-AUC
- PR-AUC

Particular attention is given to **Recall, Macro F1-Score, and PR-AUC**, since failure-related transformer conditions may be underrepresented in the original dataset.

---

## Technologies Used

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Streamlit | Interactive application interface |
| Pandas | Data manipulation |
| NumPy | Numerical computation |
| Scikit-learn | Machine learning and preprocessing |
| XGBoost | Transformer health classification |
| Imbalanced-learn | SMOTE and imbalance handling |
| SHAP | Model explainability |
| LIME | Local prediction explanation |
| Matplotlib | Data visualization |

---

## Project Structure

```text
gridguard_ai/
│
├── models/
│   ├── lime_reference_data.csv
│   ├── model_metadata.json
│   ├── shap_explainer.pkl
│   ├── simulation_presets.json
│   └── smote_xgboost.json
│
├── utils/
│   ├── __init__.py
│   ├── explainability.py
│   ├── helpers.py
│   ├── loader.py
│   ├── predictor.py
│   └── style.py
│
├── views/
│   ├── __init__.py
│   ├── about.py
│   ├── about_developer.py
│   ├── assessment.py
│   ├── explainable_ai.py
│   ├── home.py
│   └── insights.py
│
├── app.py
├── requirements.txt
├── .gitignore
└── README.md
```

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/birdcoreone/transformer-predictive-maintenance-ai.git
```

### 2. Enter the project directory

```bash
cd transformer-predictive-maintenance-ai
```

### 3. Create a virtual environment

Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

Linux/macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Run the application

```bash
streamlit run app.py
```

Streamlit will provide a local address through which the application can be accessed in a web browser.

---

## Current Scope

Version 1 focuses on:

- Transformer health classification
- Manual entry of diagnostic measurements
- Preset test profiles
- Machine learning-based health assessment
- Explainable AI
- Visualization of prediction information
- Decision support for transformer maintenance assessment

The current implementation does **not** claim direct connection to operational transformers or live utility infrastructure.

---

## Future Development

A future version of the system may investigate integration with appropriate IoT sensors, online DGA monitoring equipment, APIs, or existing SCADA infrastructure where diagnostic measurements are electronically available.

Such integration could allow measurements to be acquired automatically and passed to the predictive model for near-real-time transformer health assessment.

Further development may also include:

- Improved engineer-focused user interface
- Automated navigation from assessment to prediction results
- Simplified maintenance-oriented explanations
- Historical transformer assessment records
- Model and data drift monitoring
- Validation using additional transformer datasets
- Deployment within a utility monitoring environment

---

## Version History

### v1.0 — Initial Prototype

The first working prototype includes:

- Transformer diagnostic data entry
- Preset test cases
- Four-class transformer health prediction
- XGBoost prediction engine
- SHAP/LIME explainability components
- Interactive Streamlit interface

### v2.0 — Engineer-Focused Redesign

Planned improvements focus on simplifying the application for practical maintenance use by removing unnecessary model-development information from the user interface and improving the assessment-to-result workflow.

---

## Academic Context

This project was developed as part of a **Bachelor of Technology (BTech) Artificial Intelligence** research project at **Kumasi Technical University (KsTU), Ghana**.

The work investigates the application of machine learning and explainable artificial intelligence to predictive maintenance and transformer health assessment.

---

## Disclaimer

GridGuard AI is currently a research prototype and decision-support system. Predictions produced by the application should not replace established transformer diagnostic procedures, professional engineering judgement, or utility safety protocols.

---

## Author

**Teddy Boamah**  
BTech Artificial Intelligence  
Kumasi Technical University (KsTU), Ghana

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.