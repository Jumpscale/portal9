if (ARGS.nid != undefined && ARGS.nid != "$$id") {
    var prefix = "stats.gauges." + ARGS.gid + "_" + ARGS.nid + "_";
    var suffix = "";
    var alias = "";
} else {
    var prefix = "/stats.gauges." + ARGS.gid + "_\\d+_";
    var suffix = "/";
    var alias = "$2.$3";
}


return {
  "title": "Grafana",
  "tags": [],
  "style": "light",
  "timezone": "browser",
  "editable": false,
  "rows": [
    {
      "title": "CPU Information",
      "height": "250px",
      "editable": false,
      "collapse": false,
      "collapsable": true,
      "panels": [
        {
          "span": 6,
          "editable": false,
          "type": "graph",
          "x-axis": true,
          "y-axis": true,
          "scale": 1,
          "y_formats": [
            "short",
            "short"
          ],
          "grid": {
            "max": null,
            "min": null,
            "leftMax": null,
            "rightMax": null,
            "leftMin": null,
            "rightMin": null,
            "threshold1": null,
            "threshold2": null,
            "threshold1Color": "rgba(216, 200, 27, 0.27)",
            "threshold2Color": "rgba(234, 112, 112, 0.22)"
          },
          "resolution": 100,
          "lines": true,
          "fill": 1,
          "linewidth": 2,
          "points": false,
          "pointradius": 5,
          "bars": false,
          "stack": true,
          "spyable": true,
          "options": false,
          "legend": {
            "show": true,
            "values": false,
            "min": false,
            "max": false,
            "current": false,
            "total": false,
            "avg": false
          },
          "interactive": true,
          "legend_counts": true,
          "timezone": "browser",
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
              "series": prefix + "cpu.promile" + suffix,
              "column": "value / 10.0",
              "query": "",
              "alias": alias || "CPU",
              "interval": "1m"
            }
          ],
          "aliasColors": {},
          "aliasYAxis": {},
          "title": "CPU Percent",
          "datasource": null,
          "renderer": "flot",
          "annotate": {
            "enable": false
          }
        },
        {
          "span": 6,
          "editable": false,
          "type": "graph",
          "datasource": null,
          "renderer": "flot",
          "x-axis": true,
          "y-axis": true,
          "scale": 1,
          "y_formats": [
            "short",
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
          "fill": 0,
          "linewidth": 2,
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
              "function": "mean",
              "series": prefix + "load.avg1min" + suffix,
              "column": "value / 100.",
              "alias": alias || "Avg 1 Min",
              "hide": false,
              "interval": "1m"
            },
            {
              "function": "mean",
              "series": prefix + "load.avg5min" + suffix,
              "column": "value / 100.",
              "alias": alias || "Avg 5 min",
              "interval": "1m"
            },
            {
              "function": "mean",
              "series": prefix + "load.avg15min" + suffix,
              "column": "value / 100.",
              "alias": alias || "Avg 15 min",
              "interval": "1m"
            }
          ],
          "aliasColors": {},
          "aliasYAxis": {},
          "title": "System Load",
          "leftYAxisLabel": ""
        }
      ],
      "notice": false
    },
    {
      "title": "Memory Information",
      "height": "250px",
      "editable": false,
      "collapse": false,
      "panels": [
        {
          "span": 6,
          "editable": false,
          "type": "graph",
          "datasource": null,
          "renderer": "flot",
          "x-axis": true,
          "y-axis": true,
          "scale": 1,
          "y_formats": [
            "none",
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
            "threshold2Color": "rgba(234, 112, 112, 0.22)",
            "thresholdLine": false
          },
          "annotate": {
            "enable": false
          },
          "resolution": 100,
          "lines": true,
          "fill": 100,
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
            "avg": false,
            "alignAsTable": false
          },
          "percentage": true,
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
              "series": prefix + "cpu.time.system" + suffix,
              "column": "value",
              "alias": alias || "System",
              "interval": "1m"
            },
            {
              "function": "mean",
              "series": prefix + "cpu.time.user" + suffix,
              "column": "value",
              "alias": alias || "User",
              "interval": "1m"
            },
            {
              "function": "mean",
              "series": prefix + "cpu.time.idle" + suffix,
              "column": "value",
              "alias": alias || "Idle",
              "interval": "1m"
            },
            {
              "function": "mean",
              "series": prefix + "cpu.time.iowait" + suffix,
              "column": "value",
              "alias": alias || "IO Wait",
              "interval": "1m"
            }
          ],
          "aliasColors": {},
          "aliasYAxis": {},
          "title": "CPU Time"
        },
        {
          "span": 6,
          "editable": false,
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
          "fill": 3,
          "linewidth": 2,
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
              "series": prefix + "memory.used" + suffix,
              "column": "value *1024 * 1024",
              "alias": alias || "Used",
              "interval": "1m"
            },
            {
              "function": "mean",
              "series": prefix + "memory.cached" + suffix,
              "column": "value *1024 * 1024",
              "alias": alias || "Cached",
              "interval": "1m"
            },
            {
              "function": "mean",
              "series": prefix + "memory.free" + suffix,
              "column": "value * 1024 * 1024",
              "alias": alias || "Free",
              "hide": false,
              "interval": "1m"
            }
          ],
          "aliasColors": {},
          "aliasYAxis": {},
          "title": "Memory",
          "leftYAxisLabel": ""
        }
      ]
    },
    {
      "title": "Network Information",
      "height": "250px",
      "editable": false,
      "collapse": false,
      "panels": [
        {
          "span": 6,
          "editable": false,
          "type": "graph",
          "datasource": null,
          "renderer": "flot",
          "x-axis": true,
          "y-axis": true,
          "scale": 1,
          "y_formats": [
            "bytes",
            "bytes"
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
              "series": prefix + "network.kbytes.recv" + suffix,
              "column": "value * 1024",
              "interval": "2m",
              "alias": alias || "Received"
            },
            {
              "function": "difference",
              "series": prefix + "network.kbytes.send" + suffix,
              "column": "value * 1024",
              "interval": "2m",
              "alias": alias || "Sent"
            }
          ],
          "aliasColors": {},
          "aliasYAxis": {},
          "title": "Network Bandwith"
        },
        {
          "span": 6,
          "editable": false,
          "type": "graph",
          "datasource": null,
          "renderer": "flot",
          "x-axis": true,
          "y-axis": true,
          "scale": 1,
          "y_formats": [
            "short",
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
              "series": prefix + "network.error.in" + suffix,
              "column": "value",
              "interval": "2m",
              "alias": alias || "In"
            },
            {
              "function": "difference",
              "series": prefix + "network.error.out" + suffix,
              "column": "value",
              "interval": "2m",
              "alias": alias || "Out"
            }
          ],
          "aliasColors": {},
          "aliasYAxis": {},
          "title": "Network Error"
        }
      ]
    }
  ],
  "pulldowns": [
    {
      "type": "filtering",
      "collapse": false,
      "notice": false,
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
    "from": "now-1h",
    "to": "now"
  },
  "templating": {
    "list": []
  },
  "version": 2
}

