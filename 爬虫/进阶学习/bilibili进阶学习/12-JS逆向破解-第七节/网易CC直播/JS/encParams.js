var l = 0,
    u = 16,
    _ = [214, 144, 233, 254, 204, 225, 61, 183, 22, 182, 20, 194, 40, 251, 44, 5, 43, 103, 154, 118, 42, 190, 4, 195, 170, 68, 19, 38, 73, 134, 6, 153, 156, 66, 80, 244, 145, 239, 152, 122, 51, 84, 11, 67, 237, 207, 172, 98, 228, 179, 28, 169, 201, 8, 232, 149, 128, 223, 148, 250, 117, 143, 63, 166, 71, 7, 167, 252, 243, 115, 23, 186, 131, 89, 60, 25, 230, 133, 79, 168, 104, 107, 129, 178, 113, 100, 218, 139, 248, 235, 15, 75, 112, 86, 157, 53, 30, 36, 14, 94, 99, 88, 209, 162, 37, 34, 124, 59, 1, 33, 120, 135, 212, 0, 70, 87, 159, 211, 39, 82, 76, 54, 2, 231, 160, 196, 200, 158, 234, 191, 138, 210, 64, 199, 56, 181, 163, 247, 242, 206, 249, 97, 21, 161, 224, 174, 93, 164, 155, 52, 26, 85, 173, 147, 50, 48, 245, 140, 177, 227, 29, 246, 226, 46, 130, 102, 202, 96, 192, 41, 35, 171, 13, 83, 78, 111, 213, 219, 55, 69, 222, 253, 142, 47, 3, 255, 106, 114, 109, 108, 91, 81, 141, 27, 175, 146, 187, 221, 188, 127, 17, 217, 92, 65, 31, 16, 90, 216, 10, 193, 49, 136, 165, 205, 123, 189, 45, 116, 208, 18, 184, 229, 180, 176, 137, 105, 151, 74, 12, 150, 119, 126, 101, 185, 241, 9, 197, 110, 198, 132, 24, 240, 125, 236, 58, 220, 77, 32, 121, 238, 95, 62, 215, 203, 57, 72],
    f = [462357, 472066609, 943670861, 1415275113, 1886879365, 2358483617, 2830087869, 3301692121, 3773296373, 4228057617, 404694573, 876298825, 1347903077, 1819507329, 2291111581, 2762715833, 3234320085, 3705924337, 4177462797, 337322537, 808926789, 1280531041, 1752135293, 2223739545, 2695343797, 3166948049, 3638552301, 4110090761, 269950501, 741554753, 1213159005, 1684763257];

function i(e) {
    for (var t = [], n = 0, i = e.length; n < i; n += 2)
        t.push(parseInt(e.substr(n, 2), 16));
    return t
}
function a(e, t) {
    return e << t | e >>> 32 - t
}
function s(e) {
    return (255 & _[e >>> 24 & 255]) << 24 | (255 & _[e >>> 16 & 255]) << 16 | (255 & _[e >>> 8 & 255]) << 8 | 255 & _[255 & e]
}
function r(e) {
    return e ^ a(e, 2) ^ a(e, 10) ^ a(e, 18) ^ a(e, 24)
}
function o(e) {
    return e ^ a(e, 13) ^ a(e, 23)
}

