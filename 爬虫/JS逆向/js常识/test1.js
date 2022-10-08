var o = (null === (n = window.byted_acrawler) || void 0 === n ? void 0 : null === (a = n.sign) || void 0 === a ? void 0 : a.call(n, i)) || "";

null === (n = window.byted_acrawler) || void 0 === n ? void 0 : null === (a = n.sign) || void 0 === a ? void 0 : a.call(n, i)



n = window.byted_acrawler  // -->  确定不为空
// void 0 --> undefined
null === n || void 0 === n ? void 0 : null === (a = n.sign) || void 0 === a ? void 0 : a.call(n, i)
//    |               |
//    V               V
// false || false ? void 0 : null === (a = n.sign) || void 0 === a ? void 0 : a.call(n, i)
// false ? void 0 : null === (a = n.sign) || void 0 === a ? void 0 : a.call(n, i)
// null === (a = n.sign) || void 0 === a ? void 0 : a.call(n, i)
a = window.byted_acrawler.sign  //  -->  确定不为空
// null === a || void 0 === a ? void 0 : a.call(n, i)
//       |               |
//       V               V
// false ? void 0 : a.call(n, i)
a.call(n, i)
//  |
//  V
window.byted_acrawler.sign.call(n, i)   // -->  确定不为空

//所以
var o = window.byted_acrawler.sign.call(n, i) || ""  // 确定有值
var o = window.byted_acrawler.sign.call(n, i)
