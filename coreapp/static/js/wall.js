$(function(){
  $deletebutton = $("button.delete");
  $strech = $("div.strech");
  $deletebutton.on("click", function(){
    var message ="";
    $buttonparent = $(this).parent();
    $.ajax({
      type: 'DELETE',
      url: '/wall/delete/' + $(this).attr("data-id"),
      success: function(data){
        $buttonparent.remove();
        message = "<div style=\"position:fixed;top:48px;width:100%;z-index:13;text-align:center;\" class=\"alert alert-success fade in\">" +
                  "<a href=\"#\" class=\"close\" data-dismiss=\"alert\" aria-label=\"close\">&times;</a>删除成功" + data.name + "的留言" +
                  "</div>" +
                  "<script>" +
                  "window.setTimeout(function() {" +
                  "$(\"div.alert\").fadeOut(1000);" +
                  "}, 2000);" +
                  "</script>";
        $strech.after(message);
      },
      error: function(data){
        message = "<div style=\"position:fixed;top:48px;width:100%;z-index:13;text-align:center;\" class=\"alert alert-success fade in\">" +
                  "<a href=\"#\" class=\"close\" data-dismiss=\"alert\" aria-label=\"close\">&times;</a>删除失败 " + data.name + "的留言" +
                  "</div>" +
                  "<script>" +
                  "window.setTimeout(function() {" +
                  "$(\"div.alert\").fadeOut(1000);" +
                  "}, 2000);" +
                  "</script>";
        $strech.after(message);
      },

    });
  });
});
