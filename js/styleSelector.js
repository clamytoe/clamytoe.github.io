//Dynamic stylesheet selector v1.0 20180810
//Author: Martin Uribe

function setStyle() {
    var i, cacheobj, altstyles=[""]

    for (i=0; (cacheobj=document.getElementsByTagName("link")[i]); i++) {
        if (cacheobj.getAttribute("rel").toLowerCase() == "alt style") {
            cacheobj.rel = "stylesheet"
            altstyles.push(cacheobj)
        }
    }

    var randomnumber = Math.floor(Math.random() * altstyles.length)
    var chosenstyle = altstyles[randomnumber]
    document.getElementsByTagName("head")[0].appendChild(chosenstyle)
    console.log("style: " + chosenstyle.href)
}

setStyle()
