| Dataset                  | Classifier             | Imbalance method        |   delta_recall |   delta_precision |   delta_f1 |   delta_pr_auc |
|:-------------------------|:-----------------------|:------------------------|---------------:|------------------:|-----------:|---------------:|
| URL-Phish (1:6.02)       | Decision Tree          | ADASYN                  |         0.0457 |           -0.0348 |     0.0058 |        -0.0571 |
| URL-Phish (1:6.02)       | Decision Tree          | SMOTE                   |         0.0375 |           -0.0295 |     0.0044 |        -0.0622 |
| URL-Phish (1:6.02)       | Decision Tree          | SMOTETomek              |         0.0369 |           -0.0302 |     0.0038 |        -0.0459 |
| URL-Phish (1:6.02)       | Decision Tree          | Random Oversampling     |         0.0252 |           -0.0191 |     0.0034 |        -0.0603 |
| Vrbancic et al. (1:1.89) | Decision Tree          | SMOTETomek              |         0.0159 |           -0.0139 |     0.0006 |        -0.003  |
| Vrbancic et al. (1:1.89) | Decision Tree          | Cost-Sensitive Learning |         0.0224 |           -0.0215 |    -0.0004 |        -0.0002 |
| Vrbancic et al. (1:1.89) | Random Forest          | SMOTE                   |         0.0055 |           -0.0081 |    -0.0015 |        -0.0002 |
| Vrbancic et al. (1:1.89) | Random Forest          | Random Oversampling     |         0.0063 |           -0.009  |    -0.0016 |        -0.0005 |
| URL-Phish (1:6.02)       | Random Forest          | SMOTE                   |         0.0275 |           -0.0332 |    -0.0018 |        -0      |
| Vrbancic et al. (1:1.89) | Random Forest          | Cost-Sensitive Learning |        -0.001  |           -0.0027 |    -0.0019 |        -0.0009 |
| Vrbancic et al. (1:1.89) | Random Forest          | SMOTETomek              |         0.0055 |           -0.0098 |    -0.0024 |        -0.0009 |
| Vrbancic et al. (1:1.89) | Decision Tree          | SMOTEENN                |         0.0207 |           -0.0243 |    -0.0027 |        -0.0339 |
| Vrbancic et al. (1:1.89) | Random Forest          | ADASYN                  |         0.0125 |           -0.0172 |    -0.0029 |        -0.0008 |
| URL-Phish (1:6.02)       | Random Forest          | SMOTETomek              |         0.0269 |           -0.0352 |    -0.0031 |        -0      |
| URL-Phish (1:6.02)       | Decision Tree          | Cost-Sensitive Learning |         0.0187 |           -0.0269 |    -0.0035 |        -0.0776 |
| Vrbancic et al. (1:1.89) | Support Vector Machine | SMOTE                   |         0.0234 |           -0.03   |    -0.0039 |        -0.0014 |
| Vrbancic et al. (1:1.89) | Support Vector Machine | SMOTETomek              |         0.0241 |           -0.0305 |    -0.0039 |        -0.0017 |
| Vrbancic et al. (1:1.89) | Decision Tree          | SMOTE                   |         0.0101 |           -0.0183 |    -0.0045 |         0.0163 |
| URL-Phish (1:6.02)       | Random Forest          | Cost-Sensitive Learning |        -0.0076 |           -0.0009 |    -0.0046 |        -0.0012 |
| Vrbancic et al. (1:1.89) | Decision Tree          | Random Oversampling     |         0.0193 |           -0.0275 |    -0.005  |        -0.0034 |
| URL-Phish (1:6.02)       | Random Forest          | ADASYN                  |         0.0351 |           -0.0471 |    -0.0051 |        -0.0086 |
| Vrbancic et al. (1:1.89) | Decision Tree          | Random Undersampling    |         0.0178 |           -0.0271 |    -0.0055 |        -0.0149 |
| Vrbancic et al. (1:1.89) | Support Vector Machine | Random Oversampling     |         0.0239 |           -0.0336 |    -0.0056 |        -0.0021 |
| Vrbancic et al. (1:1.89) | Support Vector Machine | Cost-Sensitive Learning |         0.0258 |           -0.0358 |    -0.0059 |        -0.002  |
| Vrbancic et al. (1:1.89) | Support Vector Machine | Random Undersampling    |         0.027  |           -0.0407 |    -0.0079 |        -0.0041 |
| Vrbancic et al. (1:1.89) | Decision Tree          | ADASYN                  |         0.0198 |           -0.0345 |    -0.0087 |        -0.0145 |
| Vrbancic et al. (1:1.89) | Random Forest          | Random Undersampling    |         0.0147 |           -0.0302 |    -0.0087 |        -0.0035 |
| URL-Phish (1:6.02)       | Decision Tree          | SMOTEENN                |         0.068  |           -0.0809 |    -0.0089 |        -0.101  |
| URL-Phish (1:6.02)       | Random Forest          | Random Oversampling     |         0.0158 |           -0.0365 |    -0.0094 |        -0.0037 |
| Vrbancic et al. (1:1.89) | Support Vector Machine | SMOTEENN                |         0.033  |           -0.0596 |    -0.0153 |        -0.0162 |
| Vrbancic et al. (1:1.89) | Random Forest          | SMOTEENN                |         0.0147 |           -0.0454 |    -0.017  |        -0.0092 |
| Vrbancic et al. (1:1.89) | Support Vector Machine | ADASYN                  |         0.0475 |           -0.0875 |    -0.0246 |        -0.0074 |
| URL-Phish (1:6.02)       | Random Forest          | SMOTEENN                |         0.0387 |           -0.0897 |    -0.0259 |        -0.009  |
| URL-Phish (1:6.02)       | Support Vector Machine | Cost-Sensitive Learning |         0.051  |           -0.1019 |    -0.0279 |        -0.0159 |
| URL-Phish (1:6.02)       | Support Vector Machine | SMOTETomek              |         0.0475 |           -0.1047 |    -0.031  |        -0.0182 |
| URL-Phish (1:6.02)       | Support Vector Machine | SMOTE                   |         0.0475 |           -0.1056 |    -0.0315 |        -0.018  |
| URL-Phish (1:6.02)       | Support Vector Machine | Random Oversampling     |         0.0521 |           -0.1159 |    -0.0353 |        -0.0179 |
| URL-Phish (1:6.02)       | Support Vector Machine | SMOTEENN                |         0.0615 |           -0.139  |    -0.0447 |        -0.0284 |
| URL-Phish (1:6.02)       | Support Vector Machine | Random Undersampling    |         0.0609 |           -0.1627 |    -0.0592 |        -0.0293 |
| URL-Phish (1:6.02)       | Random Forest          | Random Undersampling    |         0.0691 |           -0.177  |    -0.0627 |        -0.0044 |
| URL-Phish (1:6.02)       | Decision Tree          | Random Undersampling    |         0.0656 |           -0.174  |    -0.0648 |        -0.1004 |
| URL-Phish (1:6.02)       | Support Vector Machine | ADASYN                  |         0.0516 |           -0.2271 |    -0.1034 |        -0.0389 |