function c(e, t, n, a) {
    var c = 3 < arguments.length && void 0 !== a ? a : {}
      , _ = c.padding
      , h = void 0 === _ ? "pkcs#5" : _
      , p = c.mode
      , _ = c.iv
      , _ = void 0 === _ ? [] : _
      , c = c.output
      , c = void 0 === c ? "string" : c;
    if ("cbc" === p && 16 !== (_ = "string" == typeof _ ? i(_) : _).length)
        throw new Error("iv is invalid");
    if (16 !== (t = "string" == typeof t ? i(t) : t).length)
        throw new Error("key is invalid");
    if (e = ("string" == typeof e ? n !== l ? function(e) {
        for (var t = [], n = 0, i = e.length; n < i; n++) {
            var a = e.codePointAt(n);
            if (a <= 127)
                t.push(a);
            else if (a <= 2047)
                t.push(192 | a >>> 6),
                t.push(128 | 63 & a);
            else if (a <= 55295 || 57344 <= a && a <= 65535)
                t.push(224 | a >>> 12),
                t.push(128 | a >>> 6 & 63),
                t.push(128 | 63 & a);
            else {
                if (!(65536 <= a && a <= 1114111))
                    throw t.push(a),
                    new Error("input is not supported");
                n++,
                t.push(240 | a >>> 18 & 28),
                t.push(128 | a >>> 12 & 63),
                t.push(128 | a >>> 6 & 63),
                t.push(128 | 63 & a)
            }
        }
        return t
    }
    : i : d)(e),
    "pkcs#5" === h && n !== l)
        for (var m = u - e.length % u, g = 0; g < m; g++)
            e.push(m);
    var b = new Array(32);
    !function(e, t, n) {
        for (var i = new Array(4), a = new Array(4), r = 0; r < 4; r++)
            a[0] = 255 & e[0 + 4 * r],
            a[1] = 255 & e[1 + 4 * r],
            a[2] = 255 & e[2 + 4 * r],
            a[3] = 255 & e[3 + 4 * r],
            i[r] = a[0] << 24 | a[1] << 16 | a[2] << 8 | a[3];
        i[0] ^= 2746333894,
        i[1] ^= 1453994832,
        i[2] ^= 1736282519,
        i[3] ^= 2993693404;
        for (var c, d = 0; d < 32; d += 4)
            c = i[1] ^ i[2] ^ i[3] ^ f[d + 0],
            t[d + 0] = i[0] ^= o(s(c)),
            c = i[2] ^ i[3] ^ i[0] ^ f[d + 1],
            t[d + 1] = i[1] ^= o(s(c)),
            c = i[3] ^ i[0] ^ i[1] ^ f[d + 2],
            t[d + 2] = i[2] ^= o(s(c)),
            c = i[0] ^ i[1] ^ i[2] ^ f[d + 3],
            t[d + 3] = i[3] ^= o(s(c));
        if (n === l)
            for (var u, _ = 0; _ < 16; _++)
                u = t[_],
                t[_] = t[31 - _],
                t[31 - _] = u
    }(t, b, n);
    for (var v = [], y = _, $ = e.length, C = 0; u <= $; ) {
        var w = e.slice(C, C + 16)
          , x = new Array(16);
        if ("cbc" === p)
            for (var T = 0; T < u; T++)
                n !== l && (w[T] ^= y[T]);
        !function(e, t, n) {
            for (var i = new Array(4), a = new Array(4), o = 0; o < 4; o++)
                a[0] = 255 & e[4 * o],
                a[1] = 255 & e[4 * o + 1],
                a[2] = 255 & e[4 * o + 2],
                a[3] = 255 & e[4 * o + 3],
                i[o] = a[0] << 24 | a[1] << 16 | a[2] << 8 | a[3];
            for (var c, d = 0; d < 32; d += 4)
                c = i[1] ^ i[2] ^ i[3] ^ n[d + 0],
                i[0] ^= r(s(c)),
                c = i[2] ^ i[3] ^ i[0] ^ n[d + 1],
                i[1] ^= r(s(c)),
                c = i[3] ^ i[0] ^ i[1] ^ n[d + 2],
                i[2] ^= r(s(c)),
                c = i[0] ^ i[1] ^ i[2] ^ n[d + 3],
                i[3] ^= r(s(c));
            for (var l = 0; l < 16; l += 4)
                t[l] = i[3 - l / 4] >>> 24 & 255,
                t[l + 1] = i[3 - l / 4] >>> 16 & 255,
                t[l + 2] = i[3 - l / 4] >>> 8 & 255,
                t[l + 3] = 255 & i[3 - l / 4]
        }(w, x, b);
        for (var E = 0; E < u; E++)
            "cbc" === p && n === l && (x[E] ^= y[E]),
            v[C + E] = x[E];
        "cbc" === p && (y = n !== l ? x : w),
        $ -= u,
        C += u
    }
    return "pkcs#5" === h && n === l && (h = v[v.length - 1],
    v.splice(v.length - h, h)),
    "array" !== c ? n !== l ? v.map(function(e) {
        return 1 === (e = e.toString(16)).length ? "0" + e : e
    }).join("") : function(e) {
        for (var t = [], n = 0, i = e.length; n < i; n++)
            240 <= e[n] && e[n] <= 247 ? (t.push(String.fromCodePoint(((7 & e[n]) << 18) + ((63 & e[n + 1]) << 12) + ((63 & e[n + 2]) << 6) + (63 & e[n + 3]))),
            n += 3) : 224 <= e[n] && e[n] <= 239 ? (t.push(String.fromCodePoint(((15 & e[n]) << 12) + ((63 & e[n + 1]) << 6) + (63 & e[n + 2]))),
            n += 2) : 192 <= e[n] && e[n] <= 223 ? (t.push(String.fromCodePoint(((31 & e[n]) << 6) + (63 & e[n + 1]))),
            n++) : t.push(String.fromCodePoint(e[n]));
        return t.join("")
    }(v) : v
}

