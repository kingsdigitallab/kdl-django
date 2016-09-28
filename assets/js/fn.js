define([
    'module',
    'jquery',
    // 'es6!foundation',
    // 'es6!foundation.accordionMenu',
    // 'es6!foundation.drilldown',
    // 'es6!foundation.dropdown',
    // 'es6!foundation.dropdownMenu',
    // 'es6!foundation.equalizer',
    // 'es6!foundation.responsiveMenu',
    // 'es6!foundation.responsiveToggle',
    // 'es6!foundation.sticky',
    // 'es6!foundation.util.box',
    // 'es6!foundation.util.keyboard',
    // 'es6!foundation.util.mediaQuery',
    // 'es6!foundation.util.motion',
    // 'es6!foundation.util.nest',
    // 'es6!foundation.util.timerAndImageLoader',
    // 'es6!foundation.util.touch',
    // 'es6!foundation.util.triggers'
    'foundation',
    'foundation.accordionMenu',
    'foundation.drilldown',
    'foundation.dropdown',
    'foundation.dropdownMenu',
    'foundation.equalizer',
    'foundation.responsiveMenu',
    'foundation.responsiveToggle',
    'foundation.sticky',
    'foundation.util.box',
    'foundation.util.keyboard',
    'foundation.util.mediaQuery',
    'foundation.util.motion',
    'foundation.util.nest',
    'foundation.util.timerAndImageLoader',
    'foundation.util.touch',
    'foundation.util.triggers'
], function(module, $) {
    'use strict';

    $(document).ready(function() {
        // loads foundation
        $(document).foundation();
    });

    return module;
});
