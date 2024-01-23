import os
from datetime import datetime

intro = """<!DOCTYPE html>

<html>

<head>
    <link rel="stylesheet" href="site.css">
    <title>beans space</title>

</head>

<body>
  <h1><a id="title-link" href="index.html">beans space</a> - <a id="title-link"
      href="posts.html">posts</a></h1>

<ul>
"""

outro = """
</ul>
</body>

</html>"""

str = "" + intro

blog_list = ""

for file in os.listdir('posts'):
    if file.endswith('.html'):
        name = (os.path.splitext(file))[0].replace('_', ' ')
        date = datetime.fromtimestamp(
                os.path.getctime("posts/" + file)).strftime('%Y-%m-%d')
        str += "<li><a href=\"posts/" + file + "\">" + name + "</a> - " + date + "</li>"
        print(name)
        blog_list += "<li><a href=\"posts/" + file + "\">" + name + "</a> - " + date + "</li>"

str += outro

out_file = open('posts.html', 'w')
out_file.write(str)


in_file = open('index_template.html', 'r')
template = in_file.read()

template = template.replace("<<<blogs>>>", blog_list)

out_file = open('index.html', 'w')
out_file.write(template)