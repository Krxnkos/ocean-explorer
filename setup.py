from setuptools import setup, find_packages

setup(
    name="ocean_explorer",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "pygame>=2.0.0",
    ],
    author="South Hampshire College Group",
    description="An interactive educational game for children to learn about sea creatures",
    keywords="education, children, ocean, game",
    python_requires=">=3.6",
)
