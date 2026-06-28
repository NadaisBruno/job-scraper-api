from scraper import extract_data


def main():
    extract_data("python developer", "Lisboa")


# garante que o scraper so corre quando executamos este ficheiro directamente
# evitando executar automaticamente durante imports ou testes
if __name__ == "__main__":
    main()
