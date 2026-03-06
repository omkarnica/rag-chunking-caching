

"""
Utility functions used across the RAG system.

This module keeps small helper functions that are shared
between different components like config loading, environment
setup, and simple logging.
"""

import yaml
from dotenv import load_dotenv


def load_config(config_path="config.yaml"):
    """
    Load configuration file.

    Parameters
    ----------
    config_path : str
        Path to the YAML configuration file.

    Returns
    -------
    dict
        Parsed configuration dictionary.
    """

    with open(config_path, "r") as file:
        config = yaml.safe_load(file)

    return config


def load_environment():
    """
    Load environment variables from .env file.

    This is mainly used for API keys such as:
    - GROQ_API_KEY
    """

    load_dotenv()


def log(message):
    """
    Simple logger used during debugging.

    Example:
        log("Running retrieval step")
    """

    print(f"[RAG] {message}")