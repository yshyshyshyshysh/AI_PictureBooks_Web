const firebaseConfig = {
    authDomain: "project-project-20240429.firebaseapp.com",
    storageBucket: "gs://project-20240429.appspot.com",
    projectId: "project-20240429"
};
firebase.initializeApp(firebaseConfig);


function loadTask(path, file) {
    const ref = firebase.storage().ref(path);
    const name = +new Date() + "-" + file.name;
    const metadata = {
        contentType: file.type
    };
    return ref.child(name).put(file, metadata);
}

// here can check the upload progress
// do not called this by itself
// if dont need progress, simply comment the snpashot code
function uploadProgress(file){
    const path = file ? (file.type.startsWith('image') ? "/images/" : (file.type.startsWith('audio') ? "/audio/" : "/")) : "";

    let task = loadTask(path, file);
    return new Promise((resolve, reject) => {
        task.on('state_changed',
            function(snapshot) {
                const progress = (snapshot.bytesTransferred / snapshot.totalBytes) * 100;
                // here can get the upload progress
                console.log('Upload is ' + progress.toFixed(2) + '% done');
            },
            function(error) {
                console.error("Error:", error);
                reject(error);
            },
            function() {
                // when complete
                console.log('Upload complete.');
                task.snapshot.ref.getDownloadURL().then(downloadURL => {
                    resolve(downloadURL);
                }).catch(error => {
                    reject(error);
                });
            }
        );
    });
}

// one should write this file into parameter
// please do check before connecting to the DB
// check if the file by !file
function upload(file = document.querySelector("#photo").files[0]){
    uploadProgress(file)
        .then(downloadURL => {
            // here can return URL to use
            // example: return downloadURL
            console.log("Download URL:", downloadURL);
        })
        .catch(error => {
            console.error("Error:", error);
        });
}

