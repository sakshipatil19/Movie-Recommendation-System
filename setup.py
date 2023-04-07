from setuptools import setup

## edit below variables as per your requirements -
REPO_NAME = "Movie Recommendation System"
AUTHOR_USER_NAME = "Sakshi"
SRC_REPO = "src"
LIST_OF_REQUIREMENTS = ['streamlit']


setup(
    name=SRC_REPO,
    version="0.0.1",
    author=AUTHOR_USER_NAME,
    description="A small package for Movie Recommender System",
    # long_description=long_description,
    long_description_content_type="text/markdown",
    url=f"https://github.com/sakshipatil19/Movie-Recommendation-System",
    author_email="abc@gmail.com",
    packages=[SRC_REPO],
    license="MIT",
    python_requires=">=3.7",
    install_requires=LIST_OF_REQUIREMENTS
)
