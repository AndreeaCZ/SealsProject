# SoftwareEng
The model is trained on these 8 features - 'WBC', 'LYMF', 'RBC', 'HGB', 'MCH', 'MCHC', 'MPV', 'PLT'

One important thing (devs only):
Because I wanted to put them in modules, one thing needs to be fixed. 
When you run decisionTree, the model will be saved in the Data dir. Before running the dashboard,
move the model file to view directory or it will not work. 

TO DO: 
1. Refactoring - lot of duplicate code
2. About section
...

![](treeOutput.png)