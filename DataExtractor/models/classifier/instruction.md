## Image Classification

This image classification module focuses on identifying and extracting molecular
images from literature texts (right now we only focus on pdf). CDE focuses more on
html and xml format, but we will discuss this later. In this module we applied two
appraoches:

1. Azure custom vision service
   - providing image classification and object detection 
   - recall and precision reaches 85% + 
   - can be a pretty good image classifier when feeding good training samples
2. molminer
   - have not completed tests yet, and the system does not run through in the Windows system
   - can detect and extract molecular images and turn into SMILES using the python-cli
   interface using Python

   
