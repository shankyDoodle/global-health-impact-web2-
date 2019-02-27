
function resize(perc) {
    return (perc/100) * 200;
};
function clickBar(count,total,tb,malaria,hiv,schis,onch,lf,hook,round,whip) {
    document.getElementById("smallbartxt").innerHTML = name;
    document.getElementById("tbbar").style.width = resize(tb) + "px";
    document.getElementById("malbar").style.width = resize(malaria) + "px";
    document.getElementById("hivbar").style.width = resize(hiv) + "px";
    document.getElementById("schisbar").style.width = resize(schis) + "px";
    document.getElementById("onchbar").style.width = resize(onch) + "px";
    document.getElementById("lfbar").style.width = resize(lf) + "px";
    document.getElementById("hookbar").style.width = resize(hook) + "px";
    document.getElementById("roundbar").style.width = resize(round) + "px";
    document.getElementById("whipbar").style.width = resize(whip) + "px";
    document.getElementById("smallbars").style.display = "block";
};