/*
jQWidgets v4.5.4 (2017-June)
Copyright (c) 2011-2017 jQWidgets.
License: http://jqwidgets.com/license/
*/
!function(a){"use strict";a.jqx.jqxWidget("jqxMaskedInput","",{}),a.extend(a.jqx._jqxMaskedInput.prototype,{defineInstance:function(){var b={value:null,mask:"99999",width:null,height:25,textAlign:"left",readOnly:!1,cookies:!1,promptChar:"_",rtl:!1,disabled:!1,events:["valueChanged","textchanged","mousedown","mouseup","keydown","keyup","keypress","change"],aria:{"aria-valuenow":{name:"value",type:"string"},"aria-disabled":{name:"disabled",type:"boolean"}}};return this===a.jqx._jqxMaskedInput.prototype?b:(a.extend(!0,this,b),b)},createInstance:function(){this.render()},render:function(){var b=this;b.element.setAttribute("role","textbox"),b.element.setAttribute("data-role","input");var c=b.element.getAttribute("value");void 0!==c&&""!==c&&null!==c&&(b.value=c),a.jqx.aria(this),a.jqx.aria(this,"aria-multiline",!1),a.jqx.aria(this,"aria-readonly",b.readOnly),b._helpers=[],b._helpers.element=new jqxHelper(b.element),b._helpers.element.addClass(b.toThemeProperty("jqx-input jqx-rc-all jqx-widget jqx-widget-content"));var d=b.element.getAttribute("name");if("div"===b.element.nodeName.toLowerCase()){b.element.innerHTML="";var e=document.createElement("input");e.setAttribute("type","textarea"),e.setAttribute("autocomplete","off"),e.setAttribute("autocorrect","off"),e.setAttribute("autocapitalize","off"),e.setAttribute("spellcheck",!1),e.setAttribute("name",d),b.element.appendChild(e),b.maskbox=a(e),b.disabled&&(b._helpers.element.addClass(b.toThemeProperty("jqx-input-disabled jqx-fill-state-disabled")),e.setAttribute("disabled",!0))}else b.maskbox=b.host,b.element.setAttribute("autocomplete","off"),b.element.setAttribute("autocorrect","off"),b.element.setAttribute("autocapitalize","off"),b.element.setAttribute("spellcheck",!1),b.element.setAttribute("name",d),b.disabled&&(b._helpers.element.addClass(b.toThemeProperty("jqx-input-disabled jqx-fill-state-disabled")),b.element.setAttribute("disabled",!0));if(b._helpers.maskbox=new jqxHelper(b.maskbox[0]),b._helpers.maskbox.addClass(b.toThemeProperty("jqx-reset jqx-input-content jqx-widget-content")),b.rtl&&b._helpers.maskbox.addClass(b.toThemeProperty("jqx-rtl")),b.propertyChangeMap.disabled=function(a,c,d,e){e?a._helpers.maskbox.addClass(b.toThemeProperty("jqx-input-disabled")):a._helpers.maskbox.removeClass(b.toThemeProperty("jqx-input-disabled"))},b.selectedText="",b.self=this,b.oldValue=b._value(),b.items=[],b._initializeLiterals(),b._render(),null!=b.value&&b.inputValue(b.value.toString()),b.host.parents("form").length>0&&b.host.parents("form").on("reset",function(){setTimeout(function(){b.clearValue()},10)}),b.addHandlers(),b.cookies){var f=a.jqx.cookie.cookie("maskedInput."+b.element.id);f&&b.val(f)}},addHandlers:function(){var b=this,c="";this.addHandler(this.maskbox,"blur",function(){b.rtl&&b.maskbox.css("direction","ltr"),b._helpers.maskbox.removeClass(b.toThemeProperty("jqx-fill-state-focus")),b.maskbox.val()!==c&&(b._raiseEvent(7,{type:"keyboard"}),b.cookies&&a.jqx.cookie.cookie("maskedInput."+b.element.id,b.maskbox.val()))}),this.addHandler(this.maskbox,"focus",function(){c=b.maskbox[0].value,b.rtl&&(b.maskbox[0].style.direction="rtl"),b._helpers.element.addClass(b.toThemeProperty("jqx-fill-state-focus"))}),this.addHandler(this.host,"keydown",function(a){var c=b.readOnly,d=a.charCode?a.charCode:a.keyCode?a.keyCode:0;if(c||b.disabled)return!1;var e=b._handleKeyDown(a,d);return e||(a.preventDefault&&a.preventDefault(),a.stopPropagation&&a.stopPropagation()),e}),this.addHandler(this.host,"keyup",function(a){return!(!b.readOnly&&!b.disabled)||(a.preventDefault&&a.preventDefault(),a.stopPropagation&&a.stopPropagation(),!1)}),this.addHandler(this.host,"keypress",function(a){var c=b.readOnly,d=a.charCode?a.charCode:a.keyCode?a.keyCode:0;if(c||b.disabled)return!0;var e=b._handleKeyPress(a,d);return e||(a.preventDefault&&a.preventDefault(),a.stopPropagation&&a.stopPropagation()),e})},focus:function(){try{var a=this;a.maskbox.focus(),setTimeout(function(){a.maskbox.focus()})}catch(a){}},_getString:function(){for(var a="",b=0;b<this.items.length;b++){var c=this.items[b].character;this.items[b].character===this.promptChar&&this.promptChar!==this.items[b].defaultCharacter?a+=this.items[b].defaultCharacter:a+=c}return a},_initializeLiterals:function(){if(void 0===this.mask||null===this.mask)return void(this.items=[]);var a=this,b=function(b,c,d){var e={};return e.character=b,e.regex=c,e.canEdit=d,e.defaultCharacter=a.promptChar,e};this.mask=this.mask.toString();for(var c=this.mask.length,d=0;d<c;d++){var e=this.mask.substring(d,d+1),f="",g=!1;if("["===e){for(var h=d;h<c;h++){if("]"===this.mask.substring(h,h+1))break}f="("+this.mask.substring(d,h+1)+")",d=h,g=!0}"#"===e?(f="(\\d|[+]|[-])",g=!0):"9"===e||"0"===e?(f="\\d",g=!0):"$"===e?g=!1:"/"===e||":"===e?g=!1:"A"===e||"a"===e?(f="\\w",g=!0):"c"===e||"C"===e?(f=".",g=!0):"L"!==e&&"l"!==e||(f="([a-zA-Z])",g=!0);var i={};i=g?b(this.promptChar,f,g):b(e,f,g),this.items.push(i)}},setRegex:function(a,b,c,d){null!==a&&void 0!==a&&null!==b&&void 0!==b&&a<this.items.length&&(this.items[a].regex=b,null!==c&&void 0!==c&&(this.items[a].canEdit=c),null!==d&&void 0!==d&&(this.items[a].defaultCharacter=d))},_match:function(a,b){return new RegExp(b,"i").test(a)},_raiseEvent:function(b,c){var d=this.events[b],e={};e.owner=this;var f=!0,g=new a.Event(d);return g.owner=this,e.value=this.inputValue(),e.text=this.maskedValue(),7===b&&(e.type=c.type,void 0===e.type&&(e.type=null)),g.args=e,(b<2||b>6)&&(f=this.host.trigger(g)),f},_handleKeyPress:function(a,b){return this._isSpecialKey(b,a)},_insertKey:function(a,b){var c,d=this._selection(),e=this;if(d.start>=0&&d.start<this.items.length){var f=String.fromCharCode(a);a>=65&&a<=90&&(b.shiftKey||(f=f.toLowerCase()));for(var g=!1,h=0;h<this.items.length;h++)if(!(h<d.start)){var i=e.items[h];if(i.canEdit){if(e._match(f,i.regex)){if(!g&&d.length>0){for(var j=d.start;j<d.end;j++)e.items[j].canEdit&&(e.items[j].character=e.promptChar);c=e._getString(),e.maskedValue(c),g=!0}i.character=f,c=e._getString(),e.maskedValue(c),d.start<e.items.length&&e._setSelectionStart(h+1);break}break}}}},_deleteSelectedText:function(){var a=this._selection(),b=!1;if(a.start>0||a.length>0){for(var c=a.start;c<a.end;c++)c<this.items.length&&this.items[c].canEdit&&this.items[c].character!==this.promptChar&&(this.items[c].character=this.promptChar,b=!0);var d=this._getString();return this.maskedValue(d),b}},_saveSelectedText:function(){var b=this._selection(),c="";if(b.start>0||b.length>0)for(var d=b.start;d<b.end;d++)this.items[d].canEdit&&(c+=this.items[d].character);if(window.clipboardData)window.clipboardData.setData("Text",c);else{var e=a("<textarea style='position: absolute; left: -1000px; top: -1000px;'/>");e.val(c),a("body").append(e),e.select(),setTimeout(function(){document.designMode="off",e.select(),e.remove()},100)}return c},_pasteSelectedText:function(){var b=this._selection(),c="",d=0,e=b.start,f="",g=this,h=function(a){if(!(a!==g.selectedText&&a.length>0&&(g.selectedText=a,null===g.selectedText||void 0===g.selectedText))){if(b.start>=0||b.length>0)for(var f=b.start;f<g.items.length;f++)g.items[f].canEdit&&d<g.selectedText.length&&(g.items[f].character=g.selectedText[d],d++,e=1+f);c=g._getString(),g.maskedValue(c),e<g.items.length?g._setSelectionStart(e):g._setSelectionStart(g.items.length)}};if(window.clipboardData)f=window.clipboardData.getData("Text"),h(f);else{var i=a("<textarea style='position: absolute; left: -1000px; top: -1000px;'/>");a("body").append(i),i.select(),setTimeout(function(){var a=i.val();h(a),i.remove()},100)}},_handleKeyDown:function(b,c){var d,e,f=this._selection();c>=96&&c<=105&&(c-=48);var g=b.ctrlKey||b.metaKey;if(g&&97===c||g&&65===c)return!0;if(g&&120===c||g&&88===c)return this.selectedText=this._saveSelectedText(b),this._deleteSelectedText(b),!a.jqx.browser.msie;if(g&&99===c||g&&67===c)return this.selectedText=this._saveSelectedText(b),!a.jqx.browser.msie;if(g&&122===c||g&&90===c)return!1;if(g&&118===c||g&&86===c||b.shiftKey&&45===c)return this._pasteSelectedText(),!a.jqx.browser.msie;if(8===c){if(0===f.length)for(e=this.items.length-1;e>=0;e--)if(this.items[e].canEdit&&e<f.end&&this.items[e].character!==this.promptChar){this._setSelection(e,e+1);break}f=this._selection();var h=this._deleteSelectedText();return(f.start>0||f.length>0)&&f.start<=this.items.length&&(h?this._setSelectionStart(f.start):this._setSelectionStart(f.start-1)),!1}if(190===c)for(d=f.start,e=d;e<this.items.length;e++)if("."===this.items[e].character){this._setSelectionStart(e+1);break}if(191===c)for(d=f.start,e=d;e<this.items.length;e++)if("/"===this.items[e].character){this._setSelectionStart(e+1);break}if(189===c)for(d=f.start,e=d;e<this.items.length;e++)if("-"===this.items[e].character){this._setSelectionStart(e+1);break}if(46===c){if(0===f.length)for(e=0;e<this.items.length;e++)if(this.items[e].canEdit&&e>=f.start&&this.items[e].character!==this.promptChar){this._setSelection(e,e+1);break}var i=f;return f=this._selection(),(f.start>=0||f.length>=0)&&f.start<this.items.length&&(f.length<=1?i.end!==f.end?this._setSelectionStart(f.end):this._setSelectionStart(f.end+1):this._setSelectionStart(f.start)),!1}return this._insertKey(c,b),this._isSpecialKey(c,b)},_isSpecialKey:function(a,b){return 189===a||9===a||13===a||35===a||36===a||37===a||39===a||46===a||!!(16===a&&b.shiftKey||b.ctrlKey||b.metaKey)},_selection:function(){var a,b=this.maskbox[0];if("selectionStart"in this.maskbox[0])return a=b.selectionEnd-b.selectionStart,{start:b.selectionStart,end:b.selectionEnd,length:a,text:b.value};var c=document.selection.createRange();if(null==c)return{start:0,end:b.value.length,length:0};var d=this.maskbox[0].createTextRange(),e=d.duplicate();return d.moveToBookmark(c.getBookmark()),e.setEndPoint("EndToStart",d),a=c.text.length,{start:e.text.length,end:e.text.length+c.text.length,length:a,text:c.text}},_setSelection:function(a,b){if("selectionStart"in this.maskbox[0])this.maskbox[0].focus(),this.maskbox[0].setSelectionRange(a,b);else{var c=this.maskbox[0].createTextRange();c.collapse(!0),c.moveEnd("character",b),c.moveStart("character",a),c.select()}},_setSelectionStart:function(a){this._setSelection(a,a)},refresh:function(a){a||this._render()},resize:function(a,b){this.width=a,this.height=b,this.refresh()},_render:function(){var b=parseInt(this.host.css("border-left-width"),10),c=parseInt(this.host.css("border-left-width"),10),d=parseInt(this.host.css("border-left-width"),10),e=parseInt(this.host.css("border-left-width"),10),f=parseInt(this.host.css("height"),10)-d-e,g=parseInt(this.host.css("width"),10)-b-c;null!=this.width&&-1!==this.width.toString().indexOf("px")?g=this.width:void 0===this.width||isNaN(this.width)||(g=this.width),null!=this.height&&-1!==this.height.toString().indexOf("px")?f=this.height:void 0===this.height||isNaN(this.height)||(f=this.height),g=parseInt(g,10),f=parseInt(f,10),this.maskbox[0]!==this.element&&this.maskbox.css({"border-left-width":0,"border-right-width":0,"border-bottom-width":0,"border-top-width":0}),this.maskbox.css("text-align",this.textAlign);var h=this.maskbox.css("font-size");isNaN(f)||this.maskbox.css("height",parseInt(h,10)+4+"px"),isNaN(g)||this.maskbox.css("width",g-2);var i=parseInt(f,10)-2*parseInt(d,10)-2*parseInt(e,10)-parseInt(h,10);if(isNaN(i)&&(i=0),isNaN(f)||this.host.height(f),isNaN(g)||this.host.width(g),this.maskbox[0]!==this.element){var j=i/2;a.jqx.browser.msie&&a.jqx.browser.version<8&&(j=i/4),this.maskbox.css("padding-right","0px"),this.maskbox.css("padding-left","0px"),this.maskbox.css("padding-top",j),this.maskbox.css("padding-bottom",i/2)}this.maskbox[0].value=this._getString(),this.width&&(this.width.toString().indexOf("%")>=0&&(this.element.style.width=this.width),this.height.toString().indexOf("%")>=0&&(this.element.style.height=this.height))},destroy:function(){var b=this;a.jqx.utilities.resize(this.host,null,!0),b.host.remove(),b._helpers=[]},maskedValue:function(a){return void 0===a?this._value():(this.value=a,this._refreshValue(),this.oldValue!==a&&(this._raiseEvent(1,a),this.oldValue=a,this._raiseEvent(0,a)),this)},propertyChangedHandler:function(b,c,d,e){if(void 0!==this.isInitialized&&!1!==this.isInitialized){if("rtl"===c&&(b.rtl?b._helpers.maskbox.addClass(b.toThemeProperty("jqx-rtl")):b._helpers.maskbox.removeClass(b.toThemeProperty("jqx-rtl"))),"value"===c&&(void 0!==e&&null!==e||(e=""),""===e?this.clear():(e=e.toString(),this.inputValue(e)),b._raiseEvent(7,e)),"theme"===c&&a.jqx.utilities.setTheme(d,e,this.host),"disabled"===c&&(e?(b._helpers.maskbox.addClass(b.toThemeProperty("jqx-input-disabled")),b._helpers.element.addClass(b.toThemeProperty("jqx-fill-state-disabled")),b._helpers.maskbox.attr("disabled",!0)):(b._helpers.maskbox.removeClass(this.toThemeProperty("jqx-input-disabled")),b._helpers.element.removeClass(this.toThemeProperty("jqx-fill-state-disabled")),b._helpers.maskbox.attr("disabled",!1)),a.jqx.aria(b,"aria-disabled",e)),"readOnly"===c&&(this.readOnly=e),"promptChar"===c){for(var f=0;f<b.items.length;f++)b.items[f].character===b.promptChar&&(b.items[f].character=e,b.items[f].defaultCharacter=e);b.promptChar=e}"textAlign"===c&&(b.maskbox.css("text-align",e),b.textAlign=e),"mask"===c&&(b.mask=e,b.items=[],b._initializeLiterals(),b.value=b._getString(),b._refreshValue()),"width"===c?(b.width=e,b._render()):"height"===c&&(b.height=e,b._render())}},_value:function(){return this.value},_getEditStringLength:function(){for(var a="",b=0;b<this.items.length;b++)this.items[b].canEdit&&(a+=this.items[b].character);return a.length},_getEditValue:function(){for(var a="",b=0;b<this.items.length;b++)this.items[b].canEdit&&this.items[b].character!==this.promptChar&&(a+=this.items[b].character);return a},parseValue:function(a){if(void 0===a||null===a)return null;for(var b=a.toString(),c="",d=0,e=0;e<b.length;e++)for(var f=b.substring(e,e+1),g=d;g<this.items.length;g++)if(this.items[g].canEdit&&this._match(f,this.items[g].regex)){c+=f,d=g;break}return c},clear:function(){this.clearValue()},clearValue:function(){this.inputValue("",!0)},val:function(a){return void 0!==a&&"object"!=typeof a&&("number"==typeof a&&isFinite(a)&&(a=a.toString()),this.maskedValue(a)),this.maskbox[0].value},inputValue:function(a,b){var c;if(void 0===a||null===a){var d="";for(c=0;c<this.items.length;c++)this.items[c].canEdit&&(d+=this.items[c].character);return d}var e=0;for(a=a.toString(),c=0;c<this.items.length;c++)this.items[c].canEdit&&(this._match(a.substring(e,e+1),this.items[c].regex)?(this.items[c].character=a.substring(e,e+1),e++):b&&(this.items[c].character=this.promptChar,e++));var f=this._getString();return this.maskedValue(f),this.inputValue()},_refreshValue:function(){for(var b=this.maskedValue(),c=0,d=0;d<this.items.length;d++)b.length>c&&(this.items[d].canEdit&&this.items[d].character!==b[c]&&(!this._match(b[c],this.items[d].regex)&&b[c]!==this.promptChar||1!==b[c].length||(this.items[d].character=b[c])),c++);this.value=this._getString(),b=this.value,this.maskbox[0].value=b,a.jqx.aria(this,"aria-valuenow",b)}})}(jqxBaseFramework);

