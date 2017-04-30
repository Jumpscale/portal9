function adminLoadingShow() {
    var loadingMsg = $('<div class="loadingMsg alert alert-info">Loading...</div>').appendTo('body')
        .css('position', 'absolute')
        .css('top', '50px');
    loadingMsg.css('left', ($(window).width() - loadingMsg.width())/2 + 'px');
}

function adminLoadingHide() {
    $('.loadingMsg').remove();
}

function pullUpdate(spaceName) {
    adminLoadingShow();
    $.ajax({'url': '/system/PullUpdate?space=' + spaceName}).done(function() {
        reloadAll();
    });
}

// Restarts the portal
function reloadAll() {
    // A request to this URL will restart the portal, so this URL will give us "503 Service Unavailable"
    // Later, I poll the server to see if it's up again
    adminLoadingShow();
    $.ajax({'url': '/system/ReloadApplication'});

    function checkPortalIsUp(trials) {
        if (trials <= 0) {
            alert('Maximum trials reached & the server is not up!');
            return;
        }
        setTimeout(function() {
            $.ajax({'url': '/system/'}).done(function(){
                location.reload();
                console.log('Reloaded');
            }).error(function(){
                checkPortalIsUp(trials - 1);
            });
        }, 1000);
    };
    checkPortalIsUp(10);
};