# StoryVerse AI Hub: Language Learning through AI-Generated Picture Books

-   vscode 介面右上角有 markdown 的 preview，或是按 ctrl+shift+V

## website 資料夾裡目前網頁的功能

-   /: 探索頁面 (index.html)
-   /signup: 註冊頁面 (signup.html)
-   /contact: 登入頁面 (contact.html)
-   /test_input: 創作頁面 (submit.html)
-   /profile: 個人頁面 (profile.html)
-   /project: 故事頁面 (project.html)

## example_website 資料夾裡目前網頁的功能

-   打開後是 index.html 的內容，在網址後面加 /page1 會出現 page1.html 的內容
-   確認按鈕按下會回傳圖片

## 備註

-   ngrok 連線需輸入 access authtoken，在這拿: [ngrok-authtoken](https://dashboard.ngrok.com/get-started/your-authtoken)
-  免費的 ngrok 帳號連線三次以上會有誤，需要關閉現有 tunnel 才可以連上，在這裡關 tunnel: [ngrok-agents](https://dashboard.ngrok.com/tunnels/agents)
-   templates 跟 static 資料夾請勿刪除，且必須將 html 放在 templates 資料夾，css、js 等放在 static 資料夾，因為有使用到 render_template，否則會跑不出來
-   在 html 中呼叫 css 或 js 等檔案，需寫成 `src="{{ url_for('static', filename='js/scripts.js') }}"`，否則無法使用，詳見: [Python Flask 框架建立網頁範例](https://medium.com/%E5%B7%A5%E7%A8%8B%E9%9A%A8%E5%AF%AB%E7%AD%86%E8%A8%98/%E4%BD%BF%E7%94%A8-python-flask-%E5%BB%BA%E7%AB%8B%E7%B6%B2%E7%AB%99-353e449a9bc8)
-   other/bootstrap_template_example 資料夾裡面是一個前端網站模板用 flask 的範例，可參考
-   other/local_ai_model_test 資料夾裡面是在測試說模型可以在這台電腦的本地跑，還有把圖片音檔輸出看看
