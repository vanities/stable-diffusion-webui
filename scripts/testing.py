import math
import os
import sys
import traceback
import random
import json

from nltk import tokenize
import nltk
import modules.scripts as scripts
import gradio as gr
from scripts.the_prophet import the_prophet
from scripts.wordle import wordle
from scripts.dracula import dracula

from modules.processing import Processed, process_images
nltk.download('punkt', download_dir=".")


class Script(scripts.Script):
    def title(self):
        return "To Infinity and Beyond"

    def ui(self, is_img2img):
        return []

    def run(self, p):
        title = "random"
        description = "random"
        n = 100
        metadatas = []
        promptx = tokenize.sent_tokenize(the_prophet)
        #promptx = tokenize.sent_tokenize(dracula)
        for i in range(int(n)):
            seed = random.randint(0, 10000000)
            sampling_steps = random.randint(20, 64)
            #prompt = random.sample(wordle, 12)
            prompt = random.sample(promptx, 1)
            split_prompt = ", ".join(prompt)
            p.sampling_steps = sampling_steps
            p.prompt = prompt
            p.restore_faces = True
            p.seed = seed
            proc = process_images(p)
            image = proc.images
            attributes = [{"trait_type": f"Prompt #{prompt.index(x)}", "value": x} for x in prompt]
            attributes.append({"trait_type": "Seed", "value": p.seed})
            attributes.append({"trait_type": "Sampling Steps", "value": p.sampling_steps})
            #attributes.append({"trait_type": "Sampling Method", "value": p.sampling_method})

            metadata = {
              "name": f"{title} #{i}",
              "description": description,
              "token_id": i,
              "edition": i,
              "attributes": attributes
                }
            metadatas.append(metadata)
            with open(f"nft/metadata/{i}", "w") as f:
                json.dump(metadata, f)
            
            image[0].save(f"nft/images/{i}.png")
        with open(f"nft/metadata/_metadata.json", "w") as f:
            json.dump(metadatas, f)
        return Processed(p, image, p.seed, "")
