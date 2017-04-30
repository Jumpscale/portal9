from js9 import j

# import re
import os
# import jinja2

from watchdog.events import FileSystemEventHandler
# The default Observer on Linux (InotifyObserver) hangs in the call to `observer.schedule` because the observer uses `threading.Lock`, which is
# monkeypatched by `gevent`. To work around this, I use `PollingObserver`. It's more CPU consuming than `InotifyObserver`, but still better than
# reloading the doc processor
#
#from watchdog.observers import Observer
from watchdog.observers.polling import PollingObserver as Observer


class DocHandler(FileSystemEventHandler):

    def __init__(self, doc_processor):
        self.doc_processor = doc_processor

    def on_created(self, event):
        print(('Document {} added'.format(event.src_path)))
        path = os.path.dirname(event.src_path)
        pathItem = event.src_path
        docs = []
        if pathItem:
            lastDefaultPath = ""
            if pathItem.endswith('.wiki'):
                lastDefaultPath = os.path.join(self.doc_processor.space_path, '.space', 'default.wiki')
            elif pathItem.endswith('.md'):
                lastDefaultPath = os.path.join(self.doc_processor.space_path, '.space', 'default.md')
            elif pathItem.endswith('.py'):
                self.reloadMacro(event)
            self.doc_processor.add_doc(pathItem, path, docs=docs, lastDefaultPath=lastDefaultPath)
            self.doc_processor.docs[-1].loadFromDisk()
            self.doc_processor.docs[-1].preprocess()

    def on_modified(self, event):
        if event.src_path and not event.is_directory and event.src_path.endswith(".py"):
            self.reloadMacro(event)

    def reloadMacro(self, event):
        for macroexecute in (self.doc_processor.macroexecutorPreprocessor,
                             self.doc_processor.macroexecutorWiki, self.doc_processor.macroexecutorPage):
            for groupname, taskletenginegroup in list(macroexecute.taskletsgroup.items()):
                for group, taskletengine in list(taskletenginegroup.taskletEngines.items()):
                    for tasklet in taskletengine.tasklets:
                        if tasklet.path == event.src_path:
                            taskletengine.reloadTasklet(tasklet)
                            return

    on_moved = on_created
