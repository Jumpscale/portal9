
def main(j, args, params, tags, tasklet):
    page = args.page
    import requests
    res = requests.get('https://api.ipify.org?format=json')
    ip = res.json()['ip']

    page.addJS('https://maps.google.com/maps/api/js?key=AIzaSyCIlRCymCbaIA1p1UjP7kEl-YmljPAI8ng')
    page.addJS('/jslib/ipmapper.js')
    page.addMessage("<div id='map' style='height:500px'></div>")
    page.addJS(jsContent='''
  $(function() {
    IPMapper.initializeMap("map");
    // just static ip, should be replaced from server side IP
    var ip = '%s';
    IPMapper.addIPMarker(ip);
  });
  ''' % ip, header=False)
    params.result = page

    return params
