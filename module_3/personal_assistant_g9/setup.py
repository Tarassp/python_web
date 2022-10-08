from setuptools import setup, find_namespace_packages

setup(
    name="personal_assistant_g9",
    version="0.0.2",
    description="Personal Assistant can help you organize your Contacts, Notes and Files",
    author="Team-lead Taras Spasibov, project group 9",
    author_email="spasibovtaras@gmail.com",
    license="MIT",
    packages=find_namespace_packages(),
    entry_points={"console_scripts": ["assistant=main:main"]},
)
