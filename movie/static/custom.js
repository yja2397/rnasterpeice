const pusher2 = new Pusher("17e9426b449b62f3005a", {
    cluster: "ap3",
	encrypted: true
    });

    // Subscribe to movie_bot channel
const channel = pusher2.subscribe('Movie-recommend');

	// bind new_message event to movie_bot channel
channel.bind('new_message', function(data) {
    var $conversation_view = $('.conversation-view');
    // Append human message
    $conversation_view.append(`
        <div class="chat-bubble me">
            <span class="chat-content">
                ${data.human_message}
            </span>
        </div>
	`);

	   // Append bot message
    $conversation_view.append(`
        <div class="chat-bubble">
            <span class="chat-content">
                ${data.bot_message}
            </span>
        </div>
    `);
});


function submit_message(message) {
    $.post( "/send_message", {
        message: message, 
        socketId: pusher2.connection.socket_id
    }, handle_response);
	

    function handle_response(data) {
      // append the bot repsonse to the div
		if(`${data.result}` == "null"){
			console.log(`${data.result}`);
			$('.conversation-view').append(`
				<div class="chat-bubble">
					<span class="chat-content">
						${data.message}
					</span>
				</div>
			`);
          // remove the loading indicator
			$( "#loading" ).remove();
		} else{
			$('.conversation-view').append(`
				<div class="chat-bubble">
					<span class="chat-content">
						${data.message}
					</span>
				</div>
				<div class="chat-bubble result">
					<span class="chat-content">
						${data.result}
					</span>
				</div>
			`);
          // remove the loading indicator
			$( "#loading" ).remove();
		
		}
	}
}

function get_detail(message){
    var $movieDetail = $('.movieDetail');

    $movieDetail.empty();

    $movieDetail.append(`
        <div class="loading">Loading Detail Information</div>
    `)

    message = String(message);
    $.post("/get_detail", {
        message: message,
        socketId: pusher2.connection.socket_id
    }, get_detail);

    function get_detail(data){
        $movieDetail.empty();

        $movieDetail.append(`
            ${data.message}
      `);

    }
}

i = 0;
setInterval(function() {
    i = ++i % 4;
    $(".loading").text("Loading Detail Information " + Array(i+1).join("."));
}, 800);

function get_cast(message){
    message = String(message);
    $.post("/get_cast", {
        message: message,
        socketId: pusher2.connection.socket_id
    }, get_detail);

    function get_detail(data){
        var $movieDetail = $('.movieDetail');
        $movieDetail.empty();

        $movieDetail.append(`
            ${data.message}
      `);

    }
}

$('#target').on('submit', function(e){
    e.preventDefault();
    var $input_message = $('#input_message');
    var $conversation_view = $('.conversation-view');

    const input_message = $input_message.val()
    // return if the user does not enter any text
    if (!input_message) {
      return
    }

    $conversation_view.append(`
        <div class="chat-bubble me">
            <span class="chat-content">
                ${input_message}
            </span>
        </div>
	`);
    // loading
    $conversation_view.append(`
        <div class="chat-bubble" id="loading">
            <span class="chat-content">
                <b>...</b>
            </span>
        </div>
	`);

        // clear the text input 
    $input_message.val('');

    var div = document.getElementsByClassName("conversation-view")[0];
    div.scrollTop = div.scrollHeight;

	console.log(input_message);
        // send the message
    submit_message(input_message);
});

function first(){
    var chat = document.getElementsByClassName('conversation-view')[0];
    var chatAi = document.createElement('div');
    var chatSpan = document.createElement('span');

    chatAi.setAttribute('class', 'chat-bubble');
    chatSpan.setAttribute('class', 'chat-content');
    chatAi.style.width = '100%';

    var chatText = document.createTextNode('다음은 검색 매뉴얼입니다.');

    chatSpan.appendChild(chatText);
	chatSpan.style.background = "orange";
	chatSpan.style.margin = 'auto';
    chatAi.appendChild(chatSpan);
    chat.appendChild(chatAi);



    var chatAi2 = document.createElement('div');

    var chatSpan2 = document.createElement('span');


    chatAi2.setAttribute('class', 'chat-bubble');
    chatSpan2.setAttribute('class', 'chat-content');


	chatSpan2.innerHTML = '연도별 검색 : 2017년 영화 추천<br> 장르별 검색 : 액션 영화 추천<br> 영화 제목 검색 : love 검색<br> 인기 영화 검색 : 인기 영화 추천<br> 최근 영화 검색 : 최근 영화 추천';
	
    chatAi2.appendChild(chatSpan2);
    chat.appendChild(chatAi2);

    var div = document.getElementsByClassName("conversation-view")[0];
    div.scrollTop = div.scrollHeight;
}