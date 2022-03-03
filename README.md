# Markdown-Documentation-Website

A project to make documenting easy and pretty.
Just throw in your .md files and get a ready Website.


# My Python implementation

## setting up the project

```bash
mkdir /var/www/website
git clone https://github.com/pIlIp-d/Markdown-Documentation-Website /var/www/website

#set group to apache2 user
sudo chgrp -R www-data /var/www/website

#set permission inheritence
sudo chmod -R g+s /var/www/website

#set group rights
sudo chmod -R g+rw /var/www/website

#make pythonscript executable
sudo chmod g+x /var/www/website/build_website.py
```
## file structure

website/  
├── **libs/**  
│   └── **[scripts].js**    - automatically added to html  
├── **style/**  
│   └── **[style].css**     - automatically added to html  
├── **pages/**  
│   └── **[pages].html**    - convertet md files  
├── **docs/**  
│   │── **subfolders/**  
│   │   └── **[more_docs].md**  
│   └── **[docs].md**       - raw md files  
├── **img/**                - address via `![Picture](/img/...)`  
│── **index.hp**            - created main page with all the links  
└── **build_website.py**    - script that is executed by index.php  

## Apache2

use apache2 to display the website

```bash
sudo apt install apache2

sudo nano /etc/apache2/sites-available/00-default.conf

#change
DocumentRoot /var/www/website
```
## update Markdown Files

### samba privileges

use samba share to work on your .md files
```bash
mkdir docs
chgrp -R www-data docs
adduser -a your_smb_user www-data

sudo chgrp -R www-data /var/www/*

apt install php libapache2-mod-php
```

### git sync

if your have a public server use [webhooks](https://docs.github.com/en/developers/webhooks-and-events/webhooks/creating-webhooks)<br>

another alternative is to write a php script that handles a git pull<br>

a cronjob would work too, but may be outdated sometimes<br>


# Dependencies

## Syntax Highlighting


- [Highlight.js](https://highlightjs.org/)

&ensp;&ensp;&ensp; Copyright (c) 2010, [Andris Reinman](http://www.andrisreinman.com)<br>
&ensp;&ensp;&ensp; Original Highlight.js Copyright (c) 2006, Ivan Sagalaev<br>
&ensp;&ensp;&ensp; [FULL LICENCE](/libs/LICENCE)


## Python Markdown Package

- [python-markdown](https://python-markdown.github.io/) - pip3 install markdown

### Toc extension

- [python-markdown.toc](https://python-markdown.github.io/extensions/toc/) - comes with markdown package

### Extra extension

- [python-markdown.extra](https://python-markdown.github.io/extensions/extra/) - comes with markdown package

## CSS sources

### github.css

&ensp;&ensp;&ensp; no original link found<br>
&ensp;&ensp;&ensp; Copyright (c) [Vasily Polovnyov](https://github.com/vast)

### Dark Theme Css

- [Tomorrow Night Theme](https://jmblog.github.io/color-themes-for-google-code-highlightjs)

# possible other ways

+ [mdbook](https://github.com/rust-lang/mdBook.git) - requires 64bit
+ [docosaurus](https://docusaurus.io) - modern, React.js, more Secure
+ [showdown](http://showdownjs.com/) - Node.js
+ [remarkable](https://github.com/jonschlinkert/remarkable) - Node.js good plugins (plugins didn't work as normal js)
