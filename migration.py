from app import app, engine
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

migrate = Migrate(app, engine)

manager = Manager(app)
manager.add_command("engine", MigrateCommand)

if __name__ == '__main__':
    manager.run()
