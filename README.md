# Book A Meal API :pizza:
[![Build Status](https://travis-ci.org/codingedward/book-a-meal-api.svg?branch=develop)](https://travis-ci.org/codingedward/book-a-meal)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/49c7aa4533664706889b54e1254a4b6f?branch=develop)](https://www.codacy.com/app/codingedward/book-a-meal-api?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=codingedward/book-a-meal&amp;utm_campaign=Badge_Grade)
[![Coverage Status](https://coveralls.io/repos/github/codingedward/book-a-meal/badge.svg?branch=develop)](https://coveralls.io/github/codingedward/book-a-meal-api?branch=develop)

This is the Andela Book-A-Meal web project challenge API.

**Note**: The UI template is [here](https://codingedward.github.io/book-a-meal-ui).

**Note**: The PivotalTracker project is
[here](https://www.pivotaltracker.com/n/projects/2165567). 

**Note**: The documentation for the API is 
[here](https://mealbooking.docs.apiary.io)

## Table of Content

  * [Introduction](#introduction)
  * [The API](#the-server-side)
     * [Installation](#installation)
     * [Configuration](#configuration)
     * [Running](#running)
     * [Testing](#testing)

## Introduction
The project entails having a caterer as the site administrator and can add 
meals to the application as well as set menus for a particular day. 
The customers, after signing up first, are then allowed to book meals online.

## The API

This application uses Flask Python web microframework to create a RESTful 
API.

**Note**: The documentation for the API is [here](https://mealbooking.docs.apiary.io).

### Installation

To have the API running, you will have to have `pipenv` package manager. To 
install this, run the following command:
```
$ pip install pipenv
```
Then, change directory to the top level directory of the project `/book-a-meal-api`.
```
$ cd book-a-meal-api
```
Next, you have to install the applications dependancies.
```
$ pipenv install
```

### Configuration

This application requires some configuration held in the `.env` file.
For this, the `.env.example` file has already been provided and you simply have
to copy paste it to a `.env` file. That is:
```
$ cp .env.example .env
```

Then, ensure you **fill in the required values** in the configuration file.


### Running

This part assumes you have already configured your application as described 
above. To access the virtual enviroment created by `pipenv`, run:
```
$ pipenv shell
```
This will load the environment variables and create your virtual environment.  
To run your application, simply run:
```
$ flask run
```
You should then have your application up and running:
```
 * Serving Flask app "run" 
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit) 
```

### Testing

The application was built using TDD pattern and therefore has tests that can
be run using `nose` test runner. To run these tests, simply run `nosetests`:
```
$ nosetests --with-coverage --cover-package app
```

TIA!
