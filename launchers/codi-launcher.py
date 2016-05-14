from flask import Flask
from codi import codi
from utils.globs import config

def register_codi_routes (app):
    app.add_url_rule('/codi/', 'api_list', codi.api_list)
    app.add_url_rule('/codi/version', 'get_version', codi.get_version)
    app.add_url_rule('/codi/list-toolchains', 'get_toolchains', codi.get_toolchains)

    app.add_url_rule('/codi/register-toolchain', 'add_toolchain', codi.add_toolchain)
    app.add_url_rule('/codi/find-image', 'find_image', codi.find_image)
    app.add_url_rule('/codi/pull-image', 'pull_image', codi.pull_image)
    app.add_url_rule('/codi/remove-image', 'remove-image', codi.remove_image)
    app.add_url_rule('/codi/remove-toolchain', 'remove_toolchain', codi.remove_toolchain)

if __name__ == '__main__':
    app = Flask(__name__)
    codi = codi.Codi(app)
    register_codi_routes(app)
    app.run(host=config.CODI_IP, port=config.CODI_PORT, debug=True)
