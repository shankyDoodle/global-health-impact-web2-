Array.from(document.getElementsByClassName('limitations-anchor'))
    .forEach(function(elt) {
        elt.addEventListener('click', function(e) {
            document.getElementById("company-limitations").scrollIntoView({alignToTop: true})
            e.preventDefault(); // so <a> doesn't actually refresh page, but still need href which makes cursor pointer
        })