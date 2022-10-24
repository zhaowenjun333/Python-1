const jsdom = require('jsdom');
const {JSDOM} = jsdom;

const resourceLoader = new jsdom.ResourceLoader({
    userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
});

const html = `<!DOCTYPE html><p>Hello world</p>`;

const dom = new JSDOM(html, {
    url: 'https://www.toutiao.com/',
    referrer: 'https://example.com/',
    contentType: 'text/html',
    resources: resourceLoader,
});

// console.log(dom.window.location)
// console.log(dom.window.navigator.userAgent)
// console.log(dom.window.document.referrer)

window = global   // node全局变量 + 一些浏览器必备的工具

const params = {
    location: {
        hash: '',
        host: "www.toutiao.com" ,
        hostname: "ww.toutiao.com",
        href: "https://www.toutiao.com",
        origin: "https:/ /www.toutiao.com",
        pathname: "/",
        port: '',
        protocol: "https:",
        search: '',
    },
    navigator: {
        appCodeName: "Mozilla",
        appName: "Netscape",
        appVersion: "5,0 (Nacintosh; Intel Mac OS X 10_15_7)AppleWebKit/537.36(RHITML，1like Cecko)Cchrome/93,0.4577.82 Safari/37.36",
        cookieEnabled:true,
        deviceMemory: 8,
        doNotTrack: null,
        hardwareConcurrency: 4,
        language: "zh-CN",
        languages: [" zh-CN", "zh"],
        maxTouchPoints: 0,
        onLine: true,
        platform: "MacIntel",
        product: "Gecko",
        productSub: "20030107",
        userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
        vendorSub: "",
        webdriver: false
    }
};

Object.assign(global, params)


// function xx(){
//     console.log(window.navigator.userAgent);
//     console.log(window.location.href);
// }
// xx()
//
// function xxx(){
//     console.log(navigator.userAgent);
//     console.log(location.href);
// }
// xxx()

function xxxx(){
    console.log(navigator.userAgent);
    console.log(location.href);

    setInterval(function () {

    }, 1000)
}
xxxx()