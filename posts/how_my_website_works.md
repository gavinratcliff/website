How my website works
==============
***August 11th, 2024***

This is a short rundown of how I implemented my website (mostly so I can remember).

### Frontend

The frontend is built around a few [static assets](https://github.com/gavinratcliff/website/tree/main/assets) and a [simple Python script](https://github.com/gavinratcliff/website/blob/main/webhook_listener.py) that combines them all. There is a [posts directory](https://github.com/gavinratcliff/website/tree/main/posts) that contains all the markdown posts for the website. The script iterates over them and generates HTML with CommonMark, attaching a short header and footer HTML template. Finally, it builds out a short table of contents of posts for the index.

The rest of the assets are static and simply need to be copied over to the generated folder (which can be served by any web server).

### Deployment

There isn't a 'backend' per se, but I do have a few small deployment conveniences. First, [deploy.sh](https://github.com/gavinratcliff/website/blob/main/deploy.sh) generates the complete website and copies it into the directory my web server serves. Then, I configured GitHub to send my server a webhook whenever someone pushes to the blog repo. The [webhook listener](https://github.com/gavinratcliff/website/blob/main/webhook_listener.py) is always listening for this, and fetches the latest repo and runs the deploy script. This makes it super easy to update the website.

### Why I chose this

I like this simple implementation, as it greatly lowers the cognitive load of managing my website. If I want to post, I just make a new markdown file and commit it, and it will update without thought. It also requires very little in the way of extra libraries and doesn't require more than basic web and Python skills to understand. I think it will be easy to come back to and update it in a year or so. As a plus, I think it looks nice.

It's not perfect, though, and at some point, I hope to implement:

- An RSS feed for sending out my posts.
- Live-reloading for editing the website without having to regenerate.
- Some code to generate a random 3D polyhedron each time the website is opened.
- An active reading log with notes on books I like.