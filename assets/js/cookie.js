define([
    'module',
    'jquery',
    'jscookie'
], function(module, $, cookie) {
    'use strict';

    $(document).ready(function() {
        if (!cookie.get('kdl-cookie')) {
          $("#cookie-disclaimer").removeClass('hide');
        }
        // Set cookie
        $('#cookie-disclaimer .closeme').on("click", function() {
          cookie.set('kdl-cookie', 'kdl-cookie-set', {
              expires: 30
          });
        });

        $('.closeme').bind("click", function () {
            $('#cookie-disclaimer').addClass("hide");
            return false;
        });
    });

    return module;
});
