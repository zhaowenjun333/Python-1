function get_t() {
    return parseInt(Math.round((new Date).getTime() / 1e3).toString())
}

console.log(get_t())