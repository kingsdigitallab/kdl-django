// Main
require([
    'requirejs',
    'jquery',
    'fn',
    'ga'
    // 'object-fit-images'
], function(r, $) {
    'use strict';

    $(document).ready(function() {

        // Smooth scrolling
    	$(function() {
		  $('a[href*="#"]:not([href="#"])').click(function() {
		    if (location.pathname.replace(/^\//,'') == this.pathname.replace(/^\//,'') && location.hostname == this.hostname) {
		      var target = $(this.hash);
		      target = target.length ? target : $('[name=' + this.hash.slice(1) +']');
		      if (target.length) {
		        $('html, body').animate({
		          scrollTop: target.offset().top
		        }, 500);
		        return false;
		      }
		    }
		  });
		});

        // object-fit-images - polyfill for IE/Edge
        // $(function () {
        //     objectFitImages();
        // });
    });

});
