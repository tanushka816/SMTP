import configparser
import os
import sys


def createConfig(path):
    """
    Create a config file
    """
    config = configparser.ConfigParser()
    config.add_section("TO")
    config.set("TO", "address1", "tanushka.vasilieva816@yandex.ru")
    config.set("TO", "address2", "qxid@yandex.ru")

    config.add_section("SUBJECT")
    config.set("SUBJECT", "subject", "today!")

    config.add_section("DATE")
    config.set("DATE", "date", "Thu Apr 28 2018 10:57:03 GMT+0500")

    config.add_section("TEXT")
    config.set("TEXT", "text", "message.txt")

    config.add_section("ATTACHMENTS")
    config.set("ATTACHMENTS", "attachment1", "or_vishe_gor.png")
    # config.set("ATTACHMENTS", "attachment2", "someDoca.doc")
    # config.set("ATTACHMENTS", "attachment3", "popyg.mp4")

    with open(path, "w") as config_file:
        config.write(config_file)


if __name__ == "__main__":
    path = "config.ini"
    createConfig(path)