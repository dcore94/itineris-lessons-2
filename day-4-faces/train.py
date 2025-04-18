from PIL import Image, ImageDraw, ImageFont
import sys
import json

font = ImageFont.truetype("DejaVuSans.ttf", size=10)

filename = "picture"
image = Image.open(filename).convert("RGB")
draw = ImageDraw.Draw(image)
label = sys.argv[1]

embeddings = json.load(open("embeddings.json"))
resulting_embeddings = []
for emb in embeddings:
    box = tuple(emb["box"])
    if emb["confidence"] < 0.95:
        color = "red"
    else:
        color = "green"
        percentage = str(round(100 * emb["confidence"]))
        draw.text((box[0], box[3]), "It's a face with a confidence of " + percentage + "%", fill="cyan", font=font)
        emb["label"] = label
        resulting_embeddings.append(emb)
    draw.rectangle(box, width=3, outline=color)

image.save(label + ".jpg")
json.dump(resulting_embeddings, open(label + "_embeddings.json", "w"))