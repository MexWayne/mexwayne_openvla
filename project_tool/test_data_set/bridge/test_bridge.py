# Available Features (note that 'reward' is a dummy feature at the moment)
import tensorflow_datasets as tfds
import numpy as np
from PIL import Image
from IPython import display
import os


def as_gif(images, path="temp.gif"):
  # Render the images as the gif (15Hz control frequency):
  # the 31 tfrecord cantian 100 episodes
  images[0].save(path, save_all=True, append_images=images[1:], duration=int(1000/15), loop=0)
  gif_bytes = open(path,"rb").read()
  return gif_bytes

if __name__ == "__main__":
    
    # will load tall the tfrecord in one time, this way is no OK
    #ds = tfds.load("BridgeData V2", data_dir="/data", split="train")
    
    # this way is OK
    builder = tfds.builder_from_directory("/data/bridge_orig/1.0.0")
    ds = builder.as_dataset(split="train") 


    images = []
    print("Total episodes:", sum(1 for _ in ds))

    for episode in ds.shuffle(10, seed=0).take(1):
      for i, step in enumerate(episode["steps"]):
        images.append(
          Image.fromarray(
            np.concatenate((
                  step["observation"]["image_0"].numpy(),
                  step["observation"]["image_1"].numpy(),
                  step["observation"]["image_2"].numpy(),
                  step["observation"]["image_3"].numpy(),
            ), axis=1)
          )
        )

    as_gif(images)
    os.system("xdg-open temp.gif" if os.name == "posix" else "start demo.gif")



    builder = tfds.builder_from_directory(builder_dir="/data/bridge_orig/1.0.0")
    print(builder.info.features)