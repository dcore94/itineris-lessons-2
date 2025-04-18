from PIL import Image, ImageDraw, ImageFont
import requests
import sys
import json
import os

face_service = sys.argv[1]
threshold = float(sys.argv[2])

font = ImageFont.truetype("DejaVuSans.ttf", size=50)
image = Image.open("picture").convert("RGB")
draw = ImageDraw.Draw(image)

source_findings = json.load(open("embeddings.json"))
source_embeddings = [s["embedding"] for s in source_findings]
folder = "target_embeddings"
for target_file in os.listdir(folder):
    fpath = os.path.join(folder, target_file)
    target = json.load(open(fpath))
    label = target[0]["label"]
    print("Extracted", len(target), " target embeddings for ", label)
    for tgt in target:
        embedding = tgt["embedding"]
        print("Calling face service for comparing embeddings with target", label)
        reqjson = {
            "sources" : source_embeddings,
            "target" : embedding,
            "threshold" : threshold
        }
        resp = requests.post(face_service, json=reqjson)
        print(resp.status_code, resp.text)
        if resp.ok:
            matches = resp.json()
            for i in range(len(matches)):
                match = matches[i]
                if match["match"]:
                    box = tuple(source_findings[i]["box"])
                    color = "red" if match["similarity"] < 0.8 else "green"
                    draw.rectangle(box, width=3, outline=color)
                    percentage = round(100 * match["similarity"])
                    draw.text((box[0],box[3]), label + " (" + str(percentage) +"%)", fill="cyan", font=font)
        else:
            print("Error calling face compare service")

print("Saving output image")
image.save("output.jpg")
