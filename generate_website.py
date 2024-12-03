import commonmark
import os
import shutil
from datetime import datetime, date

# Simple static assets that the generated site needs.
assets_to_copy = ["site.css", "debian-button.jpg", "webgl.js", "resume.pdf"]

def copy_assets():
    for asset in assets_to_copy:
        shutil.copy("assets/" + asset, "generated/" + asset)

# File handling utilities
def read_file(filename: str):
    with open(filename, "r") as f:
        return f.read()

def write_file(filename: str, contents: str):
    with open(filename, "w") as f:
        return f.write(contents)

def replace_tag(tag_name: str, template: str, contents: str) -> str:
    return template.replace(f"<<<{tag_name}>>>", contents)

# Footer and header templates
post_header = read_file("assets/post_header.html")
blog_page_header = read_file("assets/blog_page_header.html")
cooking_page_header = read_file("assets/cooking_page_header.html")
post_footer = read_file("assets/post_footer.html")

# Post table handling
# 
# The post table is a line per post and separates by commas the filename, created date, and last edited date
# For example: "summer_learning_2023.md, 06/24/2023, 08/12/2024"
# These are some relatively ugly functions to load this format.
def read_post_table_entry(line: str) -> tuple[str, date, date]:
    parts = line.split(",")
    return (parts[0], datetime.strptime(parts[1][1:], "%m/%d/%Y").date(), datetime.strptime(parts[2][1:], "%m/%d/%Y").date())

def read_post_table() -> list[tuple[str, date, date]]:
    post_table_text = read_file("assets/posts.txt")
    return [read_post_table_entry(line) for line in post_table_text.split("\n")]

def write_post_table(post_table: list[tuple[str, date, date]]):
    write_file("assets/posts.txt", "\n".join([f"{post_file}, {created.strftime('%m/%d/%Y')}, {edited.strftime('%m/%d/%Y')}" for post_file, created, edited in post_table]))

# Finds the date a file was last edited (to automatically update the "edited" header on every post)
def get_last_edited_date(file_path):
    modification_time = os.path.getmtime(file_path)
    last_edited_datetime = datetime.fromtimestamp(modification_time)
    return last_edited_datetime.date()


# Loads the post table and parses it, update the edited date, and adds any new posts.
def get_posts() -> list[tuple[str, date, date]]:
    # All the posts in the table
    post_table = read_post_table()

    # All the post files on disk
    post_files = [filename for filename in os.listdir("posts/") if ".md" in filename]

    # Update all the edited times and build a new table
    new_table = []
    for post_file, created, edited in post_table:
        last_edited = get_last_edited_date("posts/" + post_file)

        if edited != last_edited:
            edited = last_edited
        
        new_table.append((post_file, created, edited))

    # Add any posts new posts not in the table, and set their creation date
    for post_file in post_files:
        found = False
        for post_file2, _, _ in post_table:
            if post_file2 == post_file:
                found = True

        if not found:
            new_entry = (post_file, datetime.today().date(), datetime.today().date())
            new_table.append(new_entry)

    # Write the new post table back to the disk
    write_post_table(new_table)

    return new_table

# Format a date like "August 23rd, 2024"
def format_date_with_suffix(date_obj):
    day = date_obj.day
    suffix = "th" if 11 <= day <= 13 else {1: "st", 2: "nd", 3: "rd"}.get(day % 10, "th")
    formatted_date = date_obj.strftime(f"%B {day}{suffix}, %Y")
    return formatted_date

# Loads the markdown, adding a nice markdown title and date subheader
def generate_post_markdown(post_path, created, edited):
    if created == edited:
        heading = post_path_to_title(post_path) + "\n==============\n***" + format_date_with_suffix(created) + "***\n\n"
    else:
        heading = f"{post_path_to_title(post_path)}\n==============\n***{format_date_with_suffix(created)} (edited {format_date_with_suffix(edited)})***\n\n"
    body = read_file("posts/" + post_path)

    return heading + body

# Loads all the posts up, sorts them by date and then generates the HTML files for each of them.
def render_posts(posts: list[tuple[str, date, date]]):

    # Get the posts in latest to oldest order.
    posts.sort(key = lambda x: x[1])
    posts.reverse()

    post_htmls = []

    for post_file, created, edited in posts:
        # Get full markdown
        text = generate_post_markdown(post_file, created, edited)

        # Convert it to HTML and add the header and footer.
        parser = commonmark.Parser()
        ast = parser.parse(text)
        renderer = commonmark.HtmlRenderer()
        basic_html = renderer.render(ast)

        # Make the title a link back to my homepage.
        html = post_header + basic_html.replace("<h1>", "<h1><a id=\"title-link\" href=\"index.html\">Blog - ").replace("</h1>", "</a></h1>") + post_footer

        url = post_file.replace(".md", ".html")

        html2 = basic_html.replace("<h1>", f"<h2><a id=\"title-link\" href=\"{url}\">").replace("</h1>", "</a></h2>")

        # Place this in the generated folder.
        write_file("generated/" + post_file.replace(".md", ".html"), html)

        post_htmls.append(html2)
    
    return post_htmls 

def post_path_to_title(post_path):
    title = post_path.replace("_", " ").replace("posts/", "")
    return title[:title.find(".md")].capitalize()

# Generates the HTML for a post table of contents
def generate_post_list(posts):
    return "".join([f'<li><a href="{post_file.replace(".md", ".html")}">{post_path_to_title(post_file)}</a>{" - " + created.strftime("%B, %Y")}</li>' for post_file, created, edited in posts])

def generate_blog_page(post_htmls):
    full_html = blog_page_header + '\n'.join(post_htmls) + post_footer
    write_file("generated/" + 'blog.html', full_html)

def generate_recipe(recipe_path, title):
    recipe_md = read_file(recipe_path)

    parser = commonmark.Parser()
    ast = parser.parse(recipe_md)
    renderer = commonmark.HtmlRenderer()
    recipe_html = renderer.render(ast)

    recipe_html = recipe_html.replace('<h2>', '<h3>').replace('</h2>', '</h3>')
    recipe_html = recipe_html.replace('<h1>', f'<h2 id={title}>').replace('</h1>', '</h2>')
    
    return recipe_html

def generate_recipes_page():
    html_all = ""
    index = []
    for recipe in os.listdir('recipes/'):
        recipe_title = recipe.split('.')[0].replace('_', ' ').title()

        html_all += generate_recipe('recipes/' + recipe, recipe_title)

        index.append(recipe_title)

    index = '<ul>' + ''.join([f'<li><a href=#{title}>{title}</a></li>' for title in index]) + '</ul>'

    html_all = cooking_page_header + index + html_all + post_footer
    
    write_file("generated/cooking.html", html_all)

# Generates the full index.
def generate_index():
    index_template = read_file("assets/index_template.html")

    posts = get_posts()

    post_htmls = render_posts(posts)
    generate_blog_page(post_htmls)

    posts_list = generate_post_list(posts)

    generate_recipes_page()

    index = replace_tag("posts", index_template, posts_list)
    write_file("generated/index.html", index)

generate_index()
copy_assets()