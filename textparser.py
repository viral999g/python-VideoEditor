file = open("/home/bharat/Downloads/videoEditor/videos/demo.mp4.log", "r")
logs = []

for f in file:
    if "frame= " in f:
        logs.append(f.replace("\n", ""))

log = logs[-1]
start = log.find("=")
end = log.find("fps")
print(log[start + 1: end].strip())
