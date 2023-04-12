import re
import json
import subprocess
import os

# Define GitHub API endpoint and repo URL
api_endpoint = "https://api.github.com/repos/TASVideos/BizHawk/releases"
repo_url = "https://github.com/TASVideos/BizHawk/releases/download"
output_file = 'bizhawk_curl.json'

# Check if the output file exists
if os.path.exists(output_file):
    # Load the JSON data from the existing file
    print(f"Loading data from local file: {output_file}")
    with open(output_file, 'r') as f:
        data = json.load(f)
else:
    print(f"Downloading data from GitHub API: {api_endpoint}")
    # Send a request to the GitHub API and load the response into a JSON object
    curl_command = ['curl', '-L', '-o', output_file, api_endpoint]
    subprocess.run(curl_command, check=True)
    # Load the JSON data from the new file
    with open(output_file, 'r') as f:
        data = json.load(f)

versions = []
for i in data:
    for j in i['assets']:
        url = j['browser_download_url']
        name = j['name']
        match = re.search(r'^(?!.*(?:linux|tar|rar))(?:https?://)?[\w./-]+-(?:(?!linux|tar|rar)\S)+\.\w{2,4}$', url)
        if match:
            versions.append({'name':name,'url':url})
            version = match.group()
            print(version)

        
for v in versions:
    # The 'name' field is expected to be in the format "Bizhawk-x.x.x.zip" or "win-x64" and remove the .zip
    version = os.path.splitext(v['name'])[0]
    # Get the URL for the binary file
    file_url = v['url']
    # Construct the Lutris installation script
    script = {
        "count": 1,
        "next": None,
        "previous": None,
        "results": [
            {
                "id": 31075,
                "game_id": 191087,
                "game_slug": "bizhawk",
                "name": "Bizhawk",
                "year": None,
                "user": "",
                "runner": "wine",
                "slug": "bizhawk-windows",
                "version": "Windows",
                "description": f"Version {version}",
                "notes": "",
                "credits": "",
                "created_at": "2021-12-30T00:27:03.257000Z",
                "updated_at": "2022-01-01T14:55:13.466623Z",
                "draft": False,
                "published": True,
                "published_by": 64834,
                "rating": "",
                "is_playable": None,
                "steamid": None,
                "gogid": None,
                "gogslug": "",
                "humbleid": "",
                "humblestoreid": "",
                "humblestoreid_real": "",
                "script": {
                    "files": [
                        {
                            "bizhawk": file_url
                        }
                    ],
                    "game": {
                        "arch": "win64",
                        "exe": f"drive_c/Program Files/{version}/EmuHawk.exe",
                        "prefix": "$GAMEDIR"
                    },
                    "installer": [
                        {
                            "task": {
                                "arch": "win64",
                                "name": "create_prefix",
                                "prefix": "$GAMEDIR"
                            }
                        },
                        {
                            "extract": {
                                "dst": f"$GAMEDIR/drive_c/Program Files/{version}",
                                "file": "bizhawk"
                            }
                        }
                    ]
                },
                "content": f"files:\n- bizhawk: {file_url}\ngame:\n  arch: win64\n  exe: drive_c/Program Files/BizHawk-2.7/EmuHawk.exe\n  prefix: $GAMEDIR\ninstaller:\n- task:\n    arch: win64\n    name: create_prefix\n    prefix: $GAMEDIR\n- extract:\n    dst: $GAMEDIR/drive_c/Program Files/BizHawk-2.7\n    file: bizhawk\n",
                "discord_id": ""
            }
        ]
    }

    # Save the Lutris installation script to a file
    with open(f"bizhawk_{version}.json", "w") as file:
        json.dump(script, file, indent=4)
