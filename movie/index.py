from flask import Flask, request, jsonify, render_template
import os
import dialogflow
import requests
import json
import pusher
import httplib2
import json
import urllib.request
from konlpy.tag import Okt
from collections import Counter
import pymysql
from datetime import datetime

h = httplib2.Http()
okt = Okt()

pusher_client = pusher.Pusher(
    app_id=os.getenv('PUSHER_APP_ID'),
    key=os.getenv('PUSHER_KEY'),
    secret=os.getenv('PUSHER_SECRET'),
    cluster=os.getenv('PUSHER_CLUSTER'),
    ssl=True
)

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

# run Flask app
if __name__ == "__main__":
    app.run(debug=True)


def detect_intent_texts(project_id, session_id, text, language_code):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)

    if text:
        text_input = dialogflow.types.TextInput(
            text=text, language_code=language_code)
        query_input = dialogflow.types.QueryInput(text=text_input)
        response = session_client.detect_intent(
            session=session, query_input=query_input)

        return response.query_result.fulfillment_text
		
@app.route('/send_message', methods=['POST'])
def send_message():
    message = request.form['message']
	
    sentences_tag = []
    noun_list = []
    okt = Okt()
    morph = okt.pos(message)
    sentences_tag.append(morph)
    for sentence1 in sentences_tag:
        for word, tag in sentence1:
            if tag in ['Noun']:
                noun_list.append(word)
    success = 0
    for word in noun_list:
        if word == '검색':
            success = 1
            break
    if success != 1:
        project_id = os.getenv('DIALOGFLOW_PROJECT_ID')
        fulfillment_text = detect_intent_texts(project_id, "unique", message, 'ko')
        result = dialog(fulfillment_text)
        response_text = {"message":  fulfillment_text, "result": result}

    else:
        result = searchMovie(message)
        fulfillment_text = message + " 결과는 다음과 같습니다."

        response_text = {"message": fulfillment_text, "result": result}
    socketId = request.form['socketId']
    pusher_client.trigger('movie_bot', 'new_message',
                          {'human_message': message, 'bot_message': fulfillment_text},
                          socketId)
    return jsonify(response_text)

def dialog(sentence):

    sentences_tag = []
    noun_list = []
    okt = Okt()
    morph = okt.pos(sentence)
    sentences_tag.append(morph)

    for sentence1 in sentences_tag:
        for word, tag in sentence1:
            if tag in ['Number']:
                return yearMovie(word)
            if tag in ['Noun']:
                noun_list.append(word)

    for word in noun_list:
        if word == '지금':
            return recentMovie()
        elif word == '장르':
            return genreMovie(noun_list)
        elif word == '인기':
            return popularMovie()
        elif word == '예정':
            return upcomingMovie()


def make_result_title(title):
    url = 'https://api.themoviedb.org/3/search/movie'
    mykey = '?api_key=ff3bedd3d47493bf66e799c508aba82a'
    city = '&language=en-US'
    myrequest = url + mykey + title
    response, content = h.request(myrequest, 'GET')
    resulta = json.loads(content.decode('utf-8'))

    return resulta

def searchMovie(title):

    title = title.replace("검색 ", "")
    title = title.replace(" 검색", "")

    return info_list(make_result_title('&query=' + title + '&include_adult=false'))


def yearMovie(x):
    from datetime import datetime

    year = datetime.today().year

    if (int(x[0:3]) > year):
        print("wrong input")
    else:
        return info_list(make_result('&primary_release_year=' + str(x) + '&sort_by=popularity.desc'))


