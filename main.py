from gamescene import GameScene


def main():

    gamescene = GameScene(16, 30, 99, (800, 450))
    gamescene.loop()


if __name__ == "__main__":
    main()