| Classifier             | Imbalance method        |   precision |   recall |     f1 |   roc_auc |   pr_auc |    mcc |
|:-----------------------|:------------------------|------------:|---------:|-------:|----------:|---------:|-------:|
| Decision Tree          | No Treatment (Baseline) |      0.9165 |   0.9291 | 0.9227 |    0.9611 |   0.9035 | 0.8815 |
| Decision Tree          | Random Oversampling     |      0.889  |   0.9484 | 0.9177 |    0.9606 |   0.9001 | 0.8732 |
| Decision Tree          | Random Undersampling    |      0.8894 |   0.947  | 0.9173 |    0.9603 |   0.8886 | 0.8724 |
| Decision Tree          | SMOTE                   |      0.8982 |   0.9393 | 0.9182 |    0.9672 |   0.9198 | 0.8741 |
| Decision Tree          | ADASYN                  |      0.882  |   0.9489 | 0.914  |    0.9537 |   0.889  | 0.8675 |
| Decision Tree          | SMOTEENN                |      0.8922 |   0.9499 | 0.9201 |    0.9482 |   0.8695 | 0.8769 |
| Decision Tree          | SMOTETomek              |      0.9026 |   0.945  | 0.9233 |    0.9612 |   0.9005 | 0.8819 |
| Decision Tree          | Cost-Sensitive Learning |      0.8949 |   0.9516 | 0.9223 |    0.9627 |   0.9033 | 0.8804 |
| Random Forest          | No Treatment (Baseline) |      0.9339 |   0.9532 | 0.9435 |    0.9922 |   0.9858 | 0.9133 |
| Random Forest          | Random Oversampling     |      0.925  |   0.9595 | 0.9419 |    0.992  |   0.9853 | 0.9107 |
| Random Forest          | Random Undersampling    |      0.9037 |   0.9679 | 0.9347 |    0.991  |   0.9823 | 0.8997 |
| Random Forest          | SMOTE                   |      0.9258 |   0.9588 | 0.942  |    0.9922 |   0.9856 | 0.9109 |
| Random Forest          | ADASYN                  |      0.9168 |   0.9658 | 0.9406 |    0.9921 |   0.985  | 0.9087 |
| Random Forest          | SMOTEENN                |      0.8885 |   0.9679 | 0.9265 |    0.9874 |   0.9766 | 0.8871 |
| Random Forest          | SMOTETomek              |      0.9241 |   0.9588 | 0.9411 |    0.9916 |   0.9849 | 0.9095 |
| Random Forest          | Cost-Sensitive Learning |      0.9312 |   0.9523 | 0.9416 |    0.9918 |   0.9849 | 0.9104 |
| Support Vector Machine | No Treatment (Baseline) |      0.9275 |   0.9219 | 0.9247 |    0.985  |   0.9713 | 0.8851 |
| Support Vector Machine | Random Oversampling     |      0.8939 |   0.9458 | 0.9191 |    0.9851 |   0.9692 | 0.8753 |
| Support Vector Machine | Random Undersampling    |      0.8868 |   0.9489 | 0.9167 |    0.9841 |   0.9672 | 0.8717 |
| Support Vector Machine | SMOTE                   |      0.8975 |   0.9453 | 0.9208 |    0.9852 |   0.9698 | 0.8779 |
| Support Vector Machine | ADASYN                  |      0.84   |   0.9694 | 0.9001 |    0.9826 |   0.9639 | 0.8468 |
| Support Vector Machine | SMOTEENN                |      0.8679 |   0.9549 | 0.9093 |    0.9794 |   0.955  | 0.8603 |
| Support Vector Machine | SMOTETomek              |      0.897  |   0.946  | 0.9208 |    0.9851 |   0.9696 | 0.878  |
| Support Vector Machine | Cost-Sensitive Learning |      0.8917 |   0.9477 | 0.9188 |    0.9852 |   0.9693 | 0.8749 |