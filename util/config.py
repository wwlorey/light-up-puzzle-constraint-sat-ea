import configparser


class Config:
    def __init__(self, config_file):
        """Initializes the Config class.

        This class assumes CFG format for data in config_file.
        """
        self.settings = configparser.ConfigParser()
        self.settings.read(config_file)

        # Remove the reference to the DEFAULT section for ease of use
        # (i.e. direct access of config settings from self.settings)
        self.settings = self.settings['DEFAULT'] 
