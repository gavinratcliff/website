import commonmark
import sys

intro = """
<!DOCTYPE html>

<html>

<head>
    <link rel="stylesheet" href="../site.css">
    <title>beans space</title>

</head>

<body>
  <h1><a id="title-link" href="../index.html">beans space</a></h1>
"""

outro = """
</body>

</html>
"""

text = open(sys.argv[1], mode='r').read()

parser = commonmark.Parser()
ast = parser.parse(text)

renderer = commonmark.HtmlRenderer()

html = intro + renderer.render(ast) + outro

out = open(sys.argv[2], 'w').write(html)
