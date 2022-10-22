#!/bin/bash

cd .. && rsync -avzhr --progress --stats \
  --exclude ".git" \
    pc:/mnt/ssd/home/vanities/stable-diffusion/stable-diffusion-webui .
