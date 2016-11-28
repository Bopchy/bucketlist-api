from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager, Shell

from bucketlist_models import Bucketlist, BucketListItem, Users
from api import create_app, db

app = create_app('development')


def make_shell_context():
    return dict(Users=Users,
                Bucketlist=Bucketlist,
                BucketListItem=BucketListItem)

# Allows us to make migrations using the db command
# Allows use to access shell as above.

manager = Manager(app)
migrate = Migrate(app, db)


manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()
