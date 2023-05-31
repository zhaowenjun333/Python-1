function rtid() {
    var e = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
      , t = 32
      , n = [];
    for (; t-- > 0; )
        n[t] = e.charAt(Math.random() * e.length);
    return n.join("")
};

console.log(rtid())
