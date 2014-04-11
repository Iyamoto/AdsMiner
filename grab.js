var webpage = require('webpage'),
    fs = require('fs'),
    system = require('system'),
    file,
    n,
    url;

if (system.args.length !== 4) {
	console.log('Usage: save.js <file with URLs> <out folder name> <Timeout>');
	phantom.exit();
}	

list_urls = system.args[1];
folder = system.args[2];

phantom.injectJs("md5.js");
var savePage = function (address) {
	var page = webpage.create();
	page.settings.resourceTimeout = system.args[3];
	page.settings.userAgent = 'Mozilla/5.0 (Windows NT 5.1; rv:27.0) Gecko/20100101 Firefox/27.0';
	page.settings.loadImages = false;
	page.viewportSize = { width: 1280, height: 1024 };
	console.log("pre-open url: " + address );
	page.open(address, function (status) {
			//console.log("loaded? url: " + address);
			if (status !== 'success') {
			console.log('FAIL to load the address');
			} else {

			var file_name = folder + "/" + CryptoJS.MD5(address) + ".html";
			console.log(file_name);
			fs.write(file_name, page.content, 'w');

			}
			n++;
			if( n < url.length) {
			savePage(url[n]);
			}
			else {
			console.log("end");
			phantom.exit();

			}

			//phantom.exit();
			});

}



var urls = '',
    f = null,
    lines = null,
    eol = system.os.name == 'windows' ? "\r\n" : "\n";

try {
	f = fs.open(list_urls, "r");
	urls = f.read();
} catch (e) {
	console.log(e);
}

if (f) {
	f.close();
}

if (urls) {
	url = urls.split(eol);
/*	for (var i = 0, len = url.length; i < len; i++) {
		console.log(url[i]);
	}*/
}

n=0;
savePage(url[n]);

