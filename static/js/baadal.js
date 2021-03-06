var baadalApp = Object();
baadalApp.serialize = function (temp) {
  var obj = {};
  for (var i in temp) {
    var curr = temp[i];
    obj[curr.name] = curr.value;
  }
  return obj;
};

baadalApp.generateTicketLink = function(error) {
  console.log('http://127.0.0.1:8000/admin/default/ticket/' + error.split(' ')[1]);
};

baadalApp.ipArrayToString = function(data, usebr) {
  if (typeof data == 'string') return data;
  var arr = [];
  for (var i = data.length - 1; i>=0; i--) {
    var str = '';
    var keys = Object.keys(data[i]);
    for (var j = keys.length - 1; j >= 0; j--) {
      str += keys[j] + ':' + data[i][keys[j]] + ' ';
    }
    arr.push(str);
  }
  return arr.join(usebr ? '<br>' : '\n');
};

if (Handlebars) {
  Handlebars.registerHelper('ifCond', function (v1, operator, v2, options) {
    switch (operator) {
      case '==':
        return (v1 == v2) ? options.fn(this) : options.inverse(this);
      case '===':
        return (v1 === v2) ? options.fn(this) : options.inverse(this);
      case '<':
        return (v1 < v2) ? options.fn(this) : options.inverse(this);
      case '<=':
        return (v1 <= v2) ? options.fn(this) : options.inverse(this);
      case '>':
        return (v1 > v2) ? options.fn(this) : options.inverse(this);
      case '>=':
        return (v1 >= v2) ? options.fn(this) : options.inverse(this);
      case '&&':
        return (v1 && v2) ? options.fn(this) : options.inverse(this);
      case '||':
        return (v1 || v2) ? options.fn(this) : options.inverse(this);
      default:
        return options.inverse(this);
    }
  });
}

baadalApp.filterArrayObject = function(object, array_name, field_name, value) {
  if (object.hasOwnProperty(array_name)) {
    var array = object[array_name];
    var newarray = [];
    for ( var a in array) {
      if (array[a][field_name] == value) {
        newarray.push(array[a]);
      }
    }
  }
  object[array_name] = newarray;
  return object;
};
