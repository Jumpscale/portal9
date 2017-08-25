
from js9 import j


def migrate_model_data(model):
    mongo_client = j.clients.mongodb.get()
    database = mongo_client.get_database('jumpscale_system')
    user_collection = database.get_collection(model)
    keys = {'domain': 1, 'roles': 1, 'xmpp': 1, 'mobile': 1}
    user_collection.update_many({}, {'$unset': keys})


def main():
    migrate_model_data('user')
    migrate_model_data('group')


if __name__ == "__main__":
    main()
