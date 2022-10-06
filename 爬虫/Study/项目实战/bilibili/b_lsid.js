// e = this.splitDate()

// e.millisecond --> 时间戳 作为参数传递给f函数

// t = Object(f.b)(e.millisecond)
//     // ceil：向上取整
//     // toString(16)：转为十六进制的字符串
//     // toUpperCase()：大写
//     // Math.ceil(e).toString(16).toUpperCase()
//     // Math.ceil(时间戳).toString(16).toUpperCase()
//
// t = "".concat(Object(f.c)(8), "_").concat(t);
//
// c.a.setCookie("b_lsid", t, 0, "current-domain")
//
// t = new Date(Date.now())

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

o = function(e) {
    return Math.ceil(e).toString(16).toUpperCase()
}

a = function(e) {
    for (var t = "", n = 0; n < e; n++)
        t += o(16 * Math.random());
    return s(t, e)
}
s = function(e, t) {
    var n = "";
    if (e.length < t)
        for (var r = 0; r < t - e.length; r++)
            n += "0";
    return n + e
}

e = splitDate()
// console.log(e.millisecond)
// t = Object(o)(e.millisecond)
t = o(e.millisecond)
t = "".concat(a(8), "_").concat(t);
function b_lsid() {
    return t
}

console.log(b_lsid())
