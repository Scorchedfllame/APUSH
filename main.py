from games.chronology import ChronologyTest


def main():
    game = ChronologyTest.create_game()
    game.start()


if __name__ == '__main__':
    while True:
        main()
