import logging

from bs4 import BeautifulSoup
import requests

from flask import Flask, render_template


HOST = 'https://github.com'

log = logging.getLogger(__name__)

log.setLevel(logging.DEBUG)

app = Flask(__name__)


def get_github_source(path,
        project='os-autoinst/os-autoinst-distri-opensuse',
        host=HOST):
    url = host + '/' + project + '/' + path
    #log.debug("url: {}".format(url))
    print("url: {}".format(url))
    response = requests.get(url)
    soup = BeautifulSoup(response.content)
    #current_file = soup.find(class_='file')
    current_file = soup.find(class_='repository-content')
    return current_file


@app.route('/source', defaults={'path': ''})
@app.route("/source/<path:path>")
def source(path):
    log.info("you requested {}".format(path))
    host = HOST
    project = 'os-autoinst/os-autoinst-distri-opensuse'
    response = requests.get(host + '/' + project + '/blob/master/' + path)
    soup = BeautifulSoup(response.content)
    # 'file' is a smaller excerpt as alternative to 'repository-content' in
    # get_github_source
    current_file = soup.find(class_='file')
    return render_template('layout.html.tmpl', source=current_file)


@app.route('/<owner>/<repo>/raw/<branch>/<path:path>')
def raw(owner, repo, branch, path):
    log.info("RAW: owner: {}, repo: {}, path: {}".format(owner, repo, path))
    #e.g. https://github.com/os-autoinst/os-autoinst-distri-opensuse/raw/master/tests/console/hostname.pm
    # TODO does not display correctly
    response = requests.get('/'.join([HOST, owner, repo, "raw", branch, path]))
    return response.content

@app.route('/<owner>/<repo>/<style>/<branch>/<path:path>')
def owner_repo(owner, repo, style, branch, path):
    log.info("owner: {}, repo: {}, path: {}".format(owner, repo, path))
    return render_template('layout.html.tmpl', source=get_github_source('/'.join([style, branch, path]), '/'.join([owner, repo])))


app.run(debug=True)
