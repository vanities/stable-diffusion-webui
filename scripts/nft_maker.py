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
from scripts.bank import bank

from modules.processing import Processed, process_images

nltk.download("punkt", download_dir=".")

NUM_OF_NFTS = 10
NUM_OF_EMOTIONS = 3
NUM_OF_SIZE_AND_STRUCTURES = 3
NUM_OF_VIBES = 3
NUM_OF_ILLUSTRATIONS = 1


class Script(scripts.Script):
    def title(self):
        return "NFT Maker"

    def ui(self, is_img2img):
        return []

    def run(self, p):
        title = "random"
        description = "random"
        metadatas = []
        sentences = tokenize.sent_tokenize(the_prophet)
        for i in range(int(NUM_OF_NFTS)):
            seed = random.randint(0, 1000000000)
            sampling_steps = random.randint(40, 70)

            random_emotion_key = random.sample(bank["Emotions"].keys(), 1)[0]
            emotions = random.sample(
                bank["Emotions"][random_emotion_key], NUM_OF_EMOTIONS
            )
            random_size_and_structure_key = random.sample(
                bank["Size and Structure"].keys(), 1
            )[0]
            size_and_structure = random.sample(
                bank["Size and Structure"][random_size_and_structure_key],
                NUM_OF_SIZE_AND_STRUCTURES,
            )
            random_vibe_key = random.sample(bank["Vibes"].keys(), 1)[0]
            vibes = random.sample(bank["Vibes"][random_vibe_key], NUM_OF_VIBES)
            illustration = random.sample(bank["Illustrations"], NUM_OF_ILLUSTRATIONS)

            prompt = (
                random.sample(sentences, 1)
                + emotions
                + size_and_structure
                + vibes
                + illustration
            )
            split_prompt = ", ".join(prompt)
            p.sampling_steps = sampling_steps
            p.prompt = prompt
            p.restore_faces = True
            p.cfg_scale = random.randint(10, 30)
            p.seed = seed
            proc = process_images(p)
            image = proc.images
            attributes = [
                {"trait_type": f"Prompt #{prompt.index(x)}", "value": x} for x in prompt
            ]
            attributes.append({"trait_type": "Seed", "value": p.seed})
            attributes.append(
                {"trait_type": "Sampling Steps", "value": p.sampling_steps}
            )
            # attributes.append({"trait_type": "Sampling Method", "value": p.sampling_method})

            metadata = {
                "name": f"{title} #{i}",
                "description": description,
                "token_id": i,
                "edition": i,
                "attributes": attributes,
            }
            metadatas.append(metadata)
            with open(f"nft/metadata/{i}", "w") as f:
                json.dump(metadata, f)

            image[0].save(f"nft/images/{i}.png")
        with open(f"nft/metadata/_metadata.json", "w") as f:
            json.dump(metadatas, f)
        return Processed(p, image, p.seed, "")
