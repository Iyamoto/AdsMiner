var webpage = require('webpage'),
    fs = require('fs'),
    system = require('system'),
    file,
    nThreads = 2,
    finishedThreads,
    url;

if (system.args.length !== 5) {
    console.log('Usage: save.js <file with URLs> <out folder name> <Timeout> <nThreads>');
    phantom.exit();
}
list_urls = system.args[1];
folder = system.args[2];
nThreads = parseInt(system.args[4]);

phantom.injectJs("md5.js");
var nextStep = function(index) {
    index += nThreads;
    if (index < url.length) {
        savePage(index);
    } else {
        console.log("end of thread");
        finishedThreads += 1;
	console.log("finished threads " + finishedThreads);
        if (finishedThreads == nThreads) {
            console.log("end.");
            phantom.exit();
        }
    }
}
var savePage = function(index) {
    var address = url[index];
    var page = webpage.create();
    page.settings.resourceTimeout = system.args[3];
    page.settings.userAgent = 'Mozilla/5.0 (Windows NT 5.1; rv:27.0) Gecko/20100101 Firefox/27.0';
    page.settings.loadImages = false;
    page.viewportSize = {
        width: 1280,
        height: 1024
    };
    page.onError = undefined;
    console.log("pre-open url: " + address + " index: " + index);
    var file_name = folder + "/" + CryptoJS.MD5(address) + ".html";
    if (fs.exists(file_name)) {
        console.log("file " + file_name + " exist, not retrieving");
        nextStep(index);
	page.close();
    } else {
        //console.log("not exist, retrieving");
        page.open(address, function(status) {
            //console.log("loaded? url: " + address);
            if (status !== 'success') {
                console.log('FAIL to load the address ' + address + '. status: ' + status);
            } else {

                console.log(file_name);
                fs.write(file_name, page.content, 'w');

            }
            nextStep(index);
	    page.close();

            //phantom.exit();
        });
    }

}



var urls = '',
    eol = system.os.name == 'windows' ? "\r\n" : "\n";
urls = fs.read(list_urls);

if (urls) {
    url = urls.split(eol);
    /*for (var i = 0, len = url.length; i < len; i++) {
		console.log(url[i]);
		}*/
}
finishedThreads = 0;
for (var i = 0; i < nThreads; i++) {

    savePage(i);
}
