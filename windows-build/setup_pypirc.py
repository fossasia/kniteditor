import os

pypi_template = \
    "\\r\\n[distutils]\\r\\nindex-servers =\\r\\n    pypi\\r\\n\\r\\n" \
    "[pypi]\\r\\nusername:{PYPI_USERNAME}\\r\\npassword:{PYPI_PASSWORD}\\r\\n"

if __name__ == "__main__":
    pypirc = os.path.join(os.environ["HOME"], ".pypirc")

    pypi_configuration = pypi_template.format(**os.environ)

    with open(pypirc, "w") as file:
        file.write(pypi_configuration)
    print("Wrote configuration to \"{}\"".format(pypirc))
