// ==UserScript==
// @name         hook 无限debugger
// @namespace    http://tampermonkey.net/
// @version      0.1
// @description  try to take over the world!
// @author       You
// @run-at       document-start
// @match        https://www.wangluozhe.com/challenge/1
// @grant        none
// ==/UserScript==

// Function.prototype.constructor_hook = Function.prototype.constructor;
// Function.prototype.constructor = function(s) {
//     if (s == 'debugger') {
//         return []
//     }
//     return Function.prototype.constructor_hook(s);
// }
//
// var _setInterval = setInterval
// setInterval = function setInterval(code, time) {
//     if (time == 0X7d0) {
//         return function () {}
//     }
//     return _setInterval(code, time)
// }

// ************************************* 原码 *************************************
// IIlIliii() + IlIliI1l() + iIlII1I1() + window[liIIIi11('20')]
// ************************************* 原码 *************************************

// 获取原码方法，控制台运行

const jsdom = require('jsdom');
window = global;
const {
    JSDOM
} = jsdom;

const dom = new JSDOM(`<html><head></head><body></body></html>`);
const document = dom.window.document;

var iｉl = 'jsjiami.com.v6'
  , iiIIilii = [
    "setInterval",
    "jsj",
    "iam",
    "undefi",
    "ned",
    "i.com.v",
    "length",
    "push",
    "apply",
    "byted_acrawler",
    "sign",
    "createElement",
    "parse",
    "toString",
    "123456789abcdefghigklmnopqrstuvwxyz",
    "function *\\( *\\)",
    "\\+\\+ *(?:(?:[a-z0-9A-Z_]){1,8}|(?:\\b|\\d)[a-z0-9_]{1,8}(?:\\b|\\d))",
    "init",
    "test",
    "chain",
    "input",
    "return (function() ",
    "{}.constructor(\"return this\")( )",
    "console",
    "log",
    "warn",
    "debug",
    "info",
    "error",
    "exception",
    "trace",
    "defineProperty",
    "code",
    "_signature",
    "function eval() { [native code] }",
    "function toString() { [native code] }",
    "gnature = window.byted_acrawler(window.sign())",
    "gnature = window.byted_acrawlers(window.signs())",
    "abc",
    "900150983cd24fb0d6963f7d28e17f72",
    "window",
    "._si",
    "concat",
    "userAgent",
    "function setInterval() { [native code] }",
    "charCodeAt",
    "fromCharCode",
    "document",
    "location",
    "href",
    "availHeight",
    "0123456789ABCDEF",
    "0123456789abcdef",
    "charAt",
    "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/",
    "get_sign",
    "string",
    "constructor",
    "debugger;",
    "counter",
    "debu",
    "gger",
    "call",
    "action",
    "stateObject"
];
var liIIIi11 = function(_0x11145e, _0x3cbe90) {
    _0x11145e = ~~'0x'['concat'](_0x11145e);
    var _0x636e4d = iiIIilii[_0x11145e];
    return _0x636e4d;
};

var l1liii11 = function() {
    var ilI1ilI = !![];
    return function(iIliII1l, IlliIIi1) {
        var li11lII1 = ilI1ilI ? function() {
            if (IlliIIi1) {
                var li11lIl1 = IlliIIi1[liIIIi11('8')](iIliII1l, arguments);
                IlliIIi1 = null;
                return li11lIl1;
            }
        }
        : function() {}
        ;
        ilI1ilI = ![];
        return li11lII1;
    }
    ;
}();
window[liIIIi11('9')] = function byted_acrawler() {
    return IIl1llI1(sign());
}
;
window[liIIIi11('a')] = function sign() {
    try {
        div = document[liIIIi11('b')];
        return Date[liIIIi11('c')](new Date())[liIIIi11('d')]();
    } catch (IIl1lI1i) {
        return liIIIi11('e');
    }
};

