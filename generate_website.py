import commonmark
import os
import shutil

assets_to_copy = ["site.css", "debian-button.jpg", "webgl.js"]

def copy_assets():
    for asset in assets_to_copy:
        shutil.copy("assets/" + asset, "generated/" + asset)

def read_file(filename: str):
    with open(filename, "r") as f:
        return f.read()

def write_file(filename: str, contents: str):
    with open(filename, "w") as f:
        return f.write(contents)

post_header = read_file("assets/post_header.html")
post_footer = read_file("assets/post_footer.html")

def replace_tag(tag_name: str, template: str, contents: str) -> str:
    return template.replace(f"<<<{tag_name}>>>", contents)

def get_posts() -> list[str]:
    return ["posts/" + filename for filename in os.listdir("posts/") if ".md" in filename]

def render_posts(posts):
    for post in posts:
        text = read_file(post)

#        title = text.split('\n')[0]

        parser = commonmark.Parser()
        ast = parser.parse(text)

        renderer = commonmark.HtmlRenderer()

        html = post_header + renderer.render(ast) + post_footer

        html = html.replace('<h1>', '<h1><a id="title-link" href="index.html">').replace('</h1>', '</a></h1>')

        write_file(post.replace(".md", ".html").replace("posts/", "generated/"), html)

def post_path_to_title(post_path):
    title = post_path.replace('_', ' ').replace('posts/', '')
    return title[:title.find(".md")]

def generate_post_list(posts):
    return "".join([f'<li><a href="{post.replace(".md", ".html").replace("posts/", "")}">{post_path_to_title(post)}</a></li>' for post in posts])

def generate_index() -> str:
    index_template = read_file("assets/index_template.html")

    posts = get_posts()

    render_posts(posts)

    posts_list = generate_post_list(posts)

    index_template = replace_tag("posts", index_template, posts_list)
    return index_template

write_file("generated/index.html", generate_index())
copy_assets()