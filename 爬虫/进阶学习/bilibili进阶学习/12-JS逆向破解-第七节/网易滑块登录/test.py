import time
import urllib.parse

url = 'https://webzjcaptcha.reg.163.com/api/v2/check?referer=https%3A%2F%2Fdl.reg.163.com%2Fwebzj%2Fv1.0.1%2Fpub%2Findex2_new.html&zoneId=CN31&id=744e2a6324ec5370616241baf4507538&token=dde0ad8e2d204561a40a6099a1ca860a&acToken=9ca17ae2e6ffcda170e2e6eea3d05dbcb7b697d463f4928ab2c15a838a9b86d545a2bc9aa2d14787b9be8dd02af0feaec3b92ab6e98dd3d564ab9085afd04e869a9ba3d55ea79fabb1e25a928e83a3b366fcacee9e&data=%7B%22d%22%3A%22fgM4%5C%5CdnJQVMJ2hyf%5C%5Cwo6NZ0oi1VhqDdgExsgsZ%2Bq1Zifxn4zKE%2Fdv6XKvDI6H5oAshjfXbDLycMdyOHbSuIybTZFdh5SpCno8Gw00CSZqPoex%5C%5C%5C%5CoTV%2BQdw6qO15nw2falO7HfFp%5C%5C%5C%5CrGE%5C%5ChKfabzgKBUOCAZJHz6Md8XO%2BTQUwOMdXJD2aGe9fI6LmwmvCzYoc880ZoKxlF0WIVoAKJK5rz6UM1dkVZ8f8g6%2BNswqCMqWpbAjy%2BBH28U2N2%2BgtvU2g9J9I%2Bkg9XCgl59Q1VHvHTsfgExZ4%2FjKkqmyDMbU5Y8bw0LSt1FfWdaT%2BY%5C%5C00Etay8QyGXh2vcwxwv9cCYLFMKIgA11dTTept6%2FHCSdJpsjUxfrodiJ20xIy4qGFc1L1aOF2zFdLcJJ%2BQSTWTz%5C%5C0xeNylFgU%2F2KAy0U6r8EJ5Mdl%5C%5CIzEtDEENsGa%2BTxF%2BhMPVpaQ2vtH6VRltGypPOD6D7BoveJ%2Bn%5C%5CM%2F1Kzud2uAN%2FXor2%2FDAhXQ%5C%5CmJJP85St7DX8P2t%2BKQi%5C%5C%5C%5CgG0D1Zw8EmGCrHbA6iafOc8P75MoWyOeNdyn2JEg6cnUbe%2Bcq%2BnpxddzO%5C%5CIxIyA0MWy4H86QbECRQZrOd1OEIcCyeIOVkL9MDU4csq59GJ1lE1%2BBudq1u0WwSrdKuiAiTVb7mkpnOyXFz7kO0XiHMDyU76MS0%2FvmODzu%5C%5CHGPCBOtCVrdH%2FquydS2Zyj1b6dY8bYtPDt1FiWm6iffgq0EAXCG5oCqWtbKA4KfpGKhg5wXuOAs7%2BSn2fVRa1K4DRCms9f9QMpOVvMmJqWuFys7DVVzOjZhodFserpxZziS7h%2FfZP80fXgEHFylVNr8kDEUbx2SEY88ZvDyBUgM8npDrcdolHzNtk%5C%5CqCx%2FWHdpIaxQjjGBmrSt4a%2BXbLi1A33%22%2C%22m%22%3A%22%22%2C%22p%22%3A%22c5I%2Fbb8KvZuzaIWMKby7PaL7JRSFTjch%22%2C%22ext%22%3A%22QC%2BgcDPN8lH1D07bp%2Fx%2FRxAM%2BSr5VQde%22%7D&width=320&type=2&version=2.15.2&cb=eGSYDKVG1FiMDbK9iKj1fBwB5oCm1MXPTfxDqJBx2iINWEOdCNKvh5nijnhQsqe9&extraData=17302254866%40163.com&runEnv=10&callback=__JSONP_d2xsay8_1'

parse_url = urllib.parse.unquote(url)

print(parse_url)


s = 'https://webzjcaptcha.reg.163.com/api/v2/check?' \
    'referer=https://dl.reg.163.com/webzj/v1.0.1/pub/index2_new.html&' \
    'zoneId=CN31&' \
    'id=744e2a6324ec5370616241baf4507538&' \
    'token=dde0ad8e2d204561a40a6099a1ca860a&' \
    'acToken=9ca17ae2e6ffcda170e2e6eea3d05dbcb7b697d463f4928ab2c15a838a9b86d545a2bc9aa2d14787b9be8dd02af0feaec3b92ab6e98dd3d564ab9085afd04e869a9ba3d55ea79fabb1e25a928e83a3b366fcacee9e&' \
    'data={' \
    '   "d":"fgM4\\dnJQVMJ2hyf\\wo6NZ0oi1VhqDdgExsgsZ+q1Zifxn4zKE/dv6XKvDI6H5oAshjfXbDLycMdyOHbSuIybTZFdh5SpCno8Gw00CSZqPoex\\\\oTV+Qdw6qO15nw2falO7HfFp\\\\rGE\\hKfabzgKBUOCAZJHz6Md8XO+TQUwOMdXJD2aGe9fI6LmwmvCzYoc880ZoKxlF0WIVoAKJK5rz6UM1dkVZ8f8g6+NswqCMqWpbAjy+BH28U2N2+gtvU2g9J9I+kg9XCgl59Q1VHvHTsfgExZ4/jKkqmyDMbU5Y8bw0LSt1FfWdaT+Y\\00Etay8QyGXh2vcwxwv9cCYLFMKIgA11dTTept6/HCSdJpsjUxfrodiJ20xIy4qGFc1L1aOF2zFdLcJJ+QSTWTz\\0xeNylFgU/2KAy0U6r8EJ5Mdl\\IzEtDEENsGa+TxF+hMPVpaQ2vtH6VRltGypPOD6D7BoveJ+n\\M/1Kzud2uAN/Xor2/DAhXQ\\mJJP85St7DX8P2t+KQi\\\\gG0D1Zw8EmGCrHbA6iafOc8P75MoWyOeNdyn2JEg6cnUbe+cq+npxddzO\\IxIyA0MWy4H86QbECRQZrOd1OEIcCyeIOVkL9MDU4csq59GJ1lE1+Budq1u0WwSrdKuiAiTVb7mkpnOyXFz7kO0XiHMDyU76MS0/vmODzu\\HGPCBOtCVrdH/quydS2Zyj1b6dY8bYtPDt1FiWm6iffgq0EAXCG5oCqWtbKA4KfpGKhg5wXuOAs7+Sn2fVRa1K4DRCms9f9QMpOVvMmJqWuFys7DVVzOjZhodFserpxZziS7h/fZP80fXgEHFylVNr8kDEUbx2SEY88ZvDyBUgM8npDrcdolHzNtk\\qCx/WHdpIaxQjjGBmrSt4a+XbLi1A33",' \
    '   "m":"",' \
    '   "p":"c5I/bb8KvZuzaIWMKby7PaL7JRSFTjch",' \
    '   "ext":"QC+gcDPN8lH1D07bp/x/RxAM+Sr5VQde"' \
    '}&' \
    'width=320&' \
    'type=2&' \
    'version=2.15.2&' \
    'cb=eGSYDKVG1FiMDbK9iKj1fBwB5oCm1MXPTfxDqJBx2iINWEOdCNKvh5nijnhQsqe9&' \
    'extraData=17302254866@163.com&' \
    'runEnv=10&' \
    'callback=__JSONP_d2xsay8_1'


cookie = '__bid_n=1849fea50c5ce057994207; ' \
         'utid=S8IVoVplupFEkIKlQDo8H9facWf2IDrt; ' \
         'NTES_WEB_FP=16ce384d8478f26482e28557203afe1c; ' \
         'l_yd_s_ccPFClpTB=8F7AD574C145A0CBC2259FC8358E677E00D460E4BA2001887E0EFCBD736258372232D65CE7ADD6F68E724B0956968D385226E15EF307BBB5F44B4FBD72852BA9B778271FE5E094520CD33C89BCCD16883F3F7B897D1CC3F37ACCCD36E8DED46B; ' \
         '_9755xjdesxxd_=32; ' \
         'YD00000710348764%3AWM_NI=2RmNyTHYh6fZ5ySPB52L2rTx9mdbhFJAnK7i6sB8caLPH3wnmYf4DrZ1VtcvTBQ3KLffLEBvvZuIuSGC5pb6dulxuCiqd0udDzbqDPPV7MC6HE7uykMDqqMVmeNpcM2Ualk%3D; ' \
         'YD00000710348764%3AWM_NIKE=9ca17ae2e6ffcda170e2e6eeacd33b83bf8495cd5ab5928ea3c84f978f8e83c85c898dbb90e16ea8998a8ac22af0fea7c3b92af28ea3affc608c87a8d7e552f7a79db1c13ff294fe93d774fbb3ac83eb4e8a9fa2acb663f6ad8ed9e26b909088d4f666af87aad5c77a9aef9a95e27e989e9fd4ca48a6ba84a6c17eb686bbaaf859859dfb91e13ea8aba499f849abafacd1f87088a6ae92c75c948af9aec23e8c9bf996fc618f9cbf92d05eafbb8291e247f28baf8dea37e2a3; ' \
         'YD00000710348764%3AWM_TID=t3wYGT94JkZAUQUEBFLUeaC79OLcWE3C; ' \
         'THE_LAST_LOGIN=17302254866@163.com; ' \
         'gdxidpyhxdE=LDi5%2B63%2FtWfbZGYDszvdJloCuyXz0mEdnpyMOKc4ihMRG9m2a3m4wfhpq4GwrBirndcZnlte3ruxd%2FwPPNxpH9CJ21vbzhoKKTl2utbx4WYc0mpiOXR2stlMnQXWKsyVU7ButlcCVreIHpgKtZkTROOjwUCqHtVgmZ3kqwCMBNhivzuh%3A1678526186079; ' \
         'l_s_ccPFClpTB=8F7AD574C145A0CBC2259FC8358E677E00D460E4BA2001887E0EFCBD73625837ED8A5883794C501473F6328812057638144033D583271A939FB43260479DC9641C331591311A2F5E1EE5BFDFF192C95EA49792832D0DC5B0313115742D3D721C'

# 1678608279.9157236
# 1678608291628.9177
