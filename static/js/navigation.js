// Change 3rd menuitem 'href' property to current page. Just for example.
$('ul li:nth-child(3) a').attr('href', window.location);

// Do the magic!
$(document).ready(function(){
  $('.navigation li a').each(function(index) {
    if(this.href.trim() == window.location) {
      $(this).addClass('selected-item');
      $(this).hover(function(){
        $(this).addClass('selected-item');
      }); 
    }
  });
});


// parlocat = 'https://s.codepen.io/boomerang/';
// curlocat = window.location.toString();
// comparelocat = window.location.toString().slice(0, parlocat.length);
// document.write('&nbsp;current url - ', curlocat, '<br>');
// document.write('&nbsp;compare url - ', comparelocat, '<br>');



 