function encrypt(e, t, n) {
    return c(e, t, 1, n)
}


e = {
    "un": "17302254866@163.com",
    "capkey": "744e2a6324ec5370616241baf4507538",
    "pd": "cc",
    "pkid": "PFClpTB",
    "cap": "CN31_RbmuR65xQhNjLcvsoyCrkNUz5s.MZo-wCrN9dxNi0AADxDZZ6sR1zy9P4ZOwL75aJdzjGN9fn_xJXgaTOi.rg8eWhJ0SjgMR-ihX8I09MKTPjy2pkQVc5LI4Z7ZAthsBGps1gvO1--O0BnLBV64jfSWH1BrqdFRWThBPJLkxgljXcNpemOnyLQrU6cGGowCqVmHqTt2KlBhMGy2BiXuIdAi46IeZbyOd1i1oxwFCidGWspvUMBvs2tuhhfjVUJ_d_IAtFvCnruqkLE_WiU5Hbesm_WYyUl4AISIgZ4xBelXB1ul8rcybgh2BhkMdoOxULpAtqLpDXkbyNBP94NEgL7Tm8GNhT8AY5OBzqI9_wQVlah_AM5PnNqxM_NHqiUmXKwR_pB6VGudtb8JzMtChwonaiWBUMzq6zh7Pw10F5HIOF--XXHQ.Vjl_jexPeHbUymhiISFYiFmAiNxoxyMWZrUMkvveXEjYq5e4ZbhgdjD_bxCqwHmpHknF4xI3",
    "channel": 0,
    "topURL": "https://cc.163.com/category/",
    "rtid": "Gz7SjbXHaMOAZj9Urv3HzCANsvUBrB1L"
}

function encParams(e){
    return encrypt(JSON.stringify(e), 'BC60B8B9E4FFEFFA219E5AD77F11F9E2')
}

console.log(encParams(e))
//7e3ba6f5eea9ee4fe8c8bf6a367329fa8ae97d92bf431367362db28508e37e245abf73b2d20c6ecce7998087abae2050567ccec30ee4300d780cb67a9088f2efd649ececf1d215d52be81c7e374efd335c7b9aa48944dfd3c1b94e512b9bb86c2a68af610a7e4e8181ce342d4bfb725d1db7dcfcf3137175370c7ece95681524fdc83f03772c2ae7c2c34f5129d4826e174b19423f4672da3eea79bb3894473d997d834fcb3ed5b55582c08bb00ce94bfc79d0dea96e39fd359da2dacf915bd2fff8071653656c11643d008507547a911e2e543d0315af8741b65b117ea2840dbeba0816489911199cf5f85e0a9cc4cf1d2711aa8ef802bd801f97992f35451584fb8618c0a5657eb5c40323f5e43c37fd0a745d4beb1f1b6b3253eb7796eaa91d9b858d4ea349146ba000fea482509f311bc0da626cafc0746536a3ec33974d1ee17e48b1fbcdd724c9ede5bea4bd41d2d62b80a3b8030be6e9e13f584ea91152f49c01d809d0f756841ab07b42e4ce497844401dcb3a2f561a1a077683e608abc98d90787dd7b3e480760adceb5f124d3532a28bf5059031678f2148ba5968a834f4016971b9cd8765e8db7e111727bd38b0d113838cc3af39c1a1533e4bde19077e642e83de684dd6db7c1837d1a88474758cea09cf0de95652a8f5e9e24c917222902a99647ae7e37c7bb6126026a19fcedb1bc88b7f50480d276da137b3c6bea5ede70155707991e4e5e76e0f037112e694324254d43d582d3300bcb3385883b48dd249fcf32aaf9b02c7c0ab4fdf54a692888711e27d7ee9285b999402858d332270a1996b05d2bf3c5a10670359cb47a25d60bb584ee62b25f1fb3c75380eeaf1fe8c3838210d86a5c4b4ca8e8ad7de2de8a2551610f9bada422a057b62947cee704006bc1f2a504280942814b5cece1d879e9f550d2e1d1cdc92689057b3c89d800a982c48238786c43346b9f7195e48bf94b24b6456e1fa3f95780aff692eaebea478f21f45a59d4e1c0083

