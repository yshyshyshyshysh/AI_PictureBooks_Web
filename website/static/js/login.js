const isLoggedIn = localStorage.getItem("username");

// 根據登入狀態顯示或隱藏登出按鈕
const logoutLi = document.getElementById("logout-li");
if (isLoggedIn) {
  logoutLi.style.display = "block";
  const loginLink = document.querySelector('#loginLink');
  const username = isLoggedIn.split('@')[0];
  loginLink.innerHTML = `<a href="/profile" title="${isLoggedIn}">${isLoggedIn}</a>`;
  loginLink.innerHTML = `<a href="/profile" title="welcome, ${username}">welcome, ${username}</a>`;
} else {
  logoutLi.style.display = "none";
}

// 登出按鈕的點擊事件
const logoutLink = document.getElementById("logout-link");
logoutLink.addEventListener("click", function (event) {
  signOut()
  event.preventDefault();
  // 清除本地存儲的登入狀態
  localStorage.removeItem("username");
  // 導向登入頁面
  alert("You have been logged out.")
  window.location.href = "/";
});

document.addEventListener("DOMContentLoaded", function (event) {
  navbarToggleSidebar();
  navActivePage();

  // 檢查本地存儲是否存在用戶名稱
  const username = localStorage.getItem("username");

  if (username) {
    const navbarBrand = document.querySelector(".navbar-brand");
    navbarBrand.textContent = `${username}'s Storybook teller`;
  } else {
    setTimeout(function() {
      alert("Please login/sign up first."); // 如果沒有用戶名稱，可能用戶尚未登錄，導航回登錄頁面
      window.location.href = "/contact";
    }, 2000); // 此處將延遲時間的括號調整到 setTimeout 函數的內部
  }
  const isLoggedIn = localStorage.getItem("username");

  // 根據登入狀態顯示或隱藏登出按鈕
  const logoutLi = document.getElementById("logout-li");
  if (isLoggedIn) {
    logoutLi.style.display = "block";
  } else {
    logoutLi.style.display = "none";
  }

  // 登出按鈕的點擊事件
  const logoutLink = document.getElementById("logout-link");
  logoutLink.addEventListener("click", function (event) {
    event.preventDefault();
    // 清除本地存儲的登入狀態
    localStorage.removeItem("username");
    // 導向登入頁面
    alert("You have been logged out.");
    window.location.href = "/";
  });
});