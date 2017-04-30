
(function(mod) {
  if (typeof exports == "object" && typeof module == "object") // CommonJS
    mod(require("../../lib/codemirror"));
  else if (typeof define == "function" && define.amd) // AMD
    define(["../../lib/codemirror"], mod);
  
    mod(CodeMirror);
})(function(CodeMirror) {
  "use strict";

  
  function forEach(arr, f) {
    for (var i = 0, e = arr.length; i < e; ++i) {
      f(arr[i]);
    }
  }

  function arrayContains(arr, item) {
    if (!Array.prototype.indexOf) {
      var i = arr.length;
      while (i--) {
        if (arr[i] === item) {
          return true;
        }
      }
      return false;
    }
    return arr.indexOf(item) != -1;
  }

  function scriptHint(editor, _keywords, getToken) {
    // Find the token at the cursor
    var cur = editor.getCursor();
    var curClone = {};
    var token = getToken(editor, cur);
    if(token.string == "."){
      curClone = { ch: cur.ch -2, line: cur.line }
      // cur.ch = cur.ch -2;
      token = getToken(editor, curClone);
      token.string = token.string + ".";
    }
    var tprop = token;
    // console.log(editor.getCursor());
    // /////////////////////console.log(token);
    if (!/^[\w$_]*$/.test(token.string)) {
        token = tprop = {start: cur.ch, end: cur.ch, string: token.string, state: token.state, fullString: token.fullString,
                         className: token.string == ":" ? "python-type" : null};
    }

    if (!context) var context = [];
    context.push(tprop);
    
      
    var completionList = getCompletions(token, context);
    completionList = completionList.sort();

    return {list: completionList,
            from: CodeMirror.Pos(cur.line, token.start),
            to: CodeMirror.Pos(cur.line, token.end)};
  }

  function pythonHint(editor) {
    return scriptHint(editor, pythonKeywordsU, function (e, cur) {return e.getTokenAt(cur);});
  }
  CodeMirror.registerHelper("hint", "python", pythonHint);

  // var ms1FirstLevel = [  ["mothership1" ,["login", ["login", "password", "cloudspace_name", "location "]] ]  , 
  // ["machine",
  // ["list"], 
  // ["new", ["name", "description", "memsize", "ssdsize" ]], 
  // ["delete", ["name "]]] ];
  
  var ms1FirstLevel = [  
  ["mothership1" ,["login", ["login", "password", "cloudspace_name", "location "]], 
  // shorthand for mothership1
  "ms1" ], 
  ["machine",
    ["list", "l"], 
    ["new", ["name", "description", "memsize", "ssdsize" ], 
    // shorthand for new
    'create', 'c', 'n'], 
    ["delete", ["name"] ,"del"],
    ["start", ["name"]],
    ["snapshot", ["name", "snapshotname"]],
    ["tcpportforward", ["name", "machinetcpport", "pubip", "pubipport"]],
    ["udpportforward", ["name", "machineudpport", "pubip", "pubipport"]],
    ["execssh", ["name", "sshport", "script"]],
    ["setpasswd", ["name", "passwd"]],
    ["execcuisine", ["name", "script"], "cuisine"],
    ["execjs", ["name", "script"], "execjumpscript","js","jumpscript"],
    ["initjs", ["name"], "initjumpscale"],
    ["initjsdebug", ["name"], "initjumpscaledebug"]
    // shorthand for machine
  , 'm'] 
  ];
  // var ms1FirstLevel = {
  //                       "mothership1" : { "login" : {"login": "login", "password":"password", "cloudspace_name": "cloudspace_name", "location": "location" } }
  //                       ,
  //                       "machine" : { "list" : "list", 
  //                                     "new" : {"name": "name", "description":"description", "memsize":"memsize", "ssdsize":"ssdsize" } , 
  //                                     "delete" : {"name": "name"}
  //                                   }
  //                     };
  // console.log(
  // _.find(ms1FirstLevel, function(num){  return num == {"login": "login"} })
  // );




  var pythonKeywords = "and del from not while as elif global or with assert else if pass yield"
+ "break except import print class exec in raise continue finally is return def for lambda try";
  var pythonKeywordsL = pythonKeywords.split(" ");
  var pythonKeywordsU = pythonKeywords.toUpperCase().split(" ");

  var pythonBuiltins = "abs divmod input open staticmethod all enumerate int ord str "
+ "any eval isinstance pow sum basestring execfile issubclass print super"
+ "bin file iter property tuple bool filter len range type"
+ "bytearray float list raw_input unichr callable format locals reduce unicode"
+ "chr frozenset long reload vars classmethod getattr map repr xrange"
+ "cmp globals max reversed zip compile hasattr memoryview round __import__"
+ "complex hash min set apply delattr help next setattr buffer"
+ "dict hex object slice coerce dir id oct sorted intern ";
  var pythonBuiltinsL = pythonBuiltins.split(" ").join("() ").split(" ");
  var pythonBuiltinsU = pythonBuiltins.toUpperCase().split(" ").join("() ").split(" ");

  function getWordAt(fullString, posetion) {
    // ToDo:
        // 1- cover case of special char before word and no space
    var specialCharacters = "[]()!@{}";
    while (fullString[posetion] == " ") posetion--;
    posetion = fullString.lastIndexOf(" ", posetion) + 1;
    var end = fullString.indexOf(" ", posetion);
    if (end == -1) end = fullString.length; // set to length if it was the last word
    var stringWithoutSpecialChar = fullString.substring(posetion, end);
    for (var i = stringWithoutSpecialChar.length - 1; i >= 0; i--) {
        if( specialCharacters.indexOf(stringWithoutSpecialChar[i]) != -1 ){
          var stringWithoutSpecialChar = stringWithoutSpecialChar.replace(stringWithoutSpecialChar[i], '')
        }
      // console.log( s.substring(pos, end).replace(/(<([^>]+)>)/ig, '') );
    };
    return stringWithoutSpecialChar;
  }
  function getCompletions(token, context) {
    var found = [], start = token.string;
    function maybeAdd(str) {
      
      // console.log(str[level]);
      var level;
      var foundString;
      var wordToComplete;
      if(ms1FirstLevel.length > 0){
        // var fullStringo = token.fullString.replace(/(<([^>]+)>)/g," ");

        if(token.start > 0 && token.fullString){
            wordToComplete = getWordAt(token.fullString, token.start);
        }else{
          if(token.stringwithdot){
              wordToComplete = token.stringwithdot;
          }
          else{
              wordToComplete = token.string;
          }
        }
        if(wordToComplete){
          wordToComplete = wordToComplete.split(".");
          // ToDo:
          // 1- on string dots filter and search
          if(wordToComplete.length == 1){
            for(var i = 0; i <= ms1FirstLevel.length -1; i++){
              foundString = _.where(ms1FirstLevel[i], token.string);
               if(foundString.length > 0){
                  if (foundString[0].lastIndexOf(start, 0) == 0 && !arrayContains(found, foundString[0])){
                    found.push(foundString[0]);
                  }
               }
            }
          }
          if(wordToComplete.length == 2){
            for(var i = 0; i <= ms1FirstLevel.length -1; i++){
              foundString = _.where(ms1FirstLevel[i], wordToComplete[0]);
               if(foundString.length > 0){
                  if (!arrayContains(found, foundString[0])){
                    if(wordToComplete[wordToComplete.length - 1] == ""){
                      var ms1seconedLevel = _.map(ms1FirstLevel[i]  , function(item) {
                          if(!arrayContains(found, item[0])){
                            if(Array.isArray(item)){
                              found.push(item[0]);
                            }
                        }
                      });
                    }
                    else{
                      var ms1seconedLevel = _.map(ms1FirstLevel[i]  , function(item) {
                          if(Array.isArray(item)){
                            if(!arrayContains(found, _.where(item, wordToComplete[1])[0]) && _.where(item, wordToComplete[1])[0]){
                                found.push(_.where(item, wordToComplete[1])[0]);
                            }
                        }
                      });
                    }
                  }
               }
            }
          }

          if(wordToComplete.length == 3){
            for(var i = 0; i <= ms1FirstLevel.length -1; i++){
              foundString = _.where(ms1FirstLevel[i], wordToComplete[0]);
               if(foundString.length > 0){
                  if (!arrayContains(found, foundString[0])){
                    if(wordToComplete[wordToComplete.length - 1] == ""){
                      _.map(ms1FirstLevel[i]  , function(item) {
                          var ms1seconedLevel = [];
                          if(!arrayContains(found, item[0])){
                            for (var i = item.length - 1; i >= 0; i--) {
                              if(item[i] == wordToComplete[1]) {
                                if(Array.isArray(item[1])){
                                  ms1seconedLevel.push( item[1] );
                                  var ms1thirdLevel = _.map(ms1seconedLevel[0], function(item) {
                                    if(!arrayContains(found, item)){
                                      found.push(item);
                                    }
                                  });
                                }
                                return;
                              }
                            }
                        }
                      });
                    }
                    else{
                      _.map(ms1FirstLevel[i]  , function(item) {
                          var ms1seconedLevel = [];
                          if(!arrayContains(found, item[0])){
                            for (var i = item.length - 1; i >= 0; i--) {
                              if(item[i] == wordToComplete[1]){
                                if(Array.isArray(item[1])){
                                  ms1seconedLevel.push( item[1] );
                                  if(!arrayContains(found, _.where(ms1seconedLevel[0], wordToComplete[2])[0])){
                                    found.push(_.where(ms1seconedLevel[0], wordToComplete[2])[0]);
                                  }
                              }
                              return;
                            }
                          } 
                        }
                      });
                    }
                  }
               }
            }
          }


        }
    }
    }

    function gatherCompletions(_obj) {
        // forEach(pythonBuiltinsL, maybeAdd);
        // forEach(pythonBuiltinsU, maybeAdd);
        // forEach(pythonKeywordsL, maybeAdd);
        // forEach(pythonKeywordsU, maybeAdd);
        forEach(ms1FirstLevel, maybeAdd);
    }

    if (context) {
      // If this is a property, see if it belongs to some object we can
      // find in the current environment.
      var obj = context.pop(), base;
      if(obj.string[obj.string.length -1] == "."){
        obj.stringwithdot = obj.string;
        obj.string = obj.string.slice(0, -1);
      }
      // if (obj.type == "variable")
          base = obj.string;
      // else if(obj.type == "variable-3")
      //     base = ":" + obj.string;

      while (base != null && context.length)
        base = base[context.pop().string];
      if (base != null) gatherCompletions(base);
    }
    return found;
  }
});
