from transformers import YolosImageProcessor, YolosForObjectDetection
from PIL import Image
import torch

class LocalHumanDetection:
    
    def __init__(self, image_file: str) -> None:
        """
        Constructor to initialize the model and image processor.
        """
        self.type = "LocalHumanDetection"
        self.image_file = image_file  # Image file to be processed
        self.model = YolosForObjectDetection.from_pretrained('hustvl/yolos-tiny')  # Load YOLO model
        self.image_processor = YolosImageProcessor.from_pretrained("hustvl/yolos-tiny")  # Load image processor
    
    def identify_person(self) -> bool:
        """
        Detects if a person is present in the image using YOLOS.
        Returns True if a person is detected, otherwise False.
        """
        # Open the image
        image = Image.open(self.image_file)

        # Process image through the model
        inputs = self.image_processor(images=image, return_tensors="pt")
        outputs = self.model(**inputs)

        # Extract logits (classification) and bounding boxes
        target_sizes = torch.tensor([image.size[::-1]])
        results = self.image_processor.post_process_object_detection(outputs, threshold=0.9, target_sizes=target_sizes)[0]

        # Iterate over detected objects
        for score, label, box in zip(results["scores"], results["labels"], results["boxes"]):
            box = [round(i, 2) for i in box.tolist()]
            label_name = self.model.config.id2label[label.item()]
            
            # print(
            #     f"Detected {label_name} with confidence {round(score.item(), 3)} at location {box}"
            # )

            # Check if the detected object is a person (COCO class "person" is typically ID 0)
            if label_name.lower() == "person":
                # TO DO: ADD CHECK FOR DISTANCE
                return True  # Person detected

        return False  # No person detected

# Example Usage
def test():
    detector = LocalHumanDetection("../environmentImage.jpg")
    print("Person detected:", detector.identify_person())

if __name__ == "__main__":
    test()
