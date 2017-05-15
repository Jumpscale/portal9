from js9 import j
from .actorgen import actorGen
import jinja2
import urllib.parse

# Datastructure use in the templates
# this is a really simple subset of the swagger spec
# the types are there just to help when doing the buisness logic implementation
# {
#     "port" : 80, // port the server listen on
#     "handlers" :[//list of handlers
#         { //handler definition
#             "name":"",
#             "path":"",
#             "methods": [ //list of methods for this path
#                 { // method definition
#                     "type" : "", // should be a HTTP verb, get,post,put,...
#                     "summary" : "", // optional description of the method
#                     "params":{ //parameters of this method definition
#                         "body":{
#                           "required":true, //boolean
#                           "isArray": false,
#                           "schema": {
#                                "id": {
#                                    "type": "integer",
#                                    "isArray: False"
#                                },
#                                "name": {
#                                    "type": "string",
#                                    "isArray: False"
#                                },
#                           }
#                        }, // object description of the content of the body
#                        "query":[ //list of query parameters
#                             {
#                                 "required":true, //boolean
#                                 "name" : "", // string
#                                 "type" : "", // string
#                                 "isArray": false
#                             }
#                        ],
#                        "form":[ //list of form parameters
#                             {
#                                 "required":true, //boolean
#                                 "name" : "", // string
#                                 "type" : "", // string
#                                 "isArray": false
#                             }
#                        ],
#                        "header":[ //list of header parameters
#                             {
#                                 "required":true, //boolean
#                                 "name" : "", // string
#                                 "type" : "", // string
#                                 "isArray": false
#                             }
#                        ],
#                        "path":[ //list of path parameters
#                             {
#                                 "required":true, //boolean
#                                 "name" : "", // string
#                                 "type" : "" ,// string
#                                 "isArray": false
#                             }
#                         ]
#                     }
#                 }
#             ],
#         }
#     ]
# }


