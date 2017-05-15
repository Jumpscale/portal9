from js9 import j
from JumpScale9Portal.PortalBase import *


class PortalRootClassFactory:

    portal_instance = None

    def __init__(self):
        self.__jslocation__ = "j.portal.tools"
        self.logger = j.logger.get("j.portal.tools")
        self._codegentools = None
        self._specparser = None
        self._models = None
        self._datatables = None
        self._defmanager = None
        self._docgenerator = None
        self._macrohelper = None
        self._portalloaders = None
        self._infomgr = None
        self._html = None
        self._docpreprocessor = None
        self._swaggerGen = None
        self._taskletengine = None
        self._server = None
        # self._portal = None


    @property
    def codegentools(self):
        from JumpScale9Portal.tools.codegentools.codegentools import codegentools
        if self._codegentools is None:
            self._codegentools = codegentools()
        return self._codegentools

    @property
    def specparser(self):
        from JumpScale9Portal.tools.specparser.specparser import specparser
        if self._specparser is None:
            self._specparser = specparser()
        return self._specparser

    @property
    def models(self):
        from JumpScale9Portal.data.models.models import models
        if self._models is None:
            self._models = models()
        return self._models

    @property
    def datatables(self):
        from JumpScale9Portal.portal.datatables.datatables import datatables
        if self._datatables is None:
            self._datatables = datatables()
        return self._datatables

    @property
    def defmanager(self):
        from JumpScale9Portal.portal.defmanager.defmanager import defmanager
        if self._defmanager is None:
            self._defmanager = defmanager()
        return self._defmanager

    @property
    def docgenerator(self):
        from JumpScale9Portal.portal.docgenerator.docgenerator import docgenerator
        if self._docgenerator is None:
            self._docgenerator = docgenerator()
        return self._docgenerator

    @property
    def macrohelper(self):
        from JumpScale9Portal.portal.macrohelper.macrohelper import macrohelper
        if self._macrohelper is None:
            self._macrohelper = macrohelper()
        return self._macrohelper

    @property
    def portalloaders(self):
        from JumpScale9Portal.portal.portalloaders.portalloaders import portalloaders
        if self._portalloaders is None:
            self._portalloaders = portalloaders()
        return self._portalloaders

    @property
    def infomgr(self):
        from JumpScale9Portal.portal.infomgr.infomgr import infomgr
        if self._infomgr is None:
            self._infomgr = infomgr()
        return self._infomgr

    @property
    def html(self):
        from JumpScale9Portal.portal.html.html import html
        if self._html is None:
            self._html = html()
        return self._html

    @property
    def docpreprocessor(self):
        from JumpScale9Portal.portal.docpreprocessor.docpreprocessor import docpreprocessor
        if self._docpreprocessor is None:
            self._docpreprocessor = docpreprocessor()
        return self._docpreprocessor

    @property
    def swaggergen(self):
        from JumpScale9Portal.tools.swaggergen.swaggergenswaggergen import swaggergen
        if self._swaggergen is None:
            self._swaggergen = swaggergen()
        return self._swaggergen

    @property
    def taskletengine(self):
        from JumpScale9Portal.tools.taskletengine.taskletengine import taskletengine
        if self._taskletengine is None:
            self._taskletengine = taskletengine()
        return self._taskletengine
    
    @property
    def server(self):
        from JumpScale9Portal.portal.PortalServerFactory import PortalServerFactory
        if self._server is None:
            self._server = PortalServerFactory()
        return self._server

    # @property
    # def server(self):
    #     from JumpScale9Portal.portal.server import server
    #     if self._server is None:
    #         self._server = server()
    #     return self._server

    def _getBaseClass(self):
        return PortalBase

    def _getBaseClassLoader(self):
        return PortalBaseLoader
