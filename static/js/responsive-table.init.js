!function (t) {
    "use strict";

    function e() {
    }

    e.prototype.init = function () {
        document.addEventListener("DOMContentLoaded", function () {
            t(".table-rep-plugin").responsiveTable("update"), t(".btn-toolbar [data-toggle=dropdown]").attr("data-bs-toggle", "dropdown")
        })
    }, t.ResponsiveTable = new e, t.ResponsiveTable.Constructor = e
}(window.jQuery), function () {
    "use strict";
    window.jQuery.ResponsiveTable.init()
}();