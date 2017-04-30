var opts = {
  lines: 9, // The number of lines to draw
  length: 5, // The length of each line
  width: 1, // The line thickness
  radius: 2, // The radius of the inner circle
  corners: 1, // Corner roundness (0..1)
  rotate: 21, // The rotation offset
  direction: 1, // 1: clockwise, -1: counterclockwise
  color: '#000', // #rgb or #rrggbb or array of colors
  speed: 1.8, // Rounds per second
  trail: 40, // Afterglow percentage
  shadow: false, // Whether to render a shadow
  hwaccel: false, // Whether to use hardware acceleration
  className: 'spinner', // The CSS class to assign to the spinner
  zIndex: 2e9, // The z-index (defaults to 2000000000)
  top: '50%', // Top position relative to parent
  left: '50%' // Left position relative to parent
};


var newReposURLs = $(".new-repo").parent('td').parent('tr').children().find('a')
newReposURLs.css('color', 'grey');
newReposURLs.click(function(e){e.preventDefault()});

$(".loadspace").each(function(){
    var that = $(this)
    var isNewRepo = $(this).hasClass('new-repo');
    var spacename = $(this).parent('td').parent('tr').children().find('a').text()
    $(this).css("position", "relative");
    var spinner = new Spinner(opts).spin();
    $(this).append(spinner.el)
    $.ajax({
       url:"/restmachine/system/gitlab/updateUserSpace",
       data:{"spacename":spacename},
       type:"post",
       success:function(jobid){
           var id;
           id = setInterval(function(){
              $.ajax({
                   url:"/restmachine/system/gitlab/checkUpdateUserSpaceJob",
                   data:{"jobid":jobid},
                   type:"post",
                    success:function(status){
                       if(status == "OK"){
                           clearTimeout(id)
                           spinner.stop();
                           if(isNewRepo){
                               that.parent('td').parent('tr').children().find('a').css('color', '')
                               that.parent('td').parent('tr').children().find('a').unbind('click');
                           }
                       }
                   }
              }); 
             
          }, 10000)
       }
                  });


      });



