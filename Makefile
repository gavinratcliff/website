POSTS_MD= $(wildcard posts/*.md)
POSTS_HTML = $(patsubst %.md,%.html,$(POSTS_MD))

POSTS_INDEX= "posts.html"

.PHONY: all

%.html: %.md
	python generate_markdown.py $^ $@

$(POSTS_INDEX): $(POSTS_HTML)
	python generate_posts_index.py

all: $(POSTS_HTML) $(POSTS_INDEX)
