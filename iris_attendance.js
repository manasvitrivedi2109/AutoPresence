// Initialize Firebase
const firebaseConfig = {
    apiKey: "AIzaSyCGiBeeTdmkRvjSXnjrmZp091w055lThMI",
    authDomain: "autopresence-b9594.firebaseapp.com",
    projectId: "autopresence-b9594",
    storageBucket: "autopresence-b9594.firebasestorage.app",
    messagingSenderId: "139292140260",
    appId: "1:139292140260:web:664258705e59f7ce7782f1"
  };
firebase.initializeApp(firebaseConfig);
const db = firebase.firestore();

// Open the camera
const video = document.createElement("video");
video.autoplay = true;
navigator.mediaDevices.getUserMedia({ video: true })
    .then(stream => video.srcObject = stream)
    .catch(err => console.error("Error accessing webcam:", err));

document.body.appendChild(video);

// Capture an image and process it with OpenCV.js
function captureAndRecognize() {
    const canvas = document.createElement("canvas");
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    const ctx = canvas.getContext("2d");
    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
    const imgData = ctx.getImageData(0, 0, canvas.width, canvas.height);
    
    let src = cv.matFromImageData(imgData);
    let gray = new cv.Mat();
    cv.cvtColor(src, gray, cv.COLOR_RGBA2GRAY);
    
    let circles = new cv.Mat();
    cv.HoughCircles(gray, circles, cv.HOUGH_GRADIENT, 1, 50, 100, 30, 20, 50);
    
    let matched = false;
    if (circles.cols > 0) {
        matched = performIrisRecognition(gray, circles);
    }
    
    storeResultInFirebase(matched);
    
    src.delete();
    gray.delete();
    circles.delete();
}

// Dummy iris recognition function (replace with actual logic)
function performIrisRecognition(grayImg, circles) {
    // Here you would extract iris features and compare them with stored data
    return Math.random() > 0.5; // Simulating a 50% match for now
}

// Store match result in Firebase
function storeResultInFirebase(matched) {
    db.collection("iris_matches").add({
        timestamp: firebase.firestore.FieldValue.serverTimestamp(),
        matched: matched
    }).then(() => {
        console.log("Result stored in Firebase");
    }).catch(err => {
        console.error("Error storing result:", err);
    });
}

// Button to capture and recognize
const button = document.createElement("button");
button.innerText = "Capture & Recognize";
button.onclick = captureAndRecognize;
document.body.appendChild(button);
