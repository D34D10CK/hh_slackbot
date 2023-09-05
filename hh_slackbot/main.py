import os
import time

import mss
import numpy as np
from dotenv import load_dotenv
from slack_sdk.webhook import WebhookClient

load_dotenv()

PLAYERS = {
    (64, 103, 73): "Verdant Delirium",
    (112, 48, 48): "Indigo Decay",
    (112, 48, 112): "Rose Arcane",
    (48, 112, 112): "Ochre Wild",
    (48, 48, 112): "Crimson Earthen",
}


def main():
    webhook = WebhookClient(os.environ["SLACK_WEBHOOK_URL"])
    current_player = None

    with mss.mss() as sct:
        while True:
            monitor = {"top": 0, "left": 0, "width": 100, "height": 100}
            img = np.array(sct.grab(monitor))[:, :, :3]

            if (img == img[0, 0]).all() and tuple(img[0, 0]) in PLAYERS:
                new_player = PLAYERS[(img[0, 0, 0], img[0, 0, 1], img[0, 0, 2])]
                if new_player != current_player:
                    webhook.send(text=f"It's {new_player}'s turn!")
                    current_player = new_player
                    print(new_player)

            time.sleep(0.2)


if __name__ == "__main__":
    main()
