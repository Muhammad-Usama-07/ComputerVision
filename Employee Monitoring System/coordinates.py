import cv2

# Global variables to store the coordinates
coordinates = []
current_rectangle = []
rectangle_started = False

def mouse_callback(event, x, y, flags, param):
    global current_rectangle, rectangle_started
    
    if event == cv2.EVENT_LBUTTONDOWN:
        rectangle_started = True
        current_rectangle = [x, y, 0, 0]
    
    elif event == cv2.EVENT_LBUTTONUP:
        rectangle_started = False
        current_rectangle[2] = x - current_rectangle[0]
        current_rectangle[3] = y - current_rectangle[1]
        coordinates.append(tuple(current_rectangle))
        cv2.rectangle(image, (current_rectangle[0], current_rectangle[1]), (x, y), (0, 0, 255), 2)
        cv2.imshow("Image", image)
    
    elif event == cv2.EVENT_MOUSEMOVE and rectangle_started:
        image_copy = image.copy()
        cv2.rectangle(image_copy, (current_rectangle[0], current_rectangle[1]), (x, y), (0, 0, 255), 2)
        cv2.imshow("Image", image_copy)

# Load the image
image = cv2.imread("image-asset.jpeg")

# Create a window and set the mouse callback function
cv2.namedWindow("Image")
cv2.setMouseCallback("Image", mouse_callback)

# Display the image
cv2.imshow("Image", image)
cv2.waitKey(0)

# Save the coordinates to a text file
filename = "coordinates.txt"
with open(filename, "w") as file:
    for rect in coordinates:
        print("Coordinate (x, y, width, height):", rect)
        file.write(f"Coordinate (x, y, width, height): {rect}\n")

print("Coordinates saved to", filename)

# Close the window
cv2.destroyAllWindows()
