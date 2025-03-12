let video = document.getElementById("video");
let canvas = document.getElementById("canvas");
let ctx = canvas.getContext("2d");

// List of stored iris images
let storedIrisImages = ["iris1.jpg", "iris2.jpg", "iris3.jpg"]; 

// Function to recognize iris
function recognizeIris() {
    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
    let capturedImage = cv.imread(canvas); // Read captured frame
    let matchFound = false;

    storedIrisImages.forEach(imgPath => {
        let storedImg = new Image();
        storedImg.src = imgPath;
        storedImg.onload = function () {
            let storedMat = cv.imread(storedImg);
            let result = new cv.Mat();
            
            // Template matching (checks for similarity)
            cv.matchTemplate(capturedImage, storedMat, result, cv.TM_CCOEFF_NORMED);
            let minMax = cv.minMaxLoc(result);

            if (minMax.maxVal > 0.8) { // If similarity is high
                alert("✅ Iris Recognized: " + imgPath);
                matchFound = true;
            }
            
            storedMat.delete();
            result.delete();
        };
    });

    capturedImage.delete();
    
    // If no match is found, display an alert
    setTimeout(() => {
        if (!matchFound) {
            alert("❌ Iris Not Recognized");
        }
    }, 1000);
}

// Start the camera
navigator.mediaDevices.getUserMedia({ video: true }).then(stream => {
    video.srcObject = stream;
    video.play();
});

// Button click to recognize iris
document.getElementById("captureButton").addEventListener("click", recognizeIris);
