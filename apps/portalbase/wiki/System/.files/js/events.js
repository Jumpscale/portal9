$( function () {

PNotify.prototype.options.styling = "bootstrap3";
var cursor = sessionStorage.getItem('event.cursor') || 0;
var notifications = {};
var getevents = function() {
    $.ajax({url: '/restmachine/system/contentmanager/checkEvents',
            data: {
                cursor: cursor
            },
            success: function(data) {
                if (data) {
                    var event = data.event;
                    cursor = data.cursor;
                    sessionStorage.setItem('event.cursor', cursor);
                    if (event) {
                        event.buttons = {sticker: false};
                        if (event.refresh_hint && event.refresh_hint == location) {
                            event.hide = false;
                            event.text += "<a href='javascript:window.reloadAll()'> refresh page</a>"
                        }
                        if (event.eventstreamid && event.eventstreamid in notifications) {
                            var notify = notifications[event.eventstreamid];
                            notify.update(event);
                            notify.open(); // reopen incase it was already closed
                        } else {
                            var notify = new PNotify(event);
                        }
                        if (event.type == 'info') {
                            notifications[event.eventstreamid] = notify;
                        } else {
                            delete notifications[event.eventstreamid];
                        }
                    }
                }
                setTimeout(getevents, 0);
            },
            error: function(data) {
                console.log('Failed to call checkEvents');
                setTimeout(getevents, 3000);
            }
    });

};
setTimeout(getevents, 0);

});