def genreMovie(noun_list):
    x = 0

    for word in noun_list:
        if word == '액션':
            x = 1
        elif word == '모험':
            x = 2
        elif word == '애니메이션':
            x = 3
        elif word == '코미디':
            x = 4
        elif word == '범죄':
            x = 5
        elif word == '다큐멘터리':
            x = 6
        elif word == '드라마':
            x = 7
        elif word == '가족':
            x = 8
        elif word == '판타지':
            x = 9
        elif word == '역사':
            x = 10
        elif word == '공포':
            x = 11
        elif word == '음악':
            x = 12
        elif word == '미스터리':
            x = 13
        elif word == '로맨스':
            x = 14
        elif word == 'SF':
            x = 15
        elif word == 'TV':
            x = 16
        elif word == '스릴러':
            x = 17
        elif word == '전쟁':
            x = 18
        elif word == '서부':
            x = 19

    if x == 1:
        return info_list(make_result('&with_genres=28&sort_by=popularity.desc'))
    elif x == 2:
        return info_list(make_result('&with_genres=12&sort_by=popularity.desc'))
    elif x == 3:
        return info_list(make_result('&with_genres=16&sort_by=popularity.desc'))
    elif x == 4:
        return info_list(make_result('&with_genres=35&sort_by=popularity.desc'))
    elif x == 5:
        return info_list(make_result('&with_genres=80&sort_by=popularity.desc'))
    elif x == 6:
        return info_list(make_result('&with_genres=99&sort_by=popularity.desc'))
    elif x == 7:
        return info_list(make_result('&with_genres=18&sort_by=popularity.desc'))
    elif x == 8:
        return info_list(make_result('&with_genres=10751&sort_by=popularity.desc'))
    elif x == 9:
        return info_list(make_result('&with_genres=14&sort_by=popularity.desc'))
    elif x == 10:
        return info_list(make_result('&with_genres=36&sort_by=popularity.desc'))
    elif x == 11:
        return info_list(make_result('&with_genres=27&sort_by=popularity.desc'))
    elif x == 12:
        return info_list(make_result('&with_genres=10402&sort_by=popularity.desc'))
    elif x == 13:
        return info_list(make_result('&with_genres=9648&sort_by=popularity.desc'))
    elif x == 14:
        return info_list(make_result('&with_genres=10749&sort_by=popularity.desc'))
    elif x == 15:
        return info_list(make_result('&with_genres=878&sort_by=popularity.desc'))
    elif x == 16:
        return info_list(make_result('&with_genres=10770&sort_by=popularity.desc'))
    elif x == 17:
        return info_list(make_result('&with_genres=53&sort_by=popularity.desc'))
    elif x == 18:
        return info_list(make_result('&with_genres=10752&sort_by=popularity.desc'))
    elif x == 19:
        return info_list(make_result('&with_genres=37&sort_by=popularity.desc'))
  
	

def popularMovie():
    return info_list(make_result('&certification_country=US&certification=R&sort_by=popularity.desc'))


def recentMovie():
    return info_list(make_result_playing())

def upcomingMovie():
    return info_list(make_result_upcoming())

def make_result_playing():
    url = 'https://api.themoviedb.org/3/movie/now_playing'
    mykey = '?api_key=ff3bedd3d47493bf66e799c508aba82a'
    city = '&language=en-US'
    myrequest = url + mykey + city
    response, content = h.request(myrequest, 'GET')
    resulta = json.loads(content.decode('utf-8'))

    return resulta

# show results of lists what have many results of movie.

def make_result_upcoming():
    url = 'https://api.themoviedb.org/3/movie/upcoming'
    mykey = '?api_key=ff3bedd3d47493bf66e799c508aba82a'
    city = '&language=en-US&region=KR'
    myrequest = url + mykey + city
    response, content = h.request(myrequest, 'GET')
    resulta = json.loads(content.decode('utf-8'))

    return resulta

def info_list(result):
    if result['total_results'] > 7:
        times = 6
    else:
        times = result['total_results'] - 1


    response = ""

    for num in range(0, times):
        poster = result['results'][num]['poster_path']
        base_url = 'https://image.tmdb.org/t/p/'
        file_size = 'w500/'
        poster = base_url + file_size + str(poster)
        title = result['results'][num]['title']
        api_id = result['results'][num]['id']

        response += """
            <div class="movie">
                <img src="{0}" onclick="get_detail({1})" onerror="this.src='/static/movie.jpg'" alt="{2}"><br>
                {2}
            </div>
        """.format(poster, api_id, title)

    return response

