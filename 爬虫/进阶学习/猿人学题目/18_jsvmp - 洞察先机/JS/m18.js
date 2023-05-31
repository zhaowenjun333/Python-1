// hook 思路，用其他变量接受，然后再改写
/*
_enc = _[1][0]['CryptoJS']['AES'].encrypt
_[1][0]['CryptoJS']['AES'].encrypt = function (text, key, type) {
    let a = _enc(text, key, type).toString();
    debugger;
    return a;
}
*/

/*  ****** 查看AES加密参数 ******
text: _[1][0]['CryptoJS'].enc.Utf8.stringify(text)
key:  _[1][0]['CryptoJS'].enc.Utf8.stringify(key)
type: _[1][0]['CryptoJS'].enc.Utf8.stringify(type)
type.iv: _[1][0]['CryptoJS'].enc.Utf8.stringify(type.iv)
type.mode: _[1][0]['CryptoJS'].enc.Utf8.stringify(type.mode)
type.padding: _[1][0]['CryptoJS'].enc.Utf8.stringify(type.padding)
*/


function get_v(page) {
    var CryptoJS = require('crypto-js'),
    t = Date.parse(new Date) / 1000,
    text = page + '|489m361,488m361,487m361,487d361,487u361';
    word = CryptoJS.enc.Utf8.parse(text);
    key = CryptoJS.enc.Utf8.parse(t.toString(16) + t.toString(16));
// console.log(word, key)
    v = CryptoJS.AES.encrypt(word, key, {
        iv: key,
        mode: CryptoJS.mode.CBC,
        padding: CryptoJS.pad.Pkcs7
    }).toString();
    return [t, v];
}

console.log(get_v(2))
