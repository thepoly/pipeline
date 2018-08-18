# Pipeline

Pipeline is [_The Rensselaer Polytechnic_](https://poly.rpi.edu)'s next
website. It will enable rapid development of new article layouts and
interactive features. In the long term, it will provide a solid platform for
our content over the coming decade, supporting _The Poly_'s new focus on
online-first journalism.

## Requirements

Ensure these are installed before continuing.

- [Python 3.7](https://www.python.org)
- [Pipenv](https://docs.pipenv.org)
- [npm](https://www.npmjs.com/get-npm)

## Getting started

Pipeline is written in Python. It uses Sass and PostCSS on the frontend. To
run it for development:

### Installing

```
git clone git@github.com:thepoly/pipeline.git
cd pipeline
pipenv install
npm install
npx wp --config webpack.development.config.js
```

### Running

```
pipenv shell
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```
