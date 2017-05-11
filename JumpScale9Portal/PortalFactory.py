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

    def _getBaseClass(self):
        return PortalBase

    def _getBaseClassLoader(self):
        return PortalBaseLoader
