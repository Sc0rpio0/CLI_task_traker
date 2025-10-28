from setuptools import setup, find_packages

setup(
    name="task-cli",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "typer[all]",
    ],
    entry_points={
        "console_scripts": [
            "task-cli=task_cli.main:app",
        ],
    },
)
