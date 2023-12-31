import os
import time

import mss
import numpy as np
from dotenv import load_dotenv
from slack_sdk.webhook import WebhookClient

load_dotenv()

PLAYERS = {
    (64, 103, 73): "Verdant",
    (112, 48, 48): "Indigo",
    (112, 48, 112): "Rose",
    (48, 112, 112): "Ochre",
    (48, 48, 112): "Crimson",
}


def main():
    webhook = WebhookClient(os.environ["SLACK_WEBHOOK_URL"])
    current_player = None

    with mss.mss() as sct:
        while True:
            monitor = {"top": 0, "left": 0, "width": 100, "height": 100}
            img = np.array(sct.grab(monitor))[:, :, :3]

            if (img == img[0, 0]).all() and tuple(img[0, 0]) in PLAYERS:
                new_player = PLAYERS[tuple(img[0, 0])]
                if new_player != current_player:
                    webhook.send(text=f"It's the *{new_player}* player's turn!")
                    current_player = new_player
                    print(new_player)

            time.sleep(0.2)


if __name__ == "__main__":
    main()
