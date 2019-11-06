# Voluble

![](https://img.shields.io/travis/zar3bski/voluble)


**Volubile** is a simple yet modular *Content Managment System* designed so that you can focus on what's important: **the content**. Whether you want to use it as a blog, a professional web page or a gallery, with a few ticks in a single administration panel, you can switch from one mode to another without spending frustrating hours struggling with obscure and redondant options.

## Components

|          | 
|---------:|
| Django   | 
| Gunicorn | 
| Spectre  |

## Installation

### Development version

You'll need a [Docker engine](https://docs.docker.com/install/) and [Docker-compose](https://docs.docker.com/compose/install/). The easiest way to run the app with the dev server and a populated Maria database is to: 

**Clone the repo**

```
git clone https://github.com/zar3bski/personal_cms
cd personal_cms
```
and run 

```
docker-compose up -d
```
Have then a look at `localhost:8000`

### Production version

default test credentials `john` : `478951236a` 
