from net import *

with open("crickets.json") as f:
    cricket_names = eval(f.read())

targets = ""
with open("update.txt") as f:
    lines = [line.strip() for line in f]
    filename = lines[0]
print(f"Posting {filename}...")
print()
filedata = open(filename).read()

while len(cricket_names):
    print(json.dumps(cricket_names))
    cricket_name = cricket_names.pop()
    try:
        connect(f"CK_{cricket_name}")
        response = post_file("http://192.168.4.1/file", filename, filedata)
        print(response)            
    except Exception as e:
        print("Request failed:", e)
        cricket_names.insert(0, cricket_name)
    print()


"""
curl 192.168.4.1 -F file=@cricket/config.py
"""
