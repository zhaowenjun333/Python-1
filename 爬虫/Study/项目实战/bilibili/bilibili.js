function splitDate(e) {
    var t = new Date(e || Date.now())
      , n = t.getDate()
      , r = t.getHours()
      , e = t.getMinutes()
      , t = t.getTime();
    return {
        day: n,
        hour: r,
        minute: e,
        second: Math.floor(t / 1e3),
        millisecond: t
    }
}

a = function(e) {
    for (var t = "", n = 0; n < e; n++)
        t += o(16 * Math.random());
    return s(t, e)
}

o = function(e) {
    return Math.ceil(e).toString(16).toUpperCase()
}

s = function(e, t) {
    var n = "";
    if (e.length < t)
        for (var r = 0; r < t - e.length; r++)
            n += "0";
    return n + e
}

var r = function() {
    var e = a(8)
      , t = a(4)
      , n = a(4)
      , r = a(4)
      , o = a(12)
      , i = (new Date).getTime();
    return e + "-" + t + "-" + n + "-" + r + "-" + o + s((i % 1e5).toString(), 5) + "infoc"
}

e = splitDate()

t = o(e.millisecond)
t = "".concat(a(8), "_").concat(t);
function b_lsid() {
    return t
}