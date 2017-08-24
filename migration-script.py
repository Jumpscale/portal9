
from js9 import j


def migrate_model_data(model):
    mongo_client = j.clients.mongodb.get()
    database = mongo_client.get_database('jumpscale_system')
    user_collection = database.get_collection(model)
    user_info = user_collection.find()[0]
    for key, value in user_info.items():
        if key in ['domain', 'roles', 'xmpp', 'mobile']:
            user_collection.update_many({}, {'$unset': {key: 1}})


def main():
    migrate_model_data('user')
    migrate_model_data('group')


if __name__ == "__main__":
    main()
