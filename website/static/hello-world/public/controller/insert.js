
class Paragraph {
    constructor(text, soundtrack, translation, img) {
        this.text = text;
        this.translation = translation;
        this.soundtrack = soundtrack;
        this.img = img;
    }
}

class Story {
    constructor(parag, trans, imageURL) {
        this.paragraph = parag;
        this.translation = trans;
        this.picture = imageURL;
    }
}

class Item {
    constructor(title, language, imageURL, stories, sig) {
        this.title = title;
        this.language = language;
        this.stories = stories;
        this.image = imageURL;
        this.signature = sig;
    }
}

function formatStories(soundList, textList, translationTextList, ImgList){
    const arr = [];
    for (let i = 0; i < soundList.length; i++) {
        arr.push(new Paragraph(textList[i], soundList[i], translationTextList[i], ImgList[i]));
    }
    return arr;
}

function formatItem(title, language, imageURL, stories, id){
    return new Item(title, language, imageURL, stories, id);
}

// testing use, the item is beta ver. please ignore
function insertItem(item){
    firebase.database().ref("/items/").push(item);
}

// 已存在的
function publishStories(token, item){
    const path = "/public/stories/" + token;
    firebase.database().ref(path).set(item);
}

// 新增一個故事, 拿物件與 用戶 id
// 如何獲取用戶 id? -> 見 retUserInfo()
function newStories(id, item){
    const path = "/private/" + id + "/mystories/";
    return new Promise((resolve, reject) => {
        firebase.database().ref(path).push(item)
            .then(data => {
                resolve(data.key);
            })
            .catch(error => {
                reject(error);
            });
    });
}

// 更新故事
// 用戶 id -> retUserInfo()
// 故事 token -> 從網頁獲取
// 推入一個新的故事進入 Storage
function updateStories(id, token, item){
    const path = "/private/" + id + "/mystories/" + token;
    firebase.database().ref(path).set(item);
}

// getPublishStories
// return stories information
// use .then(data => {}) retrieve and use the data
// 在此用 hidden type 將故事id存入,未來update故事可以拿取
function getPublishedStories(){
    const publicRef = firebase.database().ref("/public/stories");
    return publicRef.once('value').then(data => {
        return data.val();
    });
}

// 給予用戶 id 拿取此人的所有物件
function getMyStories(id){
    const path = "/private/" + id + "/mystories/";
    const publicRef = firebase.database().ref(path);
    return publicRef.once("value").then(data => {
        return data.val();
    });
}