var iiil1 = 0x0;
var l11il1l1 = '';
var ii1Ii = 0x8;
function i1Il11i(iiIll1i) {
    return lIIiiI1l(iIIiIlli(IIl111li(iiIll1i), iiIll1i[liIIIi11('6')] * ii1Ii));
}
function I1lIIlil(l11l1iIi) {
    return I1i11ll(iIIiIlli(IIl111li(l11l1iIi), l11l1iIi[liIIIi11('6')] * ii1Ii));
}
function lllIIiI(IIi1lIil) {
    return l1IlIlIi(iIIiIlli(IIl111li(IIi1lIil), IIi1lIil[liIIIi11('6')] * ii1Ii));
}
function IilIlI1i(ll1l1ii1, Ilil1i11) {
    return lIIiiI1l(Iii1I1il(ll1l1ii1, Ilil1i11));
}
function llII11iI(IllliliI, IIIIilI) {
    return I1i11ll(Iii1I1il(IllliliI, IIIIilI));
}
function l11l1iil(liii1iI1, lilii111) {
    return l1IlIlIi(Iii1I1il(liii1iI1, lilii111));
}
function lIliIIII() {
    return i1Il11i(liIIIi11('26')) == liIIIi11('27');
}
function iIIiIlli(lIliI1I1, lllI11lI) {
    lIliI1I1[lllI11lI >> 0x5] |= 0x80 << lllI11lI % 0x20;
    lIliI1I1[(lllI11lI + 0x40 >>> 0x9 << 0x4) + 0xe] = lllI11lI;
    var ill1Ill = 0x67452301;
    var iI1l1iIi = -0x10325477;
    var I1l1iI1 = -0x67452302;
    var IIlili = 0x10325476;
    for (var lii11ii = 0x0; lii11ii < lIliI1I1[liIIIi11('6')]; lii11ii += 0x10) {
        var IlIIIIl1 = ill1Ill;
        var il1I1li = iI1l1iIi;
        var lilIlIi1 = I1l1iI1;
        var lli11i1i = IIlili;
        ill1Ill = iiiIillI(ill1Ill, iI1l1iIi, I1l1iI1, IIlili, lIliI1I1[lii11ii + 0x0], 0x7, -0x28955b88);
        IIlili = iiiIillI(IIlili, ill1Ill, iI1l1iIi, I1l1iI1, lIliI1I1[lii11ii + 0x1], 0xc, -0x173848aa);
        I1l1iI1 = iiiIillI(I1l1iI1, IIlili, ill1Ill, iI1l1iIi, lIliI1I1[lii11ii + 0x2], 0x11, 0x242070db);
        iI1l1iIi = iiiIillI(iI1l1iIi, I1l1iI1, IIlili, ill1Ill, lIliI1I1[lii11ii + 0x3], 0x16, -0x3e423112);
        ill1Ill = iiiIillI(ill1Ill, iI1l1iIi, I1l1iI1, IIlili, lIliI1I1[lii11ii + 0x4], 0x7, -0xa83f051);
        IIlili = iiiIillI(IIlili, ill1Ill, iI1l1iIi, I1l1iI1, lIliI1I1[lii11ii + 0x5], 0xc, 0x4787c62a);
        I1l1iI1 = iiiIillI(I1l1iI1, IIlili, ill1Ill, iI1l1iIi, lIliI1I1[lii11ii + 0x6], 0x11, -0x57cfb9ed);
        iI1l1iIi = iiiIillI(iI1l1iIi, I1l1iI1, IIlili, ill1Ill, lIliI1I1[lii11ii + 0x7], 0x16, -0x2b96aff);
        ill1Ill = iiiIillI(ill1Ill, iI1l1iIi, I1l1iI1, IIlili, lIliI1I1[lii11ii + 0x8], 0x7, 0x698098d8);
        IIlili = iiiIillI(IIlili, ill1Ill, iI1l1iIi, I1l1iI1, lIliI1I1[lii11ii + 0x9], 0xc, -0x74bb0851);
        I1l1iI1 = iiiIillI(I1l1iI1, IIlili, ill1Ill, iI1l1iIi, lIliI1I1[lii11ii + 0xa], 0x11, -0xa44f);
        iI1l1iIi = iiiIillI(iI1l1iIi, I1l1iI1, IIlili, ill1Ill, lIliI1I1[lii11ii + 0xb], 0x16, -0x76a32842);
        ill1Ill = iiiIillI(ill1Ill, iI1l1iIi, I1l1iI1, IIlili, lIliI1I1[lii11ii + 0xc], 0x7, 0x6b901122);
        IIlili = iiiIillI(IIlili, ill1Ill, iI1l1iIi, I1l1iI1, lIliI1I1[lii11ii + 0xd], 0xc, -0x2678e6d);
        I1l1iI1 = iiiIillI(I1l1iI1, IIlili, ill1Ill, iI1l1iIi, lIliI1I1[lii11ii + 0xe], 0x11, -0x5986bc72);
        iI1l1iIi = iiiIillI(iI1l1iIi, I1l1iI1, IIlili, ill1Ill, lIliI1I1[lii11ii + 0xf], 0x16, 0x49b40821);
        ill1Ill = lillIii1(ill1Ill, iI1l1iIi, I1l1iI1, IIlili, lIliI1I1[lii11ii + 0x1], 0x5, -0x9e1da9e);
        IIlili = lillIii1(IIlili, ill1Ill, iI1l1iIi, I1l1iI1, lIliI1I1[lii11ii + 0x6], 0x9, -0x3fbf4cc0);
        I1l1iI1 = lillIii1(I1l1iI1, IIlili, ill1Ill, iI1l1iIi, lIliI1I1[lii11ii + 0xb], 0xe, 0x265e5a51);
        iI1l1iIi = lillIii1(iI1l1iIi, I1l1iI1, IIlili, ill1Ill, lIliI1I1[lii11ii + 0x0], 0x14, -0x16493856);
        ill1Ill = lillIii1(ill1Ill, iI1l1iIi, I1l1iI1, IIlili, lIliI1I1[lii11ii + 0x5], 0x5, -0x29d0efa3);
        IIlili = lillIii1(IIlili, ill1Ill, iI1l1iIi, I1l1iI1, lIliI1I1[lii11ii + 0xa], 0x9, 0x2441453);
        I1l1iI1 = lillIii1(I1l1iI1, IIlili, ill1Ill, iI1l1iIi, lIliI1I1[lii11ii + 0xf], 0xe, -0x275e197f);
        iI1l1iIi = lillIii1(iI1l1iIi, I1l1iI1, IIlili, ill1Ill, lIliI1I1[lii11ii + 0x4], 0x14, -0x182c0438);
        ill1Ill = lillIii1(ill1Ill, iI1l1iIi, I1l1iI1, IIlili, lIliI1I1[lii11ii + 0x9], 0x5, 0x21e1cde6);
        IIlili = lillIii1(IIlili, ill1Ill, iI1l1iIi, I1l1iI1, lIliI1I1[lii11ii + 0xe], 0x9, -0x3cc8f82a);
        I1l1iI1 = lillIii1(I1l1iI1, IIlili, ill1Ill, iI1l1iIi, lIliI1I1[lii11ii + 0x3], 0xe, -0xb2af279);
        iI1l1iIi = lillIii1(iI1l1iIi, I1l1iI1, IIlili, ill1Ill, lIliI1I1[lii11ii + 0x8], 0x14, 0x455a14ed);
        ill1Ill = lillIii1(ill1Ill, iI1l1iIi, I1l1iI1, IIlili, lIliI1I1[lii11ii + 0xd], 0x5, -0x561c16fb);
        IIlili = lillIii1(IIlili, ill1Ill, iI1l1iIi, I1l1iI1, lIliI1I1[lii11ii + 0x2], 0x9, -0x3105c08);
        I1l1iI1 = lillIii1(I1l1iI1, IIlili, ill1Ill, iI1l1iIi, lIliI1I1[lii11ii + 0x7], 0xe, 0x676f02d9);
        iI1l1iIi = lillIii1(iI1l1iIi, I1l1iI1, IIlili, ill1Ill, lIliI1I1[lii11ii + 0xc], 0x14, -0x72d5b376);
        ill1Ill = liIiiiiI(ill1Ill, iI1l1iIi, I1l1iI1, IIlili, lIliI1I1[lii11ii + 0x5], 0x4, -0x5c6be);
        IIlili = liIiiiiI(IIlili, ill1Ill, iI1l1iIi, I1l1iI1, lIliI1I1[lii11ii + 0x8], 0xb, -0x788e097f);
        I1l1iI1 = liIiiiiI(I1l1iI1, IIlili, ill1Ill, iI1l1iIi, lIliI1I1[lii11ii + 0xb], 0x10, 0x6d9d6122);
        iI1l1iIi = liIiiiiI(iI1l1iIi, I1l1iI1, IIlili, ill1Ill, lIliI1I1[lii11ii + 0xe], 0x17, -0x21ac7f4);
        ill1Ill = liIiiiiI(ill1Ill, iI1l1iIi, I1l1iI1, IIlili, lIliI1I1[lii11ii + 0x1], 0x4, -0x5b4115bc);
        IIlili = liIiiiiI(IIlili, ill1Ill, iI1l1iIi, I1l1iI1, lIliI1I1[lii11ii + 0x4], 0xb, 0x4bdecfa9);
        I1l1iI1 = liIiiiiI(I1l1iI1, IIlili, ill1Ill, iI1l1iIi, lIliI1I1[lii11ii + 0x7], 0x10, -0x944b4a0);
        iI1l1iIi = liIiiiiI(iI1l1iIi, I1l1iI1, IIlili, ill1Ill, lIliI1I1[lii11ii + 0xa], 0x17, -0x41404390);
        ill1Ill = liIiiiiI(ill1Ill, iI1l1iIi, I1l1iI1, IIlili, lIliI1I1[lii11ii + 0xd], 0x4, 0x289b7ec6);
        IIlili = liIiiiiI(IIlili, ill1Ill, iI1l1iIi, I1l1iI1, lIliI1I1[lii11ii + 0x0], 0xb, -0x155ed806);
        I1l1iI1 = liIiiiiI(I1l1iI1, IIlili, ill1Ill, iI1l1iIi, lIliI1I1[lii11ii + 0x3], 0x10, -0x2b10cf67);
        iI1l1iIi = liIiiiiI(iI1l1iIi, I1l1iI1, IIlili, ill1Ill, lIliI1I1[lii11ii + 0x6], 0x17, 0x4881d03);
        ill1Ill = liIiiiiI(ill1Ill, iI1l1iIi, I1l1iI1, IIlili, lIliI1I1[lii11ii + 0x9], 0x4, -0x262b2fc7);
        IIlili = liIiiiiI(IIlili, ill1Ill, iI1l1iIi, I1l1iI1, lIliI1I1[lii11ii + 0xc], 0xb, -0x1924661b);
        I1l1iI1 = liIiiiiI(I1l1iI1, IIlili, ill1Ill, iI1l1iIi, lIliI1I1[lii11ii + 0xf], 0x10, 0x1fa27cf8);
        iI1l1iIi = liIiiiiI(iI1l1iIi, I1l1iI1, IIlili, ill1Ill, lIliI1I1[lii11ii + 0x2], 0x17, -0x3b53a99b);
        ill1Ill = Ili1iIll(ill1Ill, iI1l1iIi, I1l1iI1, IIlili, lIliI1I1[lii11ii + 0x0], 0x6, -0xbd6ddbc);
        IIlili = Ili1iIll(IIlili, ill1Ill, iI1l1iIi, I1l1iI1, lIliI1I1[lii11ii + 0x7], 0xa, 0x432aff97);
        I1l1iI1 = Ili1iIll(I1l1iI1, IIlili, ill1Ill, iI1l1iIi, lIliI1I1[lii11ii + 0xe], 0xf, -0x546bdc59);
        iI1l1iIi = Ili1iIll(iI1l1iIi, I1l1iI1, IIlili, ill1Ill, lIliI1I1[lii11ii + 0x5], 0x15, -0x36c5fc7);
        ill1Ill = Ili1iIll(ill1Ill, iI1l1iIi, I1l1iI1, IIlili, lIliI1I1[lii11ii + 0xc], 0x6, 0x655b59c3);
        IIlili = Ili1iIll(IIlili, ill1Ill, iI1l1iIi, I1l1iI1, lIliI1I1[lii11ii + 0x3], 0xa, -0x70f3336e);
        I1l1iI1 = Ili1iIll(I1l1iI1, IIlili, ill1Ill, iI1l1iIi, lIliI1I1[lii11ii + 0xa], 0xf, -0x100b83);
        iI1l1iIi = Ili1iIll(iI1l1iIi, I1l1iI1, IIlili, ill1Ill, lIliI1I1[lii11ii + 0x1], 0x15, -0x7a7ba22f);
        ill1Ill = Ili1iIll(ill1Ill, iI1l1iIi, I1l1iI1, IIlili, lIliI1I1[lii11ii + 0x8], 0x6, 0x6fa87e4f);
        IIlili = Ili1iIll(IIlili, ill1Ill, iI1l1iIi, I1l1iI1, lIliI1I1[lii11ii + 0xf], 0xa, -0x1d31920);
        I1l1iI1 = Ili1iIll(I1l1iI1, IIlili, ill1Ill, iI1l1iIi, lIliI1I1[lii11ii + 0x6], 0xf, -0x5cfebcec);
        iI1l1iIi = Ili1iIll(iI1l1iIi, I1l1iI1, IIlili, ill1Ill, lIliI1I1[lii11ii + 0xd], 0x15, 0x4e0811a1);
        ill1Ill = Ili1iIll(ill1Ill, iI1l1iIi, I1l1iI1, IIlili, lIliI1I1[lii11ii + 0x4], 0x6, -0x8ac817e);
        IIlili = Ili1iIll(IIlili, ill1Ill, iI1l1iIi, I1l1iI1, lIliI1I1[lii11ii + 0xb], 0xa, -0x42c50dcb);
        I1l1iI1 = Ili1iIll(I1l1iI1, IIlili, ill1Ill, iI1l1iIi, lIliI1I1[lii11ii + 0x2], 0xf, 0x2ad7d2bb);
        iI1l1iIi = Ili1iIll(iI1l1iIi, I1l1iI1, IIlili, ill1Ill, lIliI1I1[lii11ii + 0x9], 0x15, -0x14792c6f);
        ill1Ill = l111i1I(ill1Ill, IlIIIIl1);
        iI1l1iIi = l111i1I(iI1l1iIi, il1I1li);
        I1l1iI1 = l111i1I(I1l1iI1, lilIlIi1);
        IIlili = l111i1I(IIlili, lli11i1i);
    }
    return Array(ill1Ill, iI1l1iIi, I1l1iI1, IIlili);
}
function IlIliI1l() {
    return liIIIi11('28');
}
function l1Ii1ili(IIl1i1ii, lI1li11l, lIll1lIi, ilIii1, ll11l1, I111ilI1) {
    return l111i1I(Il1111lI(l111i1I(l111i1I(lI1li11l, IIl1i1ii), l111i1I(ilIii1, I111ilI1)), ll11l1), lIll1lIi);
}
function iiiIillI(lI1lIll, iI1I1i11, iI1IilI, IIll1Il, lIiIIi, ii1Il1Ii, illlI11l) {
    return l1Ii1ili(iI1I1i11 & iI1IilI | ~iI1I1i11 & IIll1Il, lI1lIll, iI1I1i11, lIiIIi, ii1Il1Ii, illlI11l);
}
function lillIii1(Il1Il11, iI1IiIi, IliilIl, i11l111I, I1II1il1, liiiIl1, ll1Il1ll) {
    return l1Ii1ili(iI1IiIi & i11l111I | IliilIl & ~i11l111I, Il1Il11, iI1IiIi, I1II1il1, liiiIl1, ll1Il1ll);
}
function liIiiiiI(I1ii11Il, lIiI1Ili, ii11lili, ll1liiiI, lIIIl11l, lI1II1Il, lliiiI) {
    return l1Ii1ili(lIiI1Ili ^ ii11lili ^ ll1liiiI, I1ii11Il, lIiI1Ili, lIIIl11l, lI1II1Il, lliiiI);
}
function iIlII1I1(l11i1iI1, Il1Iiil1) {
    return liIIIi11('29');
}
function Ili1iIll(ii11lIll, iIiilli1, IIIlli1, iiIl1iII, Iillilll, lIIiI1II, iiiIlIl1) {
    return l1Ii1ili(IIIlli1 ^ (iIiilli1 | ~iiIl1iII), ii11lIll, iIiilli1, Iillilll, lIIiI1II, iiiIlIl1);
}
function Iii1I1il(l11ll1ll, IIlii1lI) {
    var Il1IlI1i = IIl111li(l11ll1ll);
    if (Il1IlI1i[liIIIi11('6')] > 0x10)
        Il1IlI1i = iIIiIlli(Il1IlI1i, l11ll1ll[liIIIi11('6')] * ii1Ii);
    var IiiiIlII = Array(0x10)
      , llIii11l = Array(0x10);
    for (var i1liIi = 0x0; i1liIi < 0x10; i1liIi++) {
        IiiiIlII[i1liIi] = Il1IlI1i[i1liIi] ^ 0x36363636;
        llIii11l[i1liIi] = Il1IlI1i[i1liIi] ^ 0x5c5c5c5c;
    }
    var ilIl1I1i = iIIiIlli(IiiiIlII[liIIIi11('2a')](IIl111li(IIlii1lI)), 0x200 + IIlii1lI[liIIIi11('6')] * ii1Ii);
    return iIIiIlli(llIii11l[liIIIi11('2a')](ilIl1I1i), 0x200 + 0x80);
}
function l111i1I(IIllIi1l, IIllI1l1) {
    var IIll1I11 = (IIllIi1l & 0xffff) + (IIllI1l1 & 0xffff);
    var i1iiiiI = (IIllIi1l >> 0x10) + (IIllI1l1 >> 0x10) + (IIll1I11 >> 0x10);
    return i1iiiiI << 0x10 | IIll1I11 & 0xffff;
}
function IIl1llI1(Iiilii1i) {
    try {
        nav = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36";
        return i1Il11i(Iiilii1i);
    } catch (IIilIIlI) {
        return i1Il11i(IIilIIlI);
    }
}

