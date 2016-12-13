from flask import Flask, Response, request
import requests
import hashlib
import redis

app = Flask(__name__)
cache = redis.StrictRedis(host='redis', port=6379, db=0)
salt= "UNIQUE_SALT"
default_name = 'Orhan Doğan'


@app.route('/', methods=['GET', 'POST'])
def manpage():

  name = default_name

  if request.method == 'POST':
      name = request.form['name']

  salted_name = salt + name
  name_hash = hashlib.sha256(salted_name.encode()).hexdigest()
  header = '''<html><head><title>Identidock</title>
  <style type="text/css">  
    body{
      margin:0;
      padding:0;
      font-family: Sans-Serif;
      line-height: 1.5em;
    }
    
    main {
      padding-bottom: 10010px;
      margin-bottom: -10000px;
      float: left;
      width: 100%;
    }
    
    #nav {
      float: left;
      width: 230px;
      margin-left: -100%;
      padding-bottom: 10010px;
      margin-bottom: -10000px;
      background: #eee;
    }
    
    #wrapper {
      overflow: hidden;
    }
    
    #content {
      margin-left: 230px; /* Same as 'nav' width */
    }
    
    .innertube{
      margin: 15px; /* Padding for content */
      margin-top: 0;
    }
    
    p {
      color: #555;
    }
  
    nav ul {
      list-style-type: none;
      margin: 0;
      padding: 0;
    }
    
    nav ul a {
      color: darkgreen;
      text-decoration: none;
    }
  
    input[type="text"] {
      margin: 0;
      width: 250px;
      font-family: sans-serif;
      font-size: 18px;
      appearance: none;
      box-shadow: none;
      border-radius: none;
      padding:7px;
    }

    input[type="submit"] {
      margin: 0;
      width: 80px;
      font-family: sans-serif;
      font-size: 18px;
      appearance: none;
      box-shadow: none;
      border-radius: none;
      padding:7px;
      background-color:orange;
    }    

    input[type="text"]:focus {
      outline: none;
    }

  </style>

  </head><body><div id="wrapper">'''
  body = '''
  <main>
    <div id="content">
      <div class="innertube" style="width:800px;">
        <h1 style="border-bottom: 1px solid #000;margin-bottom:40px;">Dockerized Identidock by Orhan DOĞAN</h1>

  <form method="POST">
            <h2>
              Type a text: 
              <input type="text" name="name" value="{0}">
              <input type="submit" value="submit">
            </h2>
            </form>
            <p>You look like a:
            <img src="/monster/8/{1}" style="margin-left:24px;"/>
            <img src="/monster/16/{1}" style="margin-left:24px;"/>
            <img src="/monster/32/{1}" style="margin-left:24px;"/>
            <img src="/monster/64/{1}" style="margin-left:24px;"/>
            <img src="/monster/128/{1}" style="margin-left:24px;"/>
            <img src="/monster/256/{1}" style="margin-left:24px;"/>
            '''.format(name, name_hash)
  footer = '</main></div></div></p></div></body></html>'

  return header + body + footer


@app.route('/monster/<size>/<name>')
def get_identicon(size, name):

  cache_key = name+':'+size
  image = cache.get(cache_key)
  if image is None:
    print ("Cache miss", flush=True)
    r = requests.get('http://dnmonster:8080/monster/' + name + '?size=' + size)
    image = r.content
    cache.set(cache_key, image)
  
  return Response(image, mimetype='image/png')


if __name__ == '__main__':
  app.run(debug=True, host='0.0.0.0')


