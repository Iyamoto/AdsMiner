var webpage = require('webpage'),
    fs = require('fs'),
    system = require('system'),
    file,
    nThreads = 2,
    finishedThreads,
    ind,
    url;

if (system.args.length !== 5) {
    console.log('Usage: save.js <file with URLs> <out folder name> <Timeout> <nThreads>');
    phantom.exit();
}
list_urls = system.args[1];
folder = system.args[2];
nThreads = parseInt(system.args[4]);

phantom.injectJs("md5.js");
ind = nThreads - 1;
var nextStep = function() {
    ind++;
    if (ind < (url.length - 1)) {
        savePage(ind, 0);
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

var savePage = function(index, attempt) {
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
    //console.log("pre-open url: " + address + " index: " + index);
    var file_name = folder + separator + CryptoJS.MD5(address) + ".html";
    if (fs.exists(file_name)) {
        console.log("url: " + address +" already loaded, file name: \t" + file_name );
        page.close();
        nextStep();
    } else {
        //console.log("not exist, retrieving");
        page.open(address, function(status) {
            //console.log("loaded? url: " + address);
            if (status !== 'success') {
                console.log('FAIL to load the address ' + address + '. status: ' + status);
		page.close();
		if ( attempt < 3 ) {
		attempt++;
		console.log("retrying url " + address);
		savePage(index, attempt);

		}
            } else {

                console.log("url " + address + " loaded file name: " +file_name);
                fs.write(file_name, page.content, 'w');
                page.close();
            }
            nextStep();

            //phantom.exit();
        });
    }

}


if( !fs.exists(list_urls) ) {
   console.log("input file does not exist!");
   phantom.exit(-2);
}
if( !fs.exists(folder) ) {
   console.log("out folder does not exist!");
   phantom.exit(-3);
}

var urls = '',
    eol = system.os.name == 'windows' ? "\r\n" : "\n";
    separator = system.os.name == 'windows' ? "\\" : "/";
urls = fs.read(list_urls);

if (urls) {
    url = urls.split(eol);
    /*for (var i = 0, len = url.length; i < len; i++) {
		console.log(url[i]);
		}*/
}
if(!url) {
   console.log("url list not defined");
   phantom.exit(-4);
}
finishedThreads = 0;
for (i = 0; i < nThreads; i++) {

    savePage(i);
}
