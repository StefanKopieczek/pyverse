import bad_sonnet


def sonnet():
    while True:
        try:
            return bad_sonnet.Sonnet()
            break
        except IndexError:
            pass

if __name__ == "__main__":
    print sonnet()
