# rnasterpeice
-----------------------------
이 프로그램을 실행하기 위해서는 약간의 작업이 필요합니다.
1. dialogflow id 생성 --> https://console.dialogflow.com/api-client/#/getStarted
2. dialogflow에서 new agent 생성
3. new agent에 Movie_recommend.zip을 import
4. pusher id 생성 후 agent 생성 --> https://pusher.com/
5. ngrok 설치 --> https://ngrok.com/
6. ngrok 실행 후 ngrok http 5000 입력 -> https로 시작하는 주소 복사
7. dialogflow의 fullfilment 탭의 Webhook 활성화 후 주소 붙여넣기
8. movie 폴더에서 .env 파일에서 dialogflow project id, pusher app id, pusher key, pusher secret, pusher cluster 수정.
9. movie 폴더 안에 있는 env 폴더 안에 있는 Script 폴더 들어간 후 참조하는 폴더 주소 복사
10. cmd 창 연 후 주소 붙여넣기
11. activate라고 입력
12. cd.. 두번 입력한 후 flask run 입력
13. chrome 창을 열고 localhost:5000 입력
14. 실행됩니다.