// Main
require([
  "requirejs",
  "jquery",
  "cookie",
  "fn",
  "foundation-datepicker",
  "ga"
], function(
  r,
  $,
  fn,
  fd
) {
  "use strict";

  $(document).ready(function() {
    $('a[href*="#"]:not([href="#"])').click(function() {
      if (
        location.pathname.replace(/^\//, "") ==
          this.pathname.replace(/^\//, "") &&
        location.hostname == this.hostname
      ) {
        var target = $(this.hash);
        target = target.length
          ? target
          : $("[name=" + this.hash.slice(1) + "]");
        if (target.length) {
          $("html, body").animate(
            {
              scrollTop: target.offset().top
            },
            500
          );
          return false;
        }
      }
    });

    $(".date-input").fdatepicker({
      closeButton: true,
      format: "yyyy-mm-dd"
    });

    $(".datetime-input").fdatepicker({
      closeButton: true,
      format: "yyyy-mm-dd hh:ii",
      pickTime: true
    });
  });
});
