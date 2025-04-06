console.log('running tester')

function make_notification() {
    var r = new XMLHttpRequest();
    r.open("GET", '/sms/test-make', true);
    r.send();
}