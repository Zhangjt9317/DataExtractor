# Add the following code to your script to create a new Custom Vision service project. 
# Insert your subscription keys in the appropriate definitions. 
# Also, get your Endpoint URL from the Settings page of the Custom Vision website.

from azure.cognitiveservices.vision.customvision.training import CustomVisionTrainingClient
from azure.cognitiveservices.vision.customvision.training.models import ImageFileCreateEntry

ENDPOINT = "https://southcentralus.api.cognitive.microsoft.com/"

# Replace with a valid key
training_key = "edb35a52aa04460d8edcffc78893ec9c3"
prediction_key = "<your prediction key>"
prediction_resource_id = "/subscriptions/b580d1b7-163e-4a91-bb43-1d260d3753a5/resourceGroups/mygroup/providers/Microsoft.CognitiveServices/accounts/Mol_Images"

publish_iteration_name = "model1"

trainer = CustomVisionTrainingClient(training_key, endpoint=ENDPOINT)

# Create a new project
print ("Creating project...")
project = trainer.create_project("OPVDB_classification")

# Make two tags in the new project
mol_tag = trainer.create_tag(project.id, "mol")
curve_tag = trainer.create_tag(project.id, "curve")
# uvvis_tag = trainer.create_tag(project.id, "uvvis")
imaging_tag = trainer.create_tag(project.id, "imaging")

# To add the sample images to the project, insert the following code after the tag creation. 
# This code uploads each image with its corresponding tag. 
# You can upload up to 64 images in a single batch.
base_image_url = "test_images/"

print("Adding images...")

image_list = []

for image_num in range(1, 11):
    file_name = "mol_{}.jpg".format(image_num)
    with open(base_image_url + "mol/" + file_name, "rb") as image_contents:
        image_list.append(ImageFileCreateEntry(name=file_name, contents=image_contents.read(), tag_ids=[mol_tag.id]))

for image_num in range(1, 11):
    file_name = "curve_{}.jpg".format(image_num)
    with open(base_image_url + "curve/" + file_name, "rb") as image_contents:
        image_list.append(ImageFileCreateEntry(name=file_name, contents=image_contents.read(), tag_ids=[curve_tag.id]))

for image_num in range(1, 11):
    file_name = "imaging_{}.jpg".format(image_num)
    with open(base_image_url + "imaging/" + file_name, "rb") as image_contents:
        image_list.append(ImageFileCreateEntry(name=file_name, contents=image_contents.read(), tag_ids=[imaging_tag.id]))

upload_result = trainer.create_images_from_files(project.id, images=image_list)

if not upload_result.is_batch_successful:
    print("Image batch upload failed.")
    for image in upload_result.images:
        print("Image status: ", image.status)
    exit(-1)


# Train the classifier and publish
import time

print ("Training...")
iteration = trainer.train_project(project.id)
while (iteration.status != "Completed"):
    iteration = trainer.get_iteration(project.id, iteration.id)
    print ("Training status: " + iteration.status)
    time.sleep(1)

# The iteration is now trained. Publish it to the project endpoint
trainer.publish_iteration(project.id, iteration.id, publish_iteration_name, prediction_resource_id)
print ("Done!")

# Get and use the published iteration on the prediction endpoint
from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient

# Now there is a trained endpoint that can be used to make a prediction
predictor = CustomVisionPredictionClient(prediction_key, endpoint=ENDPOINT)

with open(base_image_url + "images/Test/test_image.jpg", "rb") as image_contents:
    results = predictor.classify_image(
        project.id, publish_iteration_name, image_contents.read())

    # Display the results.
    for prediction in results.predictions:
        print("\t" + prediction.tag_name +
              ": {0:.2f}%".format(prediction.probability * 100))