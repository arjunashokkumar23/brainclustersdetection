## Brain Clusters Detection

- This project uses the f-MRI images of the human brain as input.
- Each brain image depict the blood activation areas at various parts of the brain using different colors like red and blue.
- Our aim is to detect those blood activation areas, obtain their contours and extract that information as the first step.
- In the second step, we use the clustering algorithm DBSCAN, to group these activation areas into clusters and mark the outliers as noise.
- Finally, the total count of such clusters is reported as a CSV in each brain slice.