def info_listR(result):
    if result['total_results'] > 7:
        times = 6
    else:
        times = result['total_results'] - 1


    response = ""

    for num in range(0, times):
        poster = result['results'][num]['poster_path']
        base_url = 'https://image.tmdb.org/t/p/'
        file_size = 'w500/'
        poster = base_url + file_size + str(poster)
        title = result['results'][num]['title']
        api_id = result['results'][num]['id']

        response += """
            <div class="detail actorDetail">
                <img src="{0}" onclick="get_detail({1})" onerror="this.src='/static/movie.jpg'" alt="{2}"><br>
                {2}
            </div>
        """.format(poster, api_id, title)

    return response


# api_ex recives discover of movie's information.

def make_result(api_ex):
    url = 'https://api.themoviedb.org/3/discover/movie'
    mykey = '?api_key=ff3bedd3d47493bf66e799c508aba82a'
    city = '&language=en-US'
    myrequest = url + mykey + city + api_ex
    response, content = h.request(myrequest, 'GET')
    resulta = json.loads(content.decode('utf-8'))

    return resulta




# api_id recieves ip id of moive

def make_result_keyword(api_id):
    url = 'https://api.themoviedb.org/3/movie/'
    mykey = '?api_key=ff3bedd3d47493bf66e799c508aba82a'
    keyword = '/keywords'
    city = '&language=en-US'
    myrequest = url + str(api_id) + keyword + mykey
    response, content = h.request(myrequest, 'GET')
    resulta = json.loads(content.decode('utf-8'))

    return resulta


# api_id recieves ip id of moive

def make_result_similar(api_id):
    url = 'https://api.themoviedb.org/3/movie/'
    mykey = '?api_key=ff3bedd3d47493bf66e799c508aba82a'
    keyword = '/similar'
    city = '&language=en-US'
    myrequest = url + str(api_id) + keyword + mykey
    response, content = h.request(myrequest, 'GET')
    resulta = json.loads(content.decode('utf-8'))

    return resulta


# api_id recieves ip id of moive

def make_result_cast(api_id):
    url = 'https://api.themoviedb.org/3/movie/'
    mykey = '?api_key=ff3bedd3d47493bf66e799c508aba82a'
    keyword = '/credits'
    city = '&language=en-US'
    myrequest = url + str(api_id) + keyword + mykey
    response, content = h.request(myrequest, 'GET')
    resulta = json.loads(content.decode('utf-8'))

    return resulta


# api_id recieves ip id of moive

def make_result_id(api_id):
    url = 'https://api.themoviedb.org/3/movie/'
    mykey = '?api_key=ff3bedd3d47493bf66e799c508aba82a'
    city = '&language=en-US'
    myrequest = url + str(api_id) + mykey + city
    response, content = h.request(myrequest, 'GET')
    resulta = json.loads(content.decode('utf-8'))

    return resulta



