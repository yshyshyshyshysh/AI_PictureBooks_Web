
// 註冊
function register(email, password) {
    firebase
        .auth()
        .createUserWithEmailAndPassword(email, password)
        .then(result => {
            // 寄送驗證信 (仍可登入)
            verifyEmail(email);
            console.log("註冊成功！我們寄了一封信 請核查您的信箱已進行登入!")
        }).catch(function (error) {
            // 在此處可以跳轉頁面, 或是將錯誤訊息注入登入頁面
            console.log("註冊失敗: " + error.message);
        });
}

// 登入
function login(email, password) {
    firebase.auth().signInWithEmailAndPassword(email, password)
        .then(result => {
            // 密碼正確
            alert("成功登入!");
        })
        .catch(error => {
            // 錯誤訊息, 密碼信箱不正確等等
            // 在此處可以跳轉頁面, 或是將錯誤訊息注入登入頁面
            console.log(error.message);
        });
}

// 忽略登入狀態都可以呼叫
// 登出
function signOut() {
    firebase.auth().signOut()
        .then(function () {
            // 登出後強制重整一次頁面
            window.location.reload();
        }).catch(function (error) {
            console.log(error.message)
        });
}

// Promise 使用 then 操作
// 的資訊有 => is
function retUserInfo() {
    return new Promise((resolve, reject) => {
        firebase.auth().onAuthStateChanged(function (user) {
            if (user) {
                // User is signed in.
                resolve(user);
            } else {
                // No user is signed in.
                reject("No user is signed in.");
            }
        });
    });
}

// 用戶可能有的所有信息
function testPrintInfo(){
    retUserInfo().then(user => {
        console.log(user.uid);
        console.log(user.email);
        console.log(user.displayName);
        console.log(user.photoURL);
    })
}

// 更新用戶數據 (名字, 大頭照 url)
function updateUserInfo(displayName, photoUrl) {
    retUserInfo().then(user => {
        user.updateProfile({
            displayName: displayName,
            photoURL: photoUrl
        }).then(function() {
            // Update successful.
            console.log("User profile updated successfully.");
        }).catch(function(error) {
            // An error happened.
            console.error("Error updating user profile:", error);
        });
    }).catch(error => {
        console.error(error);
    });
}

// 登入後 才可呼叫
// 請勿單獨呼叫, 需要的情境已經包裝好了
async function reAuth(password) {
    try {
        const user = await retUserInfo();
        const credential = firebase.auth.EmailAuthProvider.credential(user.email, password);
        await user.reauthenticateWithCredential(credential);
        console.log("正確的密碼");
        return user;
    } catch (error) {
        console.log('錯誤的密碼');
        throw error;
    }
}

// 在已經登入狀態 重設密碼
// 未登入狀態請看 "忘記密碼"
async function resetPwd(oldPassword, newPassword) {
    try {
        const user = await reAuth(oldPassword);
        await user.updatePassword(newPassword);
        window.alert('密碼更新完成，請重新登入');

        // 修改密碼完成後，強制登出並重整一次頁面
        await firebase.auth().signOut();
        window.location.reload();
    } catch (error) {
        console.log(error.message);
    }
}

// 刪除用戶 必須重複輸入密碼認證身分
function deleteUser(ConfirmedPwd) {
    reAuth(ConfirmedPwd)
        .then(function (user) {
            user.delete().then(function () {
                window.alert('您的帳號已成功刪除');

                // 刪除帳號後，強制重整一次頁面
                window.location.reload();

            }).catch(function (error) {
                console.log(error.message)
            });
        }).catch(function (error) {
            console.log(error.message)
        })
}

// 此"登入中"用戶是否已經驗證
// 此系統允許先登入後綁定信箱
// Example use: isEmailVerified().then(res=> {console.log(res)})
async function isEmailVerified() {
    var user = firebase.auth().currentUser;
    if (user) {
        return user.emailVerified;
    } else {
        throw new Error("No user is signed in.");
    }
}

// 寄送驗證信
function verifyEmail() {
    var user = firebase.auth().currentUser;

    user
        .sendEmailVerification()
        .then(function () {
            // 驗證信發送完成
            window.alert('驗證信已發送到您的信箱，請查收。')
        }).catch(error => {
            // 驗證信發送失敗
            console.log(error.message);
        });
}

// "忘記密碼, 重新寄信"
function forgetUser(emailAddress) {
    const auth = firebase.auth();
    auth.sendPasswordResetEmail(emailAddress).then(function () {
        window.alert('已發送信件至信箱，請按照信件說明重設密碼');
        window.location.reload(); // 送信後，強制頁面重整一次
    }).catch(function (error) {
        console.log(error.message)
    });
}
