from js9 import j


class ActorsInfo():

    def getActorMethodCall(self, appname, actor, method):
        """
        used for during error show links to methods in browser
        """
        url = "/rest/%s/%s/%s?" % (appname, actor, method)

        auth = j.portal.server.active.ws.routes["%s_%s_%s" % (appname, actor, method)]['auth']
        if auth:
            params = ["authkey"]
        else:
            params = []
        params.extend(list(j.portal.server.active.ws.routes["%s_%s_%s" % (appname, actor, method)]['params'].keys()))

        for param in params:
            url += "%s=&" % param
        url += "format=text"
        if url[-1] == "&":
            url = url[:-1]
        if url[-1] == "?":
            url = url[:-1]
        # url="<a href=\"%s\">%s</a> " % (url,url)
        return url

    def getActorInfoPage(self, appname, actorname, methodname, page=None):
        """
        used for during error show info about 1 actor
        """
        if appname == "" or actorname == "" or methodname == "":
            txt = "getActorInfo need 3 params: appname, actorname, methoname, got: %s, %s,%s" % (
                appname, actorname, methodname)
            return txt
        if page is None:
            page = j.portal.server.active.pageprocessor.getpage()
        page.addHeading("%s.%s.%s" % (appname, actorname, methodname), 5)

        url = getActorMethodCall(appname, actorname, methodname)

        routekey = "%s_%s_%s" % (appname, actorname, methodname)
        if routekey not in j.portal.server.active.routes:
            j.portal.server.active.activateActor(appname, actorname)
        routeData = j.portal.server.active.routes[routekey]
        # routedata: function,paramvalidation,paramdescription,paramoptional,description

        description = routeData[4]
        if description.strip() != "":
            page.addMessage(description)
        # param info
        params = routeData[1]
        descriptions = routeData[2]
        # optional = routeData[3]
        page.addLink("%s" % (methodname), url)
        if len(list(params.keys())) > 0:
            page.addBullet("Params:\n", 1)
            for key in list(params.keys()):
                if key in descriptions:
                    descr = descriptions[key].strip()
                else:
                    descr = ""
                page.addBullet("- %s : %s \n" % (key, descr), 2)

        return page

    def getActorsInfoPage(appname="", actor="", page=None, extraParams={}):
        actorsloader = j.portal.server.active.actorsloader
        if appname != "" and actor != "":
            result = j.portal.server.active.activateActor(appname, actor)
            if result is False:
                # actor was not there
                page = j.portal.server.active.pageprocessor.getpage()
                page.addHeading("Could not find actor %s %s." % (appname, actor), 4)
                return page

        if page is None:
            page = j.portal.server.active.pageprocessor.getpage()
        if appname == "":
            page.addHeading("Applications in appserver.", 4)
            appnames = {}

            # [item.split("_", 1) for  item in self.app_actor_dict.keys()]:
            for appname, actorname in actorsloader.getAppActors():
                appnames[appname] = 1
            appnames = sorted(appnames.keys())
            for appname in appnames:
                link = page.getLink("%s" % (appname), getActorInfoUrl(appname, ""))
                page.addBullet(link)
            return page

        if actor == "":
            page.addHeading("Actors for application %s" % (appname), 4)
            actornames = []
            # [item.split("_", 1) for  item in self.app_actor_dict.keys()]:
            for appname2, actorname2 in actorsloader.getAppActors():
                if appname2 == appname:
                    actornames.append(actorname2)
            actornames.sort()

            for actorname in actornames:
                link = page.getLink("%s" % (actorname), getActorInfoUrl(appname, actorname))
                page.addBullet(link)
            return page

        keys = sorted(j.portal.server.active.routes.keys())
        page.addHeading("list", 2)
        for item in keys:
            app2, actor2, method = item.split("_")
            if app2 == appname and actor2 == actor:
                url = getActorMethodCall(appname, actor, method)
                link = page.getLink(item, url)
                page.addBullet(link)

        page.addHeading("details", 2)
        for item in keys:
            app2, actor2, method = item.split("_")
            if app2 == appname and actor2 == actor:
                page = getActorInfoPage(appname, actor, method, page=page)
