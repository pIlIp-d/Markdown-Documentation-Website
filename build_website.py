import markdown
import os, time
import shutil

def get_path_for_html(md_path):
    return md_path.replace("/var/www/website/","").replace("docs/","")[:-2]+"html"

def get_file_list(path):
    list_of_files = []
    for root, dirs, files in os.walk(path):
        for file in files:
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
    os.makedirs(os.path.dirname(output_file), exist_ok=True)#create directory if doesn't exist
    with open(output_file, "w+") as f:
        f.write(text)

def convert_and_save_files(file_list):
    for file in file_list:
        with open(file, "r") as f:
            html = convert_md_to_html(f.read())
            save_file(make_proper_html(html), 'pages/'+get_path_for_html(file))

def make_proper_html(body):
    html = "<!DOCTYPE html><html><head><meta charset='UTF-16'></head>"
    html += "<link rel='stylesheet' href='/github.css'>"
    html += "<link rel='stylesheet' href='/style.css'>"
    html += "<script src='/libs/highlight.pack.js'></script>"
    html += "<script>hljs.initHighlightingOnLoad();</script>"
    html += body
    html += "</body></html>"
    return html

def get_creation_time(path):
    ctime = os.path.getmtime(path)
    ctime = time.ctime(ctime)
    t_obj = time.strptime(ctime)
    return time.strftime("%Y-%m-%d %H:%M:%S", t_obj)

def create_index_html(file_list):
    md = "# Documentation Website\n"
    for file in file_list:
        # adding indent for folder strukture
        depth = len(file.split("/"))-2
        for i in range(depth):
            md += "\t"
        # add markdown line
        path_to_html = get_path_for_html(file)
        print(file +" >> pages/"+path_to_html)#show progress
        md += "+ _"+ get_creation_time(file) +"_ >> ["+ path_to_html[:-5] +"](/pages/"+ path_to_html +") \n"
    #save index.html
    with open("index.html", "w+") as f:
        f.write(make_proper_html(convert_md_to_html(md)))

def remove_old_version():
    path='pages/'
    os.makedirs(os.path.dirname(path), exist_ok=True)#create directory if doesn't exist for the first execution
    shutil.rmtree(path)

def __main__():
    file_list = get_file_list(r'docs/')
    remove_old_version()
    convert_and_save_files(file_list)
    create_index_html(file_list)

__main__()
