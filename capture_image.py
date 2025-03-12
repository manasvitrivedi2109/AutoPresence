import cv2

# Initialize the camera (0 is usually the default camera)
camera = cv2.VideoCapture(0)
cv2.namedWindow("Test")
img_counter = 0
inp = input("Enter name of student: ")
while(1):
    result,image = camera.read()
    cv2.imshow(inp,image)
    # if cv2.waitKey(0):
    #     cv2.imwrite(inp + ".jpg",image)
    #     print("image taken")
    k = cv2.waitKey(1)
    if k%256 == 27:
        print("Escape hit,closing the app")
        break
    elif k%256 == 32:
        img_name = "opencv_frame_{}.jpg".format(img_counter)
        cv2.imwrite(inp + ".jpg",image)
        print("Screenshot taken")
        img_counter += 1
else:
    print("No image taken!!Try again")
camera.release()
    
