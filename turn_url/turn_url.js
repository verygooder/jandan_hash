var crypto = require('crypto');
var atob = require('atob');
var fs = require('fs');

function md5(string) {
    return crypto.createHash('md5').update(string).digest('hex');
}


function b64decode(string) {
    return atob(string)
}


function chr(a) {
    return String.fromCharCode(a);
}


function ord(a) {
    return a.charCodeAt()
}

function time() {
  var a = new Date().getTime();
  return parseInt(a / 1000)
}


var turn_url = function (m, r, d) {
  var e = 'DECODE';
  var r = r ? r : '';
  var d = d ? d : 0;
  var q = 4;
  r = md5(r);
  var o = md5(r.substr(0, 16));
  var n = md5(r.substr(16, 16));
  if (q) {
    if (e == 'DECODE') {
      var l = m.substr(0, q)
    }
  } else {
    var l = ''
  }
  var c = o + md5(o + l);
  var k;
  if (e == 'DECODE') {
    m = m.substr(q);
    k = b64decode(m)
  }
  var h = new Array(256);
  for (var g = 0; g < 256; g++) {
    h[g] = g
  }
  var b = new Array();
  for (var g = 0; g < 256; g++) {
    b[g] = c.charCodeAt(g % c.length)
  }
  for (var f = g = 0; g < 256; g++) {
    f = (f + h[g] + b[g]) % 256;
    tmp = h[g];
    h[g] = h[f];
    h[f] = tmp
  }
  var t = '';
  k = k.split('');
  for (var p = f = g = 0; g < k.length; g++) {
    p = (p + 1) % 256;
    f = (f + h[p]) % 256;
    tmp = h[p];
    h[p] = h[f];
    h[f] = tmp;
    t += chr(ord(k[g]) ^ (h[(h[p] + h[f]) % 256]))
  }
  if (e == 'DECODE') {
    if ((t.substr(0, 10) == 0 || t.substr(0, 10) - time() > 0) && t.substr(10, 16) == md5(t.substr(26) + n).substr(0, 16)) {
      t = t.substr(26)
    } else {
      t = ''
    }
  }
  t = t.replace(/(\/\/\w+\.sinaimg\.cn\/)(\w+)(\/.+\.(gif|jpg|jpeg))/, '$1large$3')
  return t
};

/*
function data_oper() {
  var filename = 'hashs';
  var data = fs.readFileSync(filename, 'utf-8');
  var array = data.split('\n');
  var key = 'Dmri43T4ZBhWf6E0HKDzc2FWFqshQgJt';
  var result_array = new Array();
  for (var line of array) {
    url = turn_url(line, key);
    result_array.push(url);
  }
  var result = result_array.join('\n');
  fs.writeFileSync('tmp', result);
  return result;
}


var result = data_oper();
console.log(result);
*/

var hash = process.argv[2];
var key = 'Dmri43T4ZBhWf6E0HKDzc2FWFqshQgJt';
var result = turn_url(hash, key);
console.log(result);