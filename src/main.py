import json
from generate_path import Path_plan

gcp = []  # You will pass this from Node

def run_path(gcp_input):
    global gcp
    gcp = gcp_input
    #print(gcp)
    out = Path_plan(gcp, 2.2, 3.4, 2.2)
    track, headland = out.path()
    return {
        "track": track,
        "headland": headland
    }

if __name__ == "__main__":
    import sys
    data = json.loads(sys.stdin.read())
    #print(data)
    result = run_path(data["gcp"])
    print(json.dumps(result))

