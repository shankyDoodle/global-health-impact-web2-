function cont2010() {
    document.getElementById('cont2010').style.display = 'block';
    document.getElementById('cont2013').style.display = 'none';
    document.getElementById('cont2015').style.display = 'none';
}
function cont2013() {
    document.getElementById('cont2013').style.display = 'block';
    document.getElementById('cont2010').style.display = 'none';
    document.getElementById('cont2015').style.display = 'none';
}
function cont2015() {
    document.getElementById('cont2015').style.display = 'block';
    document.getElementById('cont2010').style.display = 'none';
    document.getElementById('cont2013').style.display = 'none';
}
function yearclick(showthis,hidethis) {
    document.getElementById(hidethis).style.display = 'none';
    document.getElementById(showthis).style.display = 'block';
}
function new_yearclick(showthis,hidethis, hidethisonealso) {
    document.getElementById(hidethisonealso).style.display = 'none';
    document.getElementById(hidethis).style.display = 'none';
    document.getElementById(showthis).style.display = 'block';
}


function dropNav() {
    document.getElementById("navBar").classList.toggle("show");
    if (document.getElementById("abtBar").classList.contains('show')) {
        document.getElementById("abtBar").classList.remove('show');
    }
}
function abtNav() {
    document.getElementById("abtBar").classList.toggle("show");
    if (document.getElementById("navBar").classList.contains('show')) {
        document.getElementById("navBar").classList.remove('show');
    }
}
// Close the dropdown menu if the user clicks outside of it
window.onclick = function(event) {
    if (!event.target.matches('.navbtn')) {

        var dropdowns = document.getElementsByClassName("dropdown-content");
        var i;
        for (i = 0; i < dropdowns.length; i++) {
            var openDropdown = dropdowns[i];
            if (openDropdown.classList.contains('show')) {
                openDropdown.classList.remove('show');
            }
        }
    }
}
function scrolltop() {
    window.scrollBy(0, 500)
}

$(function(){
if (window.location.hash){
      var hash = window.location.hash.substring(1);
      if (hash == "relocation2010"){
         document.getElementById('country2010').style.display = 'block';
      }
      if (hash == "relocation2013"){
         document.getElementById('country2013').style.display = 'block';
      }
      if (hash == "relocation2015"){
         document.getElementById('country2015').style.display = 'block';
      }
      if (hash == "relocation_manu2010"){
         document.getElementById('manu2010').style.display = 'block';
      }
      if (hash == "relocation_manu2013"){
         document.getElementById('manu2013').style.display = 'block';
      }
      if (hash == "relocation_manu2015"){
         document.getElementById('manu2015').style.display = 'block';
      }
      if (hash == "relocation_ph2010"){
         document.getElementById('patent2010').style.display = 'block';
      }
      if (hash == "relocation_ph2013"){
         document.getElementById('patent2013').style.display = 'block';
      }
       if (hash == "relocation_ph2015"){
         document.getElementById('patent2015').style.display = 'block';
      }
      if (hash == "relocation_drug2010"){
         document.getElementById('drug2010').style.display = 'block';
      }
      if (hash == "relocation_drug2013"){
         document.getElementById('drug2013').style.display = 'block';
      }
      if (hash == "relocation_drug2015"){
         document.getElementById('drug2015').style.display = 'block';
      }
      if (hash == "relocation_disease2010"){
         document.getElementById('disease2010').style.display = 'block';
      }
      if (hash == "relocation_disease2013"){
         document.getElementById('disease2013').style.display = 'block';
      }
      if (hash == "relocation_disease2015"){
         document.getElementById('disease2015').style.display = 'block';
      }
   }
});

