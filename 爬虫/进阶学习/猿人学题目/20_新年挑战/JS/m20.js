
function sign(content) {
    const retptr = _index_bg_wasm__WEBPACK_IMPORTED_MODULE_0__["__wbindgen_add_to_stack_pointer"](-16);
    var ptr0 = passStringToWasm0(content, _index_bg_wasm__WEBPACK_IMPORTED_MODULE_0__["__wbindgen_malloc"], _index_bg_wasm__WEBPACK_IMPORTED_MODULE_0__["__wbindgen_realloc"]);
    var len0 = WASM_VECTOR_LEN;
    _index_bg_wasm__WEBPACK_IMPORTED_MODULE_0__["sign"](retptr, ptr0, len0);
    var r0 = getInt32Memory0()[retptr / 4 + 0];
    var r1 = getInt32Memory0()[retptr / 4 + 1];
    return getStringFromWasm0(r0, r1);
}


t = Date.parse(new Date())
sign = window.sign(3 + '|' + t.toString())
