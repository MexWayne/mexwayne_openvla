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
    
    # will load tall the tfrecord in one time

    # this way is OK
    #ds = tfds.load("droid_100", data_dir="/data/franka_droid/", split="train")

    # this way is OK too
    builder = tfds.builder_from_directory("/data/franka_droid/droid_100/1.0.0")
    ds = builder.as_dataset(split="train")
    print(builder.info.name)  # the droid 100 in put in the r2d2_faceblur that is why the tfds.load is ok

    images = []
    print("Total episodes:", sum(1 for _ in ds))

    for episode in ds.shuffle(10, seed=0).take(1):
      for i, step in enumerate(episode["steps"]):
        images.append(
          Image.fromarray(
            np.concatenate((
                  step["observation"]["exterior_image_1_left"].numpy(),
                  step["observation"]["exterior_image_2_left"].numpy(),
                  step["observation"]["wrist_image_left"].numpy(),
            ), axis=1)
          )
        )

    as_gif(images)
    os.system("xdg-open temp.gif" if os.name == "posix" else "start demo.gif")