import os

if __name__ == "__main__":
    pypirc = os.path.join(os.environ["HOME"], ".pypirc")

    pypi_configuration = """
    [distutils]
    index-servers =
        pypi

    [pypi]
    username:{PYPI_USERNAME}
    password:{PYPI_PASSWORD}
    """.format(**os.environ)

    with open(pypirc, "w") as file:
        file.write(pypi_configuration)
