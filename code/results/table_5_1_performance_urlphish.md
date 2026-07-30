| Classifier             | Imbalance method        |   precision |   recall |     f1 |   roc_auc |   pr_auc |    mcc |
|:-----------------------|:------------------------|------------:|---------:|-------:|----------:|---------:|-------:|
| Decision Tree          | No Treatment (Baseline) |      0.9005 |   0.8535 | 0.8764 |    0.9509 |   0.8674 | 0.8569 |
| Decision Tree          | Random Oversampling     |      0.8814 |   0.8787 | 0.8797 |    0.9315 |   0.8071 | 0.8601 |
| Decision Tree          | Random Undersampling    |      0.7265 |   0.9192 | 0.8115 |    0.9555 |   0.767  | 0.7836 |
| Decision Tree          | SMOTE                   |      0.871  |   0.891  | 0.8807 |    0.9395 |   0.8052 | 0.8609 |
| Decision Tree          | ADASYN                  |      0.8657 |   0.8992 | 0.8821 |    0.944  |   0.8102 | 0.8624 |
| Decision Tree          | SMOTEENN                |      0.8196 |   0.9215 | 0.8675 |    0.9439 |   0.7664 | 0.8461 |
| Decision Tree          | SMOTETomek              |      0.8703 |   0.8905 | 0.8802 |    0.9426 |   0.8214 | 0.8602 |
| Decision Tree          | Cost-Sensitive Learning |      0.8736 |   0.8723 | 0.8728 |    0.9263 |   0.7898 | 0.8518 |
| Random Forest          | No Treatment (Baseline) |      0.9507 |   0.8887 | 0.9185 |    0.99   |   0.9701 | 0.9063 |
| Random Forest          | Random Oversampling     |      0.9142 |   0.9045 | 0.9091 |    0.9901 |   0.9664 | 0.8943 |
| Random Forest          | Random Undersampling    |      0.7737 |   0.9578 | 0.8558 |    0.9906 |   0.9657 | 0.8357 |
| Random Forest          | SMOTE                   |      0.9175 |   0.9162 | 0.9167 |    0.9906 |   0.97   | 0.903  |
| Random Forest          | ADASYN                  |      0.9036 |   0.9238 | 0.9134 |    0.9905 |   0.9615 | 0.8991 |
| Random Forest          | SMOTEENN                |      0.861  |   0.9274 | 0.8927 |    0.9882 |   0.961  | 0.8751 |
| Random Forest          | SMOTETomek              |      0.9155 |   0.9156 | 0.9154 |    0.9913 |   0.97   | 0.9015 |
| Random Forest          | Cost-Sensitive Learning |      0.9497 |   0.8811 | 0.9139 |    0.9905 |   0.9688 | 0.9013 |
| Support Vector Machine | No Treatment (Baseline) |      0.9426 |   0.894  | 0.9176 |    0.9893 |   0.9614 | 0.9048 |
| Support Vector Machine | Random Oversampling     |      0.8266 |   0.9461 | 0.8823 |    0.9879 |   0.9435 | 0.864  |
| Support Vector Machine | Random Undersampling    |      0.7798 |   0.9549 | 0.8584 |    0.9867 |   0.9321 | 0.8382 |
| Support Vector Machine | SMOTE                   |      0.837  |   0.9414 | 0.8861 |    0.9877 |   0.9434 | 0.868  |
| Support Vector Machine | ADASYN                  |      0.7155 |   0.9455 | 0.8142 |    0.9823 |   0.9226 | 0.7893 |
| Support Vector Machine | SMOTEENN                |      0.8036 |   0.9555 | 0.8729 |    0.987  |   0.933  | 0.8542 |
| Support Vector Machine | SMOTETomek              |      0.8379 |   0.9414 | 0.8866 |    0.9876 |   0.9433 | 0.8686 |
| Support Vector Machine | Cost-Sensitive Learning |      0.8407 |   0.9449 | 0.8897 |    0.9881 |   0.9456 | 0.8722 |