# Dissertation

Comparative study of class imbalance treatment techniques for machine learning-based phishing website detection.

## Repository Structure

```
.
├── chapters/                 # Dissertation chapter drafts and templates (.docx)
│   ├── Design and Implementation Draft V1.docx      # Chapter 4
│   ├── Chapter 5 Results and Evaluation Template.docx
│   ├── Chapter 6 Discussion Template.docx
│   └── Chapter 7 Conclusion and Future Work Template.docx
├── figures/                  # Diagrams and figures
│   ├── Figure_Experimental_Procedure.svg            # Editable vector source
│   ├── Figure_Experimental_Procedure.png            # Standard resolution (900px)
│   ├── Figure_Experimental_Procedure_HighRes.png    # High resolution (2400px)
│   ├── Figure_Experimental_Procedure.pdf            # Vector PDF for print/LaTeX
│   └── Figure_Experimental_Procedure.mmd            # Mermaid source (editable)
└── code/                     # Implementation of the experimental pipeline
    ├── README.md             # Step-by-step implementation guide
    ├── run_pipeline.py       # End-to-end runner
    ├── src/                  # Pipeline modules
    ├── results/              # Generated result tables
    └── figures/              # Generated SHAP plots
```

See [`code/README.md`](code/README.md) for setup instructions, a stage-by-stage
walkthrough of the implementation, and the results obtained.

## Study Overview

- **Datasets:** UCI Phishing Websites (11,055 instances, 30 features) and the Hannousse & Yahiouche benchmark (11,430 URLs, 87 features)
- **Imbalance treatment techniques (7):** Random Oversampling, Random Undersampling, SMOTE, ADASYN, SMOTEENN, SMOTETomek, Cost-Sensitive Learning
- **Classifiers (3):** Decision Tree, Random Forest, Support Vector Machine
- **Experimental matrix:** 2 datasets × 7 techniques × 3 classifiers = 42 configurations
- **Evaluation metrics:** Precision, Recall, F1-score, ROC-AUC, PR-AUC, MCC
- **Statistical testing:** Friedman test and McNemar's test (p < 0.05)
- **Induced imbalance:** both published datasets are close to balanced (UCI 44.3% phishing, Hannousse balanced by design), so a 10% minority share (≈1:9) is induced by downsampling the phishing class only

## Experimental Procedure

The figure in `figures/` illustrates the end-to-end experimental workflow: dataset
loading and preprocessing, stratified 80/20 train-test split, application of one
imbalance treatment technique, learning algorithm selection, model training with
stratified 5-fold cross-validation, evaluation on the held-out test set, result
comparison, and McNemar's test for statistical significance. The process is repeated
for every combination of dataset, imbalance technique and classifier.
