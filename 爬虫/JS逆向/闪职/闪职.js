const JSEncrypt = require('node-jsencrypt')

function doLogin(password_old, public_key) {
	var encrypt = new JSEncrypt();
    // RSA算法
	encrypt.setPublicKey(public_key);
	var pass_new = encrypt.encrypt(password_old);
	return pass_new;
}

var public_key = "MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDaP+rYm6rqTMP565UmMU6YXq46KtAN3zwDSO8LNa15p0lJfsaY8jXY7iLsZqQZrGYr2Aayp6hYZy+Q+AMB/VUiSpD9ojPyOQ7r9jsf9jZbTOL4kj6iLZn37fEhp4eLvRgy5EJCyQoFyLCsgLechBTlYl2eA95C3j4ZUFhiV6WFHQIDAQAB";

console.log(doLogin('123456', public_key));
