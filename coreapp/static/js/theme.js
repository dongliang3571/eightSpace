$(function(){
  $deletebutton_theme = $("button.theme_delete");
  $strech_theme = $("div.strech");
  $deletebutton_theme.on("click", function(){
    var message_theme="";
    $buttonparent_theme = $(this).parent().parent().parent();
    $.ajax({
      type: 'DELETE',
      url: '/themes/delete_theme/' + $(this).attr("data-id"),
      success: function(data){
        $buttonparent_theme.remove();
        message_theme = "<div style=\"position:fixed;top:48px;width:100%;z-index:13;text-align:center;\" class=\"alert alert-success fade in\">" +
                  "<a href=\"#\" class=\"close\" data-dismiss=\"alert\" aria-label=\"close\">&times;</a>删除成功" + data.title  +
                  "</div>" +
                  "<script>" +
                  "window.setTimeout(function() {" +
                  "$(\"div.alert\").fadeOut(1000);" +
                  "}, 2000);" +
                  "</script>";
        $strech_theme.after(message_theme);
      },
      error: function(data){
        message_theme = "<div style=\"position:fixed;top:48px;width:100%;z-index:13;text-align:center;\" class=\"alert alert-success fade in\">" +
                  "<a href=\"#\" class=\"close\" data-dismiss=\"alert\" aria-label=\"close\">&times;</a>删除失败 " + data.title +
                  "</div>" +
                  "<script>" +
                  "window.setTimeout(function() {" +
                  "$(\"div.alert\").fadeOut(1000);" +
                  "}, 2000);" +
                  "</script>";
        $strech_theme.after(message_theme);
      },

    });
  });
});