function Il1111lI(IilIiii1, iiI1i1i1) {
    return IilIiii1 << iiI1i1i1 | IilIiii1 >>> 0x20 - iiI1i1i1;
}
function IIl111li(lIiIIIi) {
    var IIli1i1 = Array();
    var lIliI1i1 = (0x1 << ii1Ii) - 0x1;
    for (var lIiiil1 = 0x0; lIiiil1 < lIiIIIi[liIIIi11('6')] * ii1Ii; lIiiil1 += ii1Ii)
        IIli1i1[lIiiil1 >> 0x5] |= (lIiIIIi[liIIIi11('2d')](lIiiil1 / ii1Ii) & lIliI1i1) << lIiiil1 % 0x20;
    return IIli1i1;
}
function l1IlIlIi(IIIiliII) {
    var I1l1III1 = '';
    var llIi1il1 = (0x1 << ii1Ii) - 0x1;
    for (var iIii1ll = 0x0; iIii1ll < IIIiliII[liIIIi11('6')] * 0x20; iIii1ll += ii1Ii)
        I1l1III1 += String[liIIIi11('2e')](IIIiliII[iIii1ll >> 0x5] >>> iIii1ll % 0x20 & llIi1il1);
    return I1l1III1;
}
function IIlIliii(II1, iIIiIIi1) {
    try {
        href = window[liIIIi11('2f')][liIIIi11('30')][liIIIi11('31')];
        check_screen = screen[liIIIi11('32')];
        window[liIIIi11('20')] = liIIIi11('24');
        return '';
    } catch (I1IiI1il) {
        window[liIIIi11('20')] = liIIIi11('25');
        return '';
    }
}
function lIIiiI1l(lilll1I1) {
    var ililI1i = iiil1 ? liIIIi11('33') : liIIIi11('34');
    var Iii1iiIl = '';
    for (var Illi1ill = 0x0; Illi1ill < lilll1I1[liIIIi11('6')] * 0x4; Illi1ill++) {
        Iii1iiIl += ililI1i[liIIIi11('35')](lilll1I1[Illi1ill >> 0x2] >> Illi1ill % 0x4 * 0x8 + 0x4 & 0xf) + ililI1i[liIIIi11('35')](lilll1I1[Illi1ill >> 0x2] >> Illi1ill % 0x4 * 0x8 & 0xf);
    }
    return Iii1iiIl;
}
function I1i11ll(liliII) {
    var iiiiII1I = liIIIi11('36');
    var IiilIl = '';
    for (var iliIiii1 = 0x0; iliIiii1 < liliII[liIIIi11('6')] * 0x4; iliIiii1 += 0x3) {
        var I1IlIIIi = (liliII[iliIiii1 >> 0x2] >> 0x8 * (iliIiii1 % 0x4) & 0xff) << 0x10 | (liliII[iliIiii1 + 0x1 >> 0x2] >> 0x8 * ((iliIiii1 + 0x1) % 0x4) & 0xff) << 0x8 | liliII[iliIiii1 + 0x2 >> 0x2] >> 0x8 * ((iliIiii1 + 0x2) % 0x4) & 0xff;
        for (var IIIl1ilI = 0x0; IIIl1ilI < 0x4; IIIl1ilI++) {
            if (iliIiii1 * 0x8 + IIIl1ilI * 0x6 > liliII[liIIIi11('6')] * 0x20)
                IiilIl += l11il1l1;
            else
                IiilIl += iiiiII1I[liIIIi11('35')](I1IlIIIi >> 0x6 * (0x3 - IIIl1ilI) & 0x3f);
        }
    }
    return IiilIl;
}
window._signature = window.byted_acrawler(window.sign());


function _signature() {
    return window._signature;
}

console.log(_signature())