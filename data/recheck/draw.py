import cv2

# Function to draw points from labels.txt onto an image
def draw_points_from_labels(image_path, labels_file_path, output_image_path):
    # Load the image
    image = cv2.imread(image_path)
    if image is None:
        print("Error: Image not found!")
        return

    # Read the labels file
    with open(labels_file_path, 'r') as file:
        lines = file.readlines()

    # Iterate through each line in labels.txt
    for line in lines:
        parts = line.strip().split()
        classIndex = int(parts[0])  # First element is class index
        points = list(map(float, parts[1:]))  # Remaining are coordinates

        # Extract coordinates for four points
        x1, y1, x2, y2, x3, y3, x4, y4 = points

        # Draw points on the image
        for (x, y) in [(x1, y1), (x2, y2), (x3, y3), (x4, y4)]:
            cv2.circle(image, (int(x), int(y)), 5, (0, 255, 0), -1)  # Green dots

        # Optionally connect points to form a quadrilateral
        quad_points = [(int(x1), int(y1)), (int(x2), int(y2)), (int(x3), int(y3)), (int(x4), int(y4))]
        for i in range(len(quad_points)):
            cv2.line(image, quad_points[i], quad_points[(i + 1) % 4], (255, 0, 0), 2)  # Blue lines

    # Save the output image
    cv2.imwrite(output_image_path, image)
    print(f"Output saved to {output_image_path}")

# Example usage
draw_points_from_labels(
    image_path= r'D:\Python\labelImg_OBB\data\recheck\houses.jpg',
    labels_file_path=r'D:\Python\labelImg_OBB\data\recheck\houses.txt',
    output_image_path=r'D:\Python\labelImg_OBB\data\recheck\out.jpg'
)
