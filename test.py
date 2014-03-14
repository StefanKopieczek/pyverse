import bad_sonnet

def sonnet():
    while True:
        try:
            print bad_sonnet.Sonnet()
            break
        except IndexError:
            pass
