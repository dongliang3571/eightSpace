$(function(){
  var navlist=["home_li", "theme_li", "store_li", "about_li", "wall_li"];
  for (i = 0; i < navlist.length; i++) {
    var newstring = "#" + navlist[i];
    $navtap = $(newstring);
    if($navtap.length > 0){
      var tapstring = "li." + navlist[i];
      $(tapstring).attr("class", "active");
    }
  }
});
