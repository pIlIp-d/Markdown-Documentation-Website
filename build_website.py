#!/usr/bin/env python3

import markdown
import os, time
from datetime import datetime
import shutil

#--config--
remove_old_files_at_every_build = True #disable if you manually add or edit /pages files

ROOT_DIR=os.getcwd()

def get_path_for_html(md_path):
    return md_path[:-2]+"html"

def get_file_list(path):
    list_of_files = []
    for root, dirs, files in os.walk(path):
        for file in sorted(files):
            list_of_files.append(os.path.join(root,file))
    return list_of_files

def convert_md_to_html(file):
    config = {
        'extra': {
            'footnotes': {
                'UNIQUE_IDS': True
            }
        },
        'toc': {
            'title':"Contents"
        }
    }
    return markdown.markdown(file, extensions=['extra', 'toc'], extension_configs=config)
    
def save_file(text, output_file):
    os.makedirs(os.path.split(output_file)[0], exist_ok=True)#create directory if doesn't exist
    
    with open(output_file, "w+") as f:
        f.write(text)

def convert_and_save_files(file_list):
    for file in file_list:
        if file[-2:] == "md":
            with open(file, "r") as f:
                html = convert_md_to_html(f.read())
                save_file(make_proper_html(html), ROOT_DIR+'/pages/'+get_path_for_html(file.replace(ROOT_DIR+"/docs/","")))

def make_proper_html(body, php = False):    
    html = "<!DOCTYPE html><html><head><meta charset='UTF-16'></head>"
    for css_file in get_file_list(ROOT_DIR+r"/style/"):
        if css_file[-4:] == ".css":
            html += "<link rel='stylesheet' href='"+ css_file.replace(ROOT_DIR,"") +"'>"
    for js_file in get_file_list(ROOT_DIR+r"/libs/"):
        if js_file[-3:] == ".js":
            html += "<script src='"+ js_file.replace(ROOT_DIR,"") +"'></script>"
    html += "<script>hljs.initHighlightingOnLoad();</script>"#load syntax highlighting
    if php:
        html += "<?php ini_set('display_errors', 1);if (isset($_GET['rebuild'])){ $out = shell_exec('python3 /var/www/website/build_website.py');"
        html += "echo $out;"
        html += "echo \"<form action='/index.php' method='get'></form><script>setTimeout(1000);location.href = location.href.split('?')[0]</script>\";}?>"
    else:
        html += "<a href='/index.php'>Main Page</a>"
    html += body
    button = "<form action='/index.php' method='get'><input id='rebuild_btn' type='submit' name='rebuild' value='Rebuild HTML'></form>"
    html += "<br><br>"
    html += "<footer>"+ button +"<span id='footer'> Last Build: "+ datetime.now().strftime("%Y-%m-%d  %H:%M:%S") +"  <a href='https://github.com/pIlIp-d/Markdown-Documentation-Website'>pilip-d</a></span></footer>"
    html += "</body></html>"
    return html

def get_creation_time(path):
    ctime = os.path.getmtime(path)
    ctime = time.ctime(ctime)
    t_obj = time.strptime(ctime)
    return time.strftime("%Y-%m-%d %H:%M:%S", t_obj)

def create_index_php(file_list):
    md = "# Documentation Website\n"
    for file in file_list:
        # adding indent for folder strukture
        depth = len(file.split("/")) - 2 - len(ROOT_DIR.split("/"))
        for i in range(depth):
            md += "\t"
        # add markdown line
        path_to_html = get_path_for_html(file).replace(ROOT_DIR+"/","").replace("docs/","")
        print(file +" >> pages/"+path_to_html)#show progress
        md += "+ _"+ get_creation_time(file) +"_ >> ["+ path_to_html[:-5] +"](/pages/"+ path_to_html +") \n"
    #save index.html
    with open("index.php", "w") as f:
        f.write(make_proper_html(convert_md_to_html(md), True))

def remove_old_version():
    path=ROOT_DIR+'/pages/'
    os.makedirs(os.path.dirname(path), exist_ok=True)#create directory if doesn't exist for the first execution
    shutil.rmtree(path)

def __main__():
    file_list = get_file_list(ROOT_DIR + r'/docs/')
    if remove_old_files_at_every_build:
        remove_old_version()
    convert_and_save_files(file_list)
    create_index_php(file_list)
    print(datetime.now().strftime("%Y-%m-%d  %H:%M:%S"))

if __name__ == '__main__':
    __main__()
