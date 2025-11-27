import config

# from config import edgepf

config.initConfig()


def main():
    global edgepf
    print(1, config.edgepf, edgepf)
    config.edgepf = "Abcdef1"
    print(2, config.edgepf, edgepf)
    edgepf = "fedcbA1"
    print(3, config.edgepf, edgepf)
    config.edgepf = "Abcdef2"
    print(4, config.edgepf, edgepf)
    edgepf = "fedcbA2"
    print(5, config.edgepf, edgepf)


main()
