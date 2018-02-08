# personal-website-001
@KartoffelCheetah 's first website's repo.

I uploaded my first website so you can have a look at it or do what you want with it.
Feel free to use it for your own website if you like. I already added some images as placeholders.

Please note that the server is set in development mode. Do not run it directly in production environment. This is intentional, because it is likely that future users will first want to develop.
**Before going into production please switch to production mode! Or (better) use some production ready WSGI server on top like described below.**

## Dependencies:

- ImageMagick, Python3 and Flask installed on your computer.
- Optionally install npm and Node.js if you wish to edit the Stylus stylesheets.
- @Deevad 's [Pepper&Carrot Fonts](https://github.com/Deevad/peppercarrot_fonts)
- [JQuery-3.2.1](http://jquery.com/) (included)

**Note:** favicons were generated by @RealFaviconGenerator 's [RealFaviconGenerator](https://realfavicongenerator.net/).

## Installation:

In the following I assume you have Python3 with Flask installed.

Navigate to the chosen folder to clone the repo:

```git clone https://github.com/KartoffelCheetah/personal-website-001.git```

```
personal-website-001
│  server.py     # ./server.py will run the development server
│  main.py       # ./main.py is the interface for common tasks
│  db.py         # these are the function defs of the db
│  package.json
│  LICENSE
│  README.md
└───templates
          # jinja templates
└───staging_area
          # place here images before making them public
└───static
          # static files to serve
```

You need to clone [Pepper&Carrot Fonts](https://github.com/Deevad/peppercarrot_fonts):

```cd ./personal-website-001/static/ && mkdir fonts && cd fonts && git clone https://github.com/Deevad/peppercarrot_fonts```

**Optional:**
If you prefer to use Stylus instead of pure CSS install npm and Node.
Then use `npm run styl` to run the compiler from the main directory. For details check the [package.json](./package.json) file.

**Set up database:**
1. Put your drawigns inside [staging_area/drawings/](./staging_area/drawings)
2. Put your photos inside [staging_area/photos/](./staging_area/photos/)<some_subdir>/
3. Run [main.py](./main.py) and select Create database
4. Run [main.py](./main.py) and select Create Staging file
5. Edit the staing file
6. Run [main.py](./main.py) and select Use Staging file

To run the development server just run [server.py](./server.py).

**You set up everything for a development server.**

To set up a production server you need additional WSGI tools.
Install [gunicorn](http://gunicorn.org/) for example.
```pip3 install gunicorn```
Then just use something like ```gunicorn -w 4 server:app```.
