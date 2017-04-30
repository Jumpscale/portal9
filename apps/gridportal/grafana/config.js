define(['settings'],
function (Settings) {
  
  var serverip = $serverip;

  return new Settings({

    datasources: {
      monitoring: {
        type: 'influxdb',
        url: "http://"+ serverip  + ":8086/db/main",
        username: 'admin',
        password: 'admin',
      },
      grafana: {
        type: 'influxdb',
        url: "http://"+ serverip  + ":8086/db/grafana",
        username: 'admin',
        password: 'admin',
        grafanaDB: true
      },
    },

    search: {
      max_results: 20
    },

    default_route: '/dashboard/file/default.json',

    unsaved_changes_warning: true,

    playlist_timespan: "1m",

    admin: {
      password: ''
    },

    plugins: {
      panels: []
    }

  });
});
