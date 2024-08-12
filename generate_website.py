import commonmark
import os
import shutil
from datetime import datetime, date

assets_to_copy = ["site.css", "debian-button.jpg", "webgl.js", "resume.pdf"]

def copy_assets():
    for asset in assets_to_copy:
        shutil.copy("assets/" + asset, "generated/" + asset)

def read_file(filename: str):
    with open(filename, "r") as f:
        return f.read()

def write_file(filename: str, contents: str):
    with open(filename, "w") as f:
        return f.write(contents)

def replace_tag(tag_name: str, template: str, contents: str) -> str:
    return template.replace(f"<<<{tag_name}>>>", contents)

post_header = read_file("assets/post_header.html")
post_footer = read_file("assets/post_footer.html")

def read_post_table_entry(line: str) -> tuple[str, date, date]:
    parts = line.split(',')
    print(parts)
    return (parts[0], datetime.strptime(parts[1][1:], "%m/%d/%Y").date(), datetime.strptime(parts[2][1:], "%m/%d/%Y").date())

def read_post_table() -> list[tuple[str, date, date]]:
    post_table_text = read_file("assets/posts.txt")
    return [read_post_table_entry(line) for line in post_table_text.split('\n')]

def write_post_table(post_table: list[tuple[str, date, date]]):
    write_file("assets/posts.txt", "\n".join([f"{post_file}, {created.strftime('%m/%d/%Y')}, {edited.strftime('%m/%d/%Y')}" for post_file, created, edited in post_table]))
    
def get_last_edited_datetime(file_path):
    modification_time = os.path.getmtime(file_path)
    last_edited_datetime = datetime.fromtimestamp(modification_time)
    return last_edited_datetime

def get_posts() -> list[tuple[str, date, date]]:
    post_table = read_post_table()

    post_files = [filename for filename in os.listdir("posts/") if ".md" in filename]

    new_table = []
    for post_file, created, edited in post_table:
        last_edited = get_last_edited_datetime("posts/" + post_file).date()

        if (edited != last_edited):
            edited = last_edited
        
        new_table.append((post_file, created, edited))

    for post_file in post_files:
        found = False
        for post_file2, _, _ in post_table:
            if post_file2 == post_file:
                found = True

        if not found:
            new_entry = (post_file, datetime.today().date(), datetime.today().date())
            new_table.append(new_entry)

    return new_table

def format_date_with_suffix(date_obj):
    day = date_obj.day
    suffix = 'th' if 11 <= day <= 13 else {1: 'st', 2: 'nd', 3: 'rd'}.get(day % 10, 'th')
    formatted_date = date_obj.strftime(f"%B {day}{suffix}, %Y")
    return formatted_date

def generate_post_markdown(post_path, created, edited):
    if created == edited:
        heading = post_path_to_title(post_path) + "\n==============\n***" + format_date_with_suffix(created) + "***\n\n"
    else:
        heading = f"{post_path_to_title(post_path)}\n==============\n***{format_date_with_suffix(created)} (edited {format_date_with_suffix(edited)})***\n\n"
    body = read_file("posts/" + post_path)

    return heading + body

def render_posts(posts: list[tuple[str, date, date]]):
    posts.sort(key = lambda x: x[1])
    post = posts.reverse()
    for post_file, created, edited in posts:
        print(post_file)
        text = generate_post_markdown(post_file, created, edited)

        parser = commonmark.Parser()
        ast = parser.parse(text)

        renderer = commonmark.HtmlRenderer()

        html = post_header + renderer.render(ast) + post_footer

        html = html.replace('<h1>', '<h1><a id="title-link" href="index.html">').replace('</h1>', '</a></h1>')

        write_file("generated/" + post_file.replace(".md", ".html"), html)

    write_post_table(posts)

def post_path_to_title(post_path):
    title = post_path.replace('_', ' ').replace('posts/', '')
    return title[:title.find(".md")].capitalize()


def generate_post_list(posts):
    return "".join([f'<li><a href="{post_file.replace(".md", ".html")}">{post_path_to_title(post_file)}</a>{" - " + created.strftime("%B, %Y")}</li>' for post_file, created, edited in posts])

def generate_index() -> str:
    index_template = read_file("assets/index_template.html")

    posts = get_posts()

    render_posts(posts)

    posts_list = generate_post_list(posts)

    index_template = replace_tag("posts", index_template, posts_list)
    return index_template

write_file("generated/index.html", generate_index())
copy_assets()