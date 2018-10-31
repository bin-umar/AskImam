var hijri = document.getElementById("hijri");
var grigorian = document.getElementById("grigorian");

hijri.innerHTML = HijriJS.todayHijri();
grigorian.innerHTML = HijriJS.todayGregorian();
