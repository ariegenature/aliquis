from aliquis import create_app, read_config

config = read_config()
app = create_app(config)
