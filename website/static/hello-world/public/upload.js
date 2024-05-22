import { getStorage, ref, uploadBytes } from "firebase/storage";


var firebaseConfig = {
    authDomain: "project-project-20240429.firebaseapp.com",
    databaseURL: "https://project-20240429-default-rtdb.firebaseio.com",
    projectId: "project-20240429"
};
firebase.initializeApp(firebaseConfig);

const storage = getStorage();

const mountainsRef = ref(storage, 'test.png');

// Create a reference to 'images/mountains.jpg'
const mountainImagesRef = ref(storage, 'images/test.png');
const metadata = { contentType: 'image/png'};
const uploadTask = uploadBytes(storageRef, file, metadata);
