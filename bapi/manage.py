from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager, Shell

from bucketlist_models import Bucketlist, BucketListItem, Users
from bapi import app, db
from config import config

app.config.from_object(config['development'])


def make_shell_context():
    """ Allows for migrations using the db command
    Also allows for access shell as above.
    """
    return dict(Users=Users,
                Bucketlist=Bucketlist,
                BucketListItem=BucketListItem)


manager = Manager(app)
migrate = Migrate(app, db)


manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()
