| Dataset               | Classifier             | Imbalance method        |   delta_recall |   delta_precision |   delta_f1 |   delta_pr_auc |
|:----------------------|:-----------------------|:------------------------|---------------:|------------------:|-----------:|---------------:|
| Hannousse & Yahiouche | Decision Tree          | ADASYN                  |         0.1102 |           -0.0085 |     0.0503 |         0.0315 |
| UCI Phishing Websites | Decision Tree          | SMOTE                   |         0.0365 |            0.0587 |     0.0462 |        -0.0074 |
| UCI Phishing Websites | Decision Tree          | SMOTETomek              |         0.0365 |            0.0587 |     0.0462 |        -0.0074 |
| UCI Phishing Websites | Decision Tree          | ADASYN                  |         0.0511 |            0.0266 |     0.0405 |        -0.0224 |
| UCI Phishing Websites | Decision Tree          | Random Oversampling     |         0.0511 |           -0.0036 |     0.0268 |        -0.0079 |
| UCI Phishing Websites | Decision Tree          | Cost-Sensitive Learning |         0.0584 |           -0.038  |     0.0143 |        -0.022  |
| Hannousse & Yahiouche | Random Forest          | SMOTETomek              |         0.0472 |           -0.0245 |     0.0123 |         0.0014 |
| Hannousse & Yahiouche | Random Forest          | SMOTE                   |         0.0472 |           -0.0314 |     0.0088 |         0.0031 |
| Hannousse & Yahiouche | Decision Tree          | SMOTEENN                |         0.1339 |           -0.0983 |     0.0081 |        -0.011  |
| UCI Phishing Websites | Random Forest          | ADASYN                  |         0.0292 |           -0.0254 |     0.0068 |         0.0051 |
| UCI Phishing Websites | Random Forest          | SMOTE                   |         0.0146 |           -0.0174 |     0.0017 |         0.0079 |
| UCI Phishing Websites | Random Forest          | SMOTETomek              |         0.0146 |           -0.0174 |     0.0017 |         0.0069 |
| Hannousse & Yahiouche | Random Forest          | ADASYN                  |         0.0394 |           -0.039  |     0.001  |         0.0015 |
| Hannousse & Yahiouche | Random Forest          | Random Oversampling     |         0      |            0      |     0      |         0.0027 |
| UCI Phishing Websites | Random Forest          | Random Oversampling     |         0.0292 |           -0.065  |    -0.0105 |        -0.0047 |
| Hannousse & Yahiouche | Decision Tree          | SMOTETomek              |         0.0315 |           -0.054  |    -0.0108 |        -0.0485 |
| Hannousse & Yahiouche | Decision Tree          | SMOTE                   |         0.0315 |           -0.054  |    -0.0108 |        -0.0485 |
| UCI Phishing Websites | Random Forest          | Cost-Sensitive Learning |         0      |           -0.0348 |    -0.0142 |        -0.0029 |
| Hannousse & Yahiouche | Decision Tree          | Random Oversampling     |         0      |           -0.0322 |    -0.0154 |        -0.09   |
| UCI Phishing Websites | Decision Tree          | SMOTEENN                |         0.073  |           -0.1152 |    -0.0181 |        -0.1406 |
| Hannousse & Yahiouche | Random Forest          | SMOTEENN                |         0.0472 |           -0.0886 |    -0.0215 |        -0.0102 |
| Hannousse & Yahiouche | Support Vector Machine | Cost-Sensitive Learning |         0.0079 |           -0.0587 |    -0.0259 |        -0.0082 |
| Hannousse & Yahiouche | Support Vector Machine | Random Oversampling     |         0      |           -0.0538 |    -0.0271 |        -0.0112 |
| Hannousse & Yahiouche | Decision Tree          | Cost-Sensitive Learning |         0.063  |           -0.1117 |    -0.0287 |        -0.0437 |
| Hannousse & Yahiouche | Random Forest          | Cost-Sensitive Learning |        -0.063  |            0.0106 |    -0.0302 |        -0.008  |
| UCI Phishing Websites | Support Vector Machine | Cost-Sensitive Learning |         0.0292 |           -0.1151 |    -0.0367 |        -0.0308 |
| UCI Phishing Websites | Support Vector Machine | SMOTETomek              |         0      |           -0.0851 |    -0.0375 |        -0.0222 |
| UCI Phishing Websites | Support Vector Machine | SMOTE                   |         0      |           -0.0851 |    -0.0375 |        -0.0222 |
| UCI Phishing Websites | Support Vector Machine | Random Oversampling     |         0.0219 |           -0.1096 |    -0.0377 |        -0.0281 |
| Hannousse & Yahiouche | Support Vector Machine | SMOTE                   |         0.0472 |           -0.1239 |    -0.045  |        -0.0288 |
| Hannousse & Yahiouche | Support Vector Machine | SMOTETomek              |         0.0472 |           -0.1239 |    -0.045  |        -0.0288 |
| UCI Phishing Websites | Random Forest          | SMOTEENN                |         0.0365 |           -0.1533 |    -0.0484 |        -0.025  |
| UCI Phishing Websites | Support Vector Machine | SMOTEENN                |         0.0511 |           -0.1761 |    -0.058  |        -0.0394 |
| Hannousse & Yahiouche | Support Vector Machine | SMOTEENN                |         0.0315 |           -0.1516 |    -0.068  |        -0.0379 |
| Hannousse & Yahiouche | Support Vector Machine | ADASYN                  |        -0.0787 |           -0.0607 |    -0.07   |        -0.0301 |
| UCI Phishing Websites | Support Vector Machine | ADASYN                  |        -0.0073 |           -0.1579 |    -0.0764 |        -0.039  |
| UCI Phishing Websites | Random Forest          | Random Undersampling    |         0.0657 |           -0.2357 |    -0.0788 |        -0.0175 |
| Hannousse & Yahiouche | Decision Tree          | Random Undersampling    |         0.1181 |           -0.2483 |    -0.0996 |        -0.1168 |
| UCI Phishing Websites | Support Vector Machine | Random Undersampling    |         0.0511 |           -0.2494 |    -0.0999 |        -0.0235 |
| UCI Phishing Websites | Decision Tree          | Random Undersampling    |         0.0438 |           -0.268  |    -0.1196 |        -0.0857 |
| Hannousse & Yahiouche | Support Vector Machine | Random Undersampling    |         0.0787 |           -0.2653 |    -0.1265 |        -0.0475 |
| Hannousse & Yahiouche | Random Forest          | Random Undersampling    |         0.0866 |           -0.2844 |    -0.1291 |        -0.019  |