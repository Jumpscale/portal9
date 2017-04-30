def main(j, args, params, tags, tasklet):
    page = args.page
    graphdata = args.cmdstr.format(**args.doc.appliedparams)
    checksum = j.data.hash.md5_string(graphdata)
    graphdata = j.data.hrd.get(content=graphdata)

    targets = graphdata.getDictFromPrefix('target')
    cfg = {'stack': False, 'fill': '1', 'percentage': False, "y_format": 'short', 'checksum': checksum}
    cfg.update(graphdata.getDictFromPrefix('cfg'))
    if 'dashboardtitle' not in cfg:
        cfg['dashboardtitle'] = checksum

    targetsstr = ''
    grafanatargets = []

    for target in targets.values():
        target['value'] = target.get('value', 'value')
        targetvalue = {
                            "fields": [
                                {
                                    "func": target['function'],
                                    "name": target['value']
                                }
                            ],
                            "measurement": target['series'],
                            "alias": target['alias'],
                            "interval": target['interval']
                        }
        grafanatargets.append(targetvalue)
    cfg['target'] = targetsstr.strip(',')

    dashboard = {
    "title": cfg['dashboardtitle'],
    "tags": [],
    "style": "light",
    "timezone": "browser",
    "editable": False,
    "rows": [
        {
            "title": cfg['title'],
            "height": "250px",
            "editable": False,
            "collapse": False,
            "collapsable": True,
            "panels": [
                {
                    "editable": False,
                    "type": "graph",
                    "x-axis": True,
                    "y-axis": True,
                    "scale": 1,
                    "y_formats": [
                        cfg['y_format'],
                        cfg['y_format'],
                    ],
                    "grid": {
                        "max": None,
                        "min": None,
                        "leftMax": None,
                        "rightMax": None,
                        "leftMin": None,
                        "rightMin": None,
                        "threshold1": None,
                        "threshold2": None,
                        "threshold1Color": "rgba(216,200,27,0.27)",
                        "threshold2Color": "rgba(234,112,112,0.22)"
                    },
                    "lines": True,
                    "fill": cfg['fill'],
                    "linewidth": 2,
                    "points": False,
                    "pointradius": 5,
                    "bars": False,
                    "stack": cfg['stack'],
                    "spyable": True,
                    "options": False,
                    "legend": {
                        "show": True,
                        "values": False,
                        "min": False,
                        "max": False,
                        "current": False,
                        "total": False,
                        "avg": False
                    },
                    "interactive": True,
                    "legend_counts": True,
                    "timezone": "browser",
                    "percentage": cfg['percentage'],
                    "zerofill": True,
                    "nullPointMode": "connected",
                    "steppedLine": False,
                    "tooltip": {
                        "value_type": "cumulative",
                        "query_as_alias": True
                    },
                    "targets": grafanatargets,
                    "aliasColors": {},
                    "aliasYAxis": {},
                    "title": cfg['title'],
                    "datasource": "influxdb_main",
                    "renderer": "flot",
                    "annotate": {
                        "enable": False
                    }
                }
            ],
            "notice": False
        }
    ],
    "pulldowns": [
        {
            "type": "filtering",
            "collapse": False,
            "notice": False,
            "enable": False
        },
        {
            "type": "annotations",
            "enable": False
        }
    ],
    "nav": [
        {
            "type": "timepicker",
            "collapse": False,
            "notice": False,
            "enable": True,
            "status": "Stable",
            "time_options": [
                "5m",
                "15m",
                "1h",
                "6h",
                "12h",
                "24h",
                "2d",
                "7d",
                "30d"
            ],
            "refresh_intervals": [
                "5s",
                "10s",
                "30s",
                "1m",
                "5m",
                "15m",
                "30m",
                "1h",
                "2h",
                "1d"
            ],
            "now": True
        }
    ],
    "time": {
        "from": "now-1h",
        "to": "now"
    },
    "templating": {
        "list": []
    },
    "version": 2
}

    grafclient = j.clients.grafana.getByInstance()
    result = grafclient.updateDashboard(dashboard)
    cfg['slug'] = result['slug']
    page.addHTML("""
        <iframe width="%(width)s" height="%(height)s" src="/grafana/dashboard-solo/db/%(slug)s?panelId=1&fullscreen&theme=light" frameborder="0"></iframe>""" % cfg)
    params.result = page
    return params


def match(j, args, params, tags, tasklet):
    return True
