    import { initializeApp } from "https://www.gstatic.com/firebasejs/10.7.1/firebase-app.js";
    import { getAuth, createUserWithEmailAndPassword, signInWithEmailAndPassword, signOut } 
      from "https://www.gstatic.com/firebasejs/10.7.1/firebase-auth.js";
      const firebaseConfig = {
        apiKey: "AIzaSyCGiBeeTdmkRvjSXnjrmZp091w055lThMI",
        authDomain: "autopresence-b9594.firebaseapp.com",
        projectId: "autopresence-b9594",
        storageBucket: "autopresence-b9594.firebasestorage.app",
        messagingSenderId: "139292140260",
        appId: "1:139292140260:web:664258705e59f7ce7782f1"
      };
    const app = initializeApp(firebaseConfig);
    const auth = getAuth(app);
  
    // Function to Sign Up Users
    function signUp() {
      const email = document.getElementById("email").value;
      const password = document.getElementById("password").value;
      
      createUserWithEmailAndPassword(auth, email, password)
        .then((userCredential) => {
          console.log("User signed up:", userCredential.user);
          alert("Signup Successful!");
        })
        .catch((error) => {
          console.error("Signup Error:", error.message);
          alert(error.message);
        });
    }
  
    // Function to Sign In Users
    function signIn() {
      const email = document.getElementById("email").value;
      const password = document.getElementById("password").value;
      
      signInWithEmailAndPassword(auth, email, password)
        .then((userCredential) => {
          console.log("User signed in:", userCredential.user);
          alert("Login Successful!");
        })
        .catch((error) => {
          console.error("Login Error:", error.message);
          alert(error.message);
        });
    }
  
    // Function to Log Out Users
    function logOut() {
      signOut(auth)
        .then(() => {
          console.log("User signed out");
          alert("Logout Successful!");
        })
        .catch((error) => {
          console.error("Logout Error:", error.message);
          alert(error.message);
        });
    }
  
    // Attach event listeners to buttons
    document.getElementById("signup-btn").addEventListener("click", signUp);
    document.getElementById("signin-btn").addEventListener("click", signIn);
    document.getElementById("logout-btn").addEventListener("click", logOut);