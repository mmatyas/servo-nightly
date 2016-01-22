#! /usr/bin/python

import os
import requests
import subprocess
import json


def create_github_release_if_not_exists(tagname):
    release_id = ""
    upload_url = ""

    response = requests.get(release_api_url + "/tags/" + tagname)
    if "upload_url" in response.json():
        upload_url = response.json()["upload_url"]
        release_id = response.json()["id"]
    else:
        data = { "tag_name" : tagname, "name" : "Nightly build" }
        headers = {"Authorization": "token " + os.environ['GITHUB_TOKEN']}
        response = requests.post(release_api_url, data=json.dumps(data), headers=headers)
        if "upload_url" in response.json():
            upload_url = response.json()["upload_url"]
            release_id = response.json()["id"]
            print "New GitHub release created"
        else:
            raise RuntimeError(response.json())

    return release_id, upload_url.split('{')[0]


def upload_archive(upload_url, filepath, asset_name):
    command = ["curl"]
    command.extend(["-H", "Authorization: token " + os.environ['GITHUB_TOKEN']])
    command.extend(["-H", "Content-Type: application/zip"])
    command.extend(["-X", "POST"])
    command.extend(["-T", filepath])
    command.extend(["--max-time", "60"])
    command.append(upload_url + "?name=" + asset_name)

    return subprocess.check_output(command)


def delete_release_asset_if_exists(release_id, asset_name):
    response = requests.get(release_api_url + "/" + str(release_id) + "/assets")
    asset_id = ""
    for asset in response.json():
        if "name" in asset:
            if asset["name"] == asset_name:
                asset_id = str(asset["id"])

    if len(asset_id) == 0:
        return

    headers = {"Authorization": "token " + os.environ['GITHUB_TOKEN']}
    requests.delete(url=release_api_url + "/assets/" + asset_id, headers=headers)
    return response.json()


def upload_and_replace_archive(release_id, upload_url):
    asset_name = os.environ['ASSET_NAME']
    filepath = os.getcwd() + "/servo/" + asset_name

    print "Source file: " + filepath
    print "GitHub asset name: " + asset_name

    delete_release_asset_if_exists(release_id, asset_name)
    upload_archive(upload_url, filepath, asset_name)


if __name__ == "__main__":
    release_api_url = 'https://api.github.com/repos/mmatyas/servo-nightly/releases'
    subprocess.check_call(['git', 'fetch', '--tags'])

    last_tag = subprocess.check_output(['git', 'describe', '--abbrev=0', '--tags'])
    print "Latest tag: " + last_tag

    release_id, upload_url = create_github_release_if_not_exists(last_tag)
    upload_and_replace_archive(release_id, upload_url)

    print "Done"
