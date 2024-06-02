// function getResults() {
//     var input1 = document.getElementById("input1").value;
//     var input2 = document.getElementById("input2").value;

//     // 发送 AJAX 请求
//     var xhr = new XMLHttpRequest();
//     xhr.open("POST", "/get_results", true);
//     xhr.setRequestHeader("Content-Type", "application/json");
//     xhr.onreadystatechange = function() {
//         if (xhr.readyState === XMLHttpRequest.DONE) {
//             if (xhr.status === 200) {
//                 var response = JSON.parse(xhr.responseText);
//                 var image_url = response.image_url;
//                 document.getElementById("imageContainer").innerHTML = "<img src='" + image_url + "'>";
//             } else {
//                 console.error("Error:", xhr.statusText);
//             }
//         }
//     };
//     xhr.send(JSON.stringify({input1: input1, input2: input2}));
// }

function generateStory() {
    const title = document.getElementById('titleInput').value;
    fetch('/generate_story', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ title: title })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('storyContainer').innerText = data.story;
    })
    .catch(error => console.error('Error:', error));
}
