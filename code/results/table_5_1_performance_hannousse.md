| Classifier             | Imbalance method        |   precision |   recall |     f1 |   roc_auc |   pr_auc |    mcc |
|:-----------------------|:------------------------|------------:|---------:|-------:|----------:|---------:|-------:|
| Decision Tree          | No Treatment (Baseline) |      0.7983 |   0.748  | 0.7724 |    0.8554 |   0.6883 | 0.7485 |
| Decision Tree          | Random Oversampling     |      0.7661 |   0.748  | 0.757  |    0.8613 |   0.5983 | 0.7304 |
| Decision Tree          | Random Undersampling    |      0.55   |   0.8661 | 0.6728 |    0.9312 |   0.5716 | 0.6485 |
| Decision Tree          | SMOTE                   |      0.7444 |   0.7795 | 0.7615 |    0.8973 |   0.6399 | 0.7346 |
| Decision Tree          | ADASYN                  |      0.7899 |   0.8583 | 0.8226 |    0.9247 |   0.7198 | 0.8029 |
| Decision Tree          | SMOTEENN                |      0.7    |   0.8819 | 0.7805 |    0.9303 |   0.6773 | 0.7593 |
| Decision Tree          | SMOTETomek              |      0.7444 |   0.7795 | 0.7615 |    0.8973 |   0.6399 | 0.7346 |
| Decision Tree          | Cost-Sensitive Learning |      0.6867 |   0.811  | 0.7437 |    0.8907 |   0.6446 | 0.7157 |
| Random Forest          | No Treatment (Baseline) |      0.916  |   0.8583 | 0.8862 |    0.9928 |   0.9445 | 0.8746 |
| Random Forest          | Random Oversampling     |      0.916  |   0.8583 | 0.8862 |    0.9916 |   0.9472 | 0.8746 |
| Random Forest          | Random Undersampling    |      0.6316 |   0.9449 | 0.7571 |    0.9879 |   0.9255 | 0.7432 |
| Random Forest          | SMOTE                   |      0.8846 |   0.9055 | 0.8949 |    0.9914 |   0.9476 | 0.8832 |
| Random Forest          | ADASYN                  |      0.8769 |   0.8976 | 0.8872 |    0.9905 |   0.946  | 0.8745 |
| Random Forest          | SMOTEENN                |      0.8273 |   0.9055 | 0.8647 |    0.9892 |   0.9343 | 0.8499 |
| Random Forest          | SMOTETomek              |      0.8915 |   0.9055 | 0.8984 |    0.9908 |   0.9459 | 0.8871 |
| Random Forest          | Cost-Sensitive Learning |      0.9266 |   0.7953 | 0.8559 |    0.9907 |   0.9365 | 0.8443 |
| Support Vector Machine | No Treatment (Baseline) |      0.8871 |   0.8661 | 0.8765 |    0.9889 |   0.9039 | 0.863  |
| Support Vector Machine | Random Oversampling     |      0.8333 |   0.8661 | 0.8494 |    0.9871 |   0.8927 | 0.8325 |
| Support Vector Machine | Random Undersampling    |      0.6218 |   0.9449 | 0.75   |    0.9837 |   0.8565 | 0.7362 |
| Support Vector Machine | SMOTE                   |      0.7632 |   0.9134 | 0.8315 |    0.9858 |   0.8751 | 0.8151 |
| Support Vector Machine | ADASYN                  |      0.8264 |   0.7874 | 0.8065 |    0.9846 |   0.8739 | 0.7858 |
| Support Vector Machine | SMOTEENN                |      0.7355 |   0.8976 | 0.8085 |    0.9832 |   0.866  | 0.7898 |
| Support Vector Machine | SMOTETomek              |      0.7632 |   0.9134 | 0.8315 |    0.9858 |   0.8751 | 0.8151 |
| Support Vector Machine | Cost-Sensitive Learning |      0.8284 |   0.874  | 0.8506 |    0.9876 |   0.8957 | 0.8338 |