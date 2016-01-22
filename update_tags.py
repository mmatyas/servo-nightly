#! /usr/bin/python

import json
import os
import requests
import subprocess


def delete_github_release(tagname):
    response = requests.get(release_api_url + '/tags/' + tagname)
    if "id" in response.json():
        headers = {"Authorization": "token " + os.environ['GITHUB_TOKEN']}
        requests.delete(release_api_url + "/" + str(response.json()["id"]), headers=headers)


def delete_git_tag(tagname):
    subprocess.check_call(['git', 'tag', '-d', tagname])
    subprocess.check_call(['git', 'push', 'origin', ':refs/tags/' + tagname])


def create_git_tag(tagname):
    subprocess.check_call(['git', 'tag', tagname])
    subprocess.check_call(['git', 'push', 'origin', '--tags'])


def delete_all_git_tags():
    all_tags = subprocess.check_output(['git', 'tag']).split()
    for tag in all_tags:
        delete_github_release(tag)
        delete_git_tag(tag)
        print "Tag '" + tag + "' deleted"


def generate_tag_name():
    os.chdir(os.getcwd() + '/servo')
    current_short_hash = subprocess.check_output(['git', 'rev-parse', 'HEAD'])[:8]
    os.chdir('..')
    return 'v' + current_short_hash;


def create_new_git_tag_if_not_latest():
    new_tag_name = generate_tag_name()

    # If not exists yet, delete old tags and create a new one
    call = subprocess.Popen(['git', 'rev-parse', '--verify', new_tag_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if "fatal" in call.communicate()[1]:
        delete_all_git_tags()
        create_git_tag(new_tag_name)
    else:
        print "Already on latest tag"

    return new_tag_name


if __name__ == "__main__":
    release_api_url = 'https://api.github.com/repos/mmatyas/servo-nightly/releases'
    subprocess.check_call(['git', 'fetch', '--tags'])
    subprocess.check_call(['git', 'remote', 'set-url', 'origin', 'https://' + os.environ['GITHUB_TOKEN'] + '@github.com/mmatyas/servo-nightly.git'])

    print "Latest tag: " + create_new_git_tag_if_not_latest()