@app.route('/get_detail', methods=['POST'])
def makeDetail():
    api_id = request.form['message']
    poster = make_result_id(api_id)['poster_path']
    base_url = 'https://image.tmdb.org/t/p/'
    file_size = 'w500/'
    poster = base_url + file_size + str(poster)

    if make_result_id(api_id)['production_countries']:
        country = make_result_id(api_id)['production_countries'][0]['name']
    else:
        country = make_result_id(api_id)['original_language']

    genre = ""
    if make_result_id(415735)['genres']:
        if len(make_result_id(api_id)['genres']) > 5:
                genreLen = 4
        else:
            genreLen = len(make_result_id(api_id)['genres'])-1
        for i in range(0, genreLen):
            genre += make_result_id(api_id)['genres'][i]['name'] + ", "
        genre = genre[::-1]
        genre = genre.replace(" ,", "", 1)
        genre = genre[::-1]

    popularity = make_result_id(api_id)['vote_average'] * 10



    keyword = ""

    if make_result_keyword(api_id)['keywords'] :
        if len(make_result_keyword(api_id)['keywords']) > 6:
                keywordLen = 5
        else:
            keywordLen = len(make_result_keyword(api_id)['keywords'])-1
        for i in range(0, keywordLen):
            keyword += """
                <div class="tag"><span><img class="hash" src="/static/hashtag.png" /></span> {0}</div>
            """.format(make_result_keyword(api_id)['keywords'][i]['name'])


    response = ""
    response += """
        <div class="movieOri">
            <img class="detail Img" src="{0}" onerror="this.src='/static/movie.jpg'" alt="{1}"/>
            <div class="detail Simple" >
                <div  class="detail Title">{1}</div>

                <table class="detail Table" >
                    <tr>
                        <td >Original-title</td>
                        <td ><div class="detail OriNation">{2}</div></td>
                    </tr>
                    <tr>
                        <td >Original-nation</td>
                        <td ><div class="detail OriNation">{3}</div></td>
                    </tr>
                    <tr>
                        <td >Genre</td>
                        <td><div class="detail Genre">{4}</div></td>
                    </tr>
                    <tr>
                        <td >Release-date</td>
                        <td><div class="detail Genre">{5}</div></td>
                    </tr>
                    <tr>
                        <td >Star-rating</td>
                        <td><div class="detail rate">
                            <div class="rate-top" style="width: {6}%"><span>★</span><span>★</span><span>★</span><span>★</span><span>★</span></div>
                        <div class="rate-bottom"><span>★</span><span>★</span><span>★</span><span>★</span><span>★</span></div>
                        </div></td>
                    </tr>
                    <tr>
                        <td colspan="2">
                            {7}
                        </td>
                    </tr>
                </table>
            </div>
        </div>
    """.format(poster, make_result_id(api_id)['title'], make_result_id(api_id)['original_title'], country, genre, make_result_id(api_id)['release_date'], popularity, keyword)

    conn = pymysql.connect(host='localhost', user='root', password='0726', db='movie', charset='utf8')
    curs = conn.cursor()

    sql = """insert into recommendMovie values (%s, %s, %s)"""
    curs.execute(sql, (str(api_id), make_result_id(api_id)['title'], genre))
    conn.commit()

    curs.close()
    conn.close()

    crew = ""
    if make_result_cast(api_id)['crew'] :
        if len(make_result_cast(api_id)['crew']) > 4:
            crewLen = 3
        else:
            crewLen = len(make_result_cast(api_id)['crew'])-1
        for i in range(0, crewLen):
            crew += """
                <div  class="detail actorDetail">
                    <img src="{0}" onerror="this.src='/static/people.png'" alt="{1}">
                        {1}
                </div>
            """.format('https://image.tmdb.org/t/p/w500/' + str(make_result_cast(api_id)['crew'][i]['profile_path']), make_result_cast(api_id)['crew'][i]['name'])

    cast = ""
    if make_result_cast(api_id)['cast'] :
        if len(make_result_cast(api_id)['cast']) > 4:
            castLen = 3
        else:
            castLen = len(make_result_cast(api_id)['cast'])-1
        for i in range(0, castLen):
            cast += """
                <div  class="detail actorDetail">
                    <img src="{0}" onclick ="get_cast({2})" onerror="this.src='/static/people.png'" alt="{1}">
                        {1}
                </div>
            """.format('https://image.tmdb.org/t/p/w500/' + str(make_result_cast(api_id)['cast'][i]['profile_path']), make_result_cast(api_id)['cast'][i]['name'], make_result_cast(api_id)['cast'][i]['id'])

    if make_result_id(api_id)['overview'] :
	    overview = make_result_id(api_id)['overview']
    else:
        overview = ""
    response += """
        <div class="crew">
            <div class="details">Crews</div>
            {0}
        </div>
        <div class="actor">
            <div class="details">Cast Actor</div>
            {1}
        </div>
        <div class="plot">
            <div class="details">Plot</div>
                {2}
        </div>
    """.format(crew, cast, overview)

    response += """
        <div class="relatedMovie">
            <div class="details">Related Film</div>
            {0}
        </div>
        <div class="youtube">
            <div class="details">Related YouTube</div>
            <iframe src="https://www.youtube.com/embed?listType=search&list={1}" frameborder="0" allowfullscreen></iframe>
        </div>
    """.format(info_listR(make_result_similar(api_id)), make_result_id(api_id)['title'])


    reply = {
        "message": response,
    }

    return jsonify(reply)