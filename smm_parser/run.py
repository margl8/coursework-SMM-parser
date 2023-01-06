from app import create_app
from app.vk import Group

app = create_app()


@app.shell_context_processor
def make_shell_context():
    return {'VkGroup': Group}
