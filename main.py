from gamescene import GameScene


def main():
    
    # cols, rows, num bombs, screen size
    gamescene = GameScene(30, 16, 99, (320, 180))
    gamescene.loop()


if __name__ == "__main__":
    main()