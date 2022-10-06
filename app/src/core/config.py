import os


class Config:
    DB_USERNAME = os.getenv("DB_USERNAME", "root")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "root")
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", "32701")
    DB_NAME = os.getenv("DB_NAME", "manager")
