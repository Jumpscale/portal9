
def main(j, args, params, tags, tasklet):
    params.merge(args)

    import tornado.ioloop

    def stop_portal():
        ioloop = tornado.ioloop.IOLoop.current()
        ioloop.add_callback(lambda x: x.sys.exit(3), tornado.ioloop)

    stop_portal()

    params.result = ('Portal is reloaded', params.doc)

    return params


def match(j, args, params, tags, tasklet):
    return True
