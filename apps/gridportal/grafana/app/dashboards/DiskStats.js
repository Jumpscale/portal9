var prefix = "stats.gauges." + ARGS.gid + "_" + ARGS.nid + "_disk_" + ARGS.name  +"_";
return {
  "title": "Disk Statistics",
  "tags": [],
  "style": "light",
  "timezone": "browser",
  "editable": false,
  "rows": [
    {
      "title": "New row",
      "height": "250px",
      "editable": false,
      "collapse": false,
      "panels": [
        {
          "span": 12,
          "editable": true,
          "type": "graph",
          "datasource": null,
          "renderer": "flot",
          "x-axis": true,
          "y-axis": true,
          "scale": 1,
          "y_formats": [
            "bytes",
            "short"
          ],
          "grid": {
            "leftMax": null,
            "rightMax": null,
            "leftMin": null,
            "rightMin": null,
            "threshold1": null,
            "threshold2": null,
            "threshold1Color": "rgba(216, 200, 27, 0.27)",
            "threshold2Color": "rgba(234, 112, 112, 0.22)"
          },
          "annotate": {
            "enable": false
          },
          "resolution": 100,
          "lines": true,
          "fill": 0,
          "linewidth": 1,
          "points": false,
          "pointradius": 5,
          "bars": false,
          "stack": false,
          "legend": {
            "show": true,
            "values": false,
            "min": false,
            "max": false,
            "current": false,
            "total": false,
            "avg": false
          },
          "percentage": false,
          "zerofill": true,
          "nullPointMode": "connected",
          "steppedLine": false,
          "tooltip": {
            "value_type": "cumulative",
            "query_as_alias": true
          },
          "targets": [
            {
              "function": "difference",
              "column": "value * 1024 / 600.",
              "series": prefix + "kbytes_read",
              "alias": "Read",
              "interval": "10m",
              "rawQuery": false
            },
            {
              "target": "",
              "function": "difference",
              "column": "value * 1024 / 600.",
              "series": prefix + "kbytes_write",
              "alias": "Write",
              "interval": "10m"
            }
          ],
          "aliasColors": {},
          "aliasYAxis": {},
          "title": "Disk Stats"
        }
      ]
    },
    {
      "title": "New row",
      "height": "250px",
      "editable": false,
      "collapse": false,
      "panels": [
        {
          "span": 12,
          "editable": true,
          "type": "graph",
          "loadingEditor": false,
          "datasource": null,
          "renderer": "flot",
          "x-axis": true,
          "y-axis": true,
          "scale": 1,
          "y_formats": [
            "bytes",
            "short"
          ],
          "grid": {
            "leftMax": null,
            "rightMax": null,
            "leftMin": 0,
            "rightMin": null,
            "threshold1": null,
            "threshold2": null,
            "threshold1Color": "rgba(216, 200, 27, 0.27)",
            "threshold2Color": "rgba(234, 112, 112, 0.22)"
          },
          "annotate": {
            "enable": false
          },
          "resolution": 100,
          "lines": true,
          "fill": 5,
          "linewidth": 1,
          "points": false,
          "pointradius": 5,
          "bars": false,
          "stack": true,
          "legend": {
            "show": true,
            "values": false,
            "min": false,
            "max": false,
            "current": false,
            "total": false,
            "avg": false
          },
          "percentage": false,
          "zerofill": true,
          "nullPointMode": "connected",
          "steppedLine": false,
          "tooltip": {
            "value_type": "cumulative",
            "query_as_alias": true
          },
          "targets": [
            {
              "function": "mean",
              "column": "value * 1024 * 1024",
              "series": prefix + "space_used_mb",
              "alias": "Used"
            },
            {
              "target": "",
              "function": "mean",
              "column": "value * 1024 * 1024",
              "series": prefix + "space_free_mb",
              "alias": "Free"
            }
          ],
          "aliasColors": {},
          "aliasYAxis": {},
          "title": "Disk Usage"
        }
      ]
    }
  ],
  "pulldowns": [
    {
      "type": "filtering",
      "enable": false
    },
    {
      "type": "annotations",
      "enable": false
    }
  ],
  "nav": [
    {
      "type": "timepicker",
      "collapse": false,
      "notice": false,
      "enable": true,
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
      "now": true
    }
  ],
  "time": {
    "from": "now-6h",
    "to": "now"
  },
  "templating": {
    "list": []
  },
  "version": 2
}