class SwaggerGen:

    def __init__(self):
        tmplDir = j.sal.fs.joinPaths(j.sal.fs.getDirName(__file__), 'templates')
        self.jinjaEnv = jinja2.Environment(
            loader=jinja2.FileSystemLoader(tmplDir),
            trim_blocks=True,
            lstrip_blocks=True
        )
        self.spec = None
        self._definitions = {}
        self._globalParams = {}
        self.server = {
            'requires': [],
            'baseURL': '',
            'port': 80,
            'handlers': []
        }
        # spore spec for client generation
        self.client = {}

    def loadSpecFromStr(self, spec):
        self.spec = j.data.serializer.json.loads(spec)

    def loadSpecFromFile(self, path):
        content = j.sal.fs.fileGetContents(path)
        self.loadSpecFromStr(content)

    def generate(self, baseURL, serverOuput, clientOutput):
        self.server['baseURL'] = baseURL
        self.generateServer(serverOuput)
        self.generateClient(clientOutput)

    def generateServer(self, outputPath):
        self.server['port'] = self._extractPort(self.spec)
        self.server['handlers'] = self._generateHandlers(self.spec)
        server = self._renderServer(self.server)
        j.sal.fs.writeFile(outputPath, server.strip())

    def generateactors(self, destpath):
        actorGen(self).generate(destpath)

    def generateClient(self, outputPath):
        if len(self.server['handlers']) == 0:
            self._generateHandlers(self.spec)
        self._generateSporeSpec(outputPath)

    def _generateSporeSpec(self, outputPath):
        self.client = {
            'name': 'JSLuaSpore',
            'base_url': self.server['baseURL']
        }
        self.client['methods'] = self._clientMethods(self.server['handlers'])
        j.sal.fs.writeFile(outputPath, j.data.serializer.json.dumps(self.client, indent=4))
        return self.client

    def _clientMethods(self, handlers):
        methods = {}
        for h in handlers:
            for method in h['methods']:
                sporeMethod = {
                    'path': self._clientPath(h['path'], method['params']),
                    'method': method['type'].upper(),
                    'optional_params': self._clientParams(method['params'], required=False),
                    'required_params': self._clientParams(method['params'], required=True)
                }
                name = h['name'] + "_" + method['type']
            methods[name] = sporeMethod
        return methods

    def _clientPath(self, path, params):
        path = path.replace('/(.*)', '')
        if 'query' in params:
            for p in params['path']:
                path += '/' + ':' + p['name']
        return path

    def _clientParams(self, params, required):
        output = []
        for t in list(params.keys()):
            if t == 'body':
                pass
            else:
                for p in params[t]:
                    if p['required'] == required:
                        output.append(p['name'])
        return output

    def _extractPort(self, spec):
        url = {}
        if 'host' in spec:
            url = urllib.parse.urlparse(spec['host'])
            return url.port() if url.port is not None else 80
        else:
            return 80

    def _generateHandlers(self, spec):
        handlers = []
        if 'definitions' in spec:
            self._generateDefinitions(spec['definitions'])
        paths = self._generatePaths(spec['paths'])
        return paths

    def _generatePaths(self, specPaths):
        def formatPath(s):
            while True:
                start, end = s.find('{'), s.find('}')
                if start == -1 or end == -1:
                    if 'basePath' in self.spec:
                        return (self.spec['basePath'] + s).lower()
                    else:
                        return s.lower()
                else:
                    s = s[:start] + "(.*)" + s[end + 1:]

        def formatName(s):
            return s.replace('/', '').replace('{', '').replace("}", "").replace('-', '_')
        paths = []
        for path, methods in specPaths.items():
            p = {}
            p['name'] = formatName(path)
            p['path'] = formatPath(str(path))
            p['methods'] = self._generateMethods(methods)
            paths.append(p)
        # sort from precise to generic path, needed for lua router
        paths = sorted(paths, key=lambda path: path['path'], reverse=True)
        return paths

    def _generateMethods(self, specMethods):
        methods = []
        for httpVerb, detail in specMethods.items():
            m = {
                'params': {},
                'responses': [],
                'summary': "",
                'type': httpVerb
            }
            if 'parameters' in detail:
                m['params'] = self._generateParams(detail['parameters'])
            if 'responses' in detail:
                m['responses'] = self._generateResponses(detail['responses'])
            if 'summary' in detail:
                m['summary'] = detail['summary']
            methods.append(m)
        return methods

    def _generateParams(self, specParams):
        params = {
            'body': {},
            'query': [],
            'path': [],
            'header': [],
            'formData': []
        }
        for p in specParams:
            location, param = self._processParams(p)
            if location == 'body':
                # from IPython import embed;embed()
                params[location] = param
            else:
                params[location].append(param)
        return params

    def _processParams(self, specParams):
        if '$ref' in specParams:
            ss = specParams['$ref'].split("/")
            _processParams(self._globalParams[ss[2]])
        else:
            location = specParams['in']
            if location == 'body':
                return self._processBodyParam(specParams)
            elif location == 'array':
                return self._processArrayParam(specParams)
            else:
                p = {
                    "required": False if 'required' not in specParams else specParams['required'],
                    "name": specParams['name'],
                    "type": specParams['type'],
                    "isArray": False
                }
            return location, p

    def _processBodyParam(self, bodyParam):
        # from IPython import embed;embed()
        location = bodyParam['in']
        if 'schema' in bodyParam:
            # import ipdb;
            if 'items' in bodyParam['schema']:
                schema = bodyParam['schema']['items']
            else:
                schema = bodyParam['schema']
        if '$ref' in schema:
            ss = schema['$ref'].split("/")
            schema = self._definitions[ss[2]]
        p = {
            "required": bodyParam['required'],
            "isArray": False,
            "schema": schema
        }
        return location, p

    def _processArrayParam(self, arrayParam):
        location = arrayParam['in']
        param = arrayParam['items']
        if '$ref' in arrayParam['items']:
            ss = param['$ref'].split("/")
            param = self._definitions[ss[2]]
        p = {
            "required": False if 'required' not in arrayParam['items'] else arrayParam['required'],
            "name": arrayParam['name'],
            "type": param['type'],
            "isArray": True
        }
        return location, p

    def _generateResponses(self, specReponses):
        responses = []
        for code, detail in specReponses.items():
            r = {}
            r['code'] = code
            r['description'] = detail['description']
            if 'examples' in detail:
                r['examples'] = detail['examples']
            if 'headers' in detail:
                r['headers'] = detail['headers']
            if 'schema' in detail:
                if '$ref' in detail['schema']:
                    ss = detail['schema']['$ref'].split("/")
                    r['schema'] = self._definitions[ss[2]]
                else:
                    r['schema'] = detail['schema']
            responses.append(r)
        return responses

    def _generateDefinitions(self, specDefinitions):
        refs = []  # keeps the refs that need to be linked when all definitions are loaded
        for name, detail in specDefinitions.items():
            self._definitions[name] = detail
            if 'properties' in detail:
                for propName, propDetail in detail['properties'].items():
                    if '$ref' in propDetail:
                        ss = propDetail['$ref'].split('/')
                        r = {
                            'defName': name,
                            'propName': propName,
                            'ref': ss[2],
                            'isArray': False
                        }
                        refs.append(r)
                    elif 'type' in propDetail and propDetail['type'] == 'array' and '$ref' in propDetail['items']:
                        ss = propDetail['items']['$ref'].split('/')
                        r = {
                            'defName': name,
                            'propName': propName,
                            'ref': ss[2],
                            'isArray': True
                        }
                        refs.append(r)
        for r in refs:
            if r['isArray']:
                self._definitions[r['defName']]['properties'][r['propName']]['items'] = self._definitions[r['ref']]
            else:
                self._definitions[r['defName']]['properties'][r['propName']] = self._definitions[r['ref']]

    def _renderServer(self, serverSpec):
        output = ""
        output += self._renderRequire()
        output += self._renderHandlers(serverSpec['handlers'])
        output += self._renderApplication(serverSpec['handlers'])
        return output

    def _renderRequire(self):
        self.server['requires'].append('turbo')

        tmpl = self.jinjaEnv.get_template('require.tmpl')
        output = tmpl.render(requires=self.server['requires'])
        return output

    def _renderHandlers(self, handlers):
        tmpl = self.jinjaEnv.get_template('handler.tmpl')
        output = ""
        for h in handlers:
            r = tmpl.render(handler=h)
            output += r
        return output

    def _renderApplication(self, handlers):
        tmpl = self.jinjaEnv.get_template('application.tmpl')
        output = tmpl.render(handlers=handlers, port=8080)
        return output


if __name__ == '__main__':
    gen = SwaggerGen()
    gen.loadSpecFromFile("tests/spec2.json")
    gen.generate('http://localhost:8080', 'server.lua', 'client.json')
