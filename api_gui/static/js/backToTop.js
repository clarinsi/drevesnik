document.addEventListener("DOMContentLoaded", function () {
    /* back to top functionality */
    $("#backToTop").addClass("hidden");
    $(window).scroll(function (event) {
        var st = $(this).scrollTop();
        //console.log(st);
        if (st < 500) {
            $("#backToTop").addClass("hidden");
        } else {
            $("#backToTop").removeClass("hidden");
        }
    });
    $(document).on('click', '#backToTop', function () {
        $('html, body').animate({ scrollTop: 0 }, 500);
    });

    /** --------------------------------------------- **/
    /* top menu style adjustments based on window width */
    document.querySelector('#menu-toggler').addEventListener('click', toggleMenu);
    function toggleMenu() {
        const menu_links = document.querySelector(".menu-links");
        menu_links.classList.toggle('closed');
    }

    const mediaQuery = window.matchMedia("(max-width: 767px)");
    function mediaQueryChanges(event) {
        if (event.matches) {
            //is 767 or smaller
            document.querySelector(".menu-links").classList.add("closed");
        } else {
            document.querySelector(".menu-links").classList.remove("closed");
        }
    }

    mediaQuery.addEventListener('change', mediaQueryChanges);
    //init hide menu content
    mediaQueryChanges(mediaQuery);
});
