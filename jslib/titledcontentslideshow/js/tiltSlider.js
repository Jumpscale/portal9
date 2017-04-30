/*!
 * classie - class helper functions
 * from bonzo https://github.com/ded/bonzo
 * 
 * classie.has( elem, 'my-class' ) -> true/false
 * classie.add( elem, 'my-new-class' )
 * classie.remove( elem, 'my-unwanted-class' )
 * classie.toggle( elem, 'my-class' )
 */

/*jshint browser: true, strict: true, undef: true */
/*global define: false */

( function( window ) {

'use strict';

// class helper functions from bonzo https://github.com/ded/bonzo

function classReg( className ) {
  return new RegExp("(^|\\s+)" + className + "(\\s+|$)");
}

// classList support for class management
// altho to be fair, the api sucks because it won't accept multiple classes at once
var hasClass, addClass, removeClass;

if ( 'classList' in document.documentElement ) {
  hasClass = function( elem, c ) {
    return elem.classList.contains( c );
  };
  addClass = function( elem, c ) {
    elem.classList.add( c );
  };
  removeClass = function( elem, c ) {
    elem.classList.remove( c );
  };
}
else {
  hasClass = function( elem, c ) {
    return classReg( c ).test( elem.className );
  };
  addClass = function( elem, c ) {
    if ( !hasClass( elem, c ) ) {
      elem.className = elem.className + ' ' + c;
    }
  };
  removeClass = function( elem, c ) {
    elem.className = elem.className.replace( classReg( c ), ' ' );
  };
}

function toggleClass( elem, c ) {
  var fn = hasClass( elem, c ) ? removeClass : addClass;
  fn( elem, c );
}

var classie = {
  // full names
  hasClass: hasClass,
  addClass: addClass,
  removeClass: removeClass,
  toggleClass: toggleClass,
  // short names
  has: hasClass,
  add: addClass,
  remove: removeClass,
  toggle: toggleClass
};

// transport
if ( typeof define === 'function' && define.amd ) {
  // AMD
  define( classie );
} else {
  // browser global
  window.classie = classie;
}

})( window );

/**
 * tiltSlider.js v1.0.0
 * http://www.codrops.com
 *
 * Licensed under the MIT license.
 * http://www.opensource.org/licenses/mit-license.php
 * 
 * Copyright 2014, Codrops
 * http://www.codrops.com
 */
;( function( window ) {

	'use strict';

	// https://gist.github.com/edankwan/4389601
	Modernizr.addTest('csstransformspreserve3d', function () {
		var prop = Modernizr.prefixed('transformStyle');
		var val = 'preserve-3d';
		var computedStyle;
		if(!prop) return false;

		prop = prop.replace(/([A-Z])/g, function(str,m1){ return '-' + m1.toLowerCase(); }).replace(/^ms-/,'-ms-');

		Modernizr.testStyles('#modernizr{' + prop + ':' + val + ';}', function (el, rule) {
			computedStyle = window.getComputedStyle ? getComputedStyle(el, null).getPropertyValue(prop) : '';
		});

		return (computedStyle === val);
	});

	var support = { 
			animations : Modernizr.cssanimations,
			preserve3d : Modernizr.csstransformspreserve3d,
			transforms3d : Modernizr.csstransforms3d
		},
		isSupported = support.animations && support.preserve3d && support.transforms3d,
		animEndEventNames = {
			'WebkitAnimation' : 'webkitAnimationEnd',
			'OAnimation' : 'oAnimationEnd',
			'msAnimation' : 'MSAnimationEnd',
			'animation' : 'animationend'
		},
		// animation end event name
		animEndEventName = animEndEventNames[ Modernizr.prefixed( 'animation' ) ];

	function extend( a, b ) {
		for( var key in b ) { 
			if( b.hasOwnProperty( key ) ) {
				a[key] = b[key];
			}
		}
		return a;
	}

	function TiltSlider( el, options ) {
		this.el = el;
		// available effects for the animations (animation class names) - when a item comes in / out
		this.animEffectsOut = ['moveUpOut','moveDownOut','slideUpOut','slideDownOut','slideLeftOut','slideRightOut'];
		this.animEffectsIn = ['moveUpIn','moveDownIn','slideUpIn','slideDownIn','slideLeftIn','slideRightIn'];
		// the items
		this.items = this.el.querySelector( 'ol.slides' ).children;
		// total items
		this.itemsCount = this.items.length;
		if( !this.itemsCount ) return;
		// index of the current item
		this.current = 0;
		this.options = extend( {}, this.options );
		extend( this.options, options );
		this._init();
	}

	TiltSlider.prototype.options = {};

	TiltSlider.prototype._init = function() {
		this._addNavigation();
		this._initEvents();
	}

	// add the navigation to the DOM
	TiltSlider.prototype._addNavigation = function() {
		// add nav "dots"
		this.nav = document.createElement( 'nav' )
		var inner = '';
		for( var i = 0; i < this.itemsCount; ++i ) {
			inner += i === 0 ? '<span class="current"></span>' : '<span></span>';
		}
		this.nav.innerHTML = inner;
		this.el.appendChild( this.nav );
		this.navDots = [].slice.call( this.nav.children );
	}

	TiltSlider.prototype._initEvents = function() {
		var self = this;
		// show a new item when clicking the navigation "dots"
		this.navDots.forEach( function( dot, idx ) {
			dot.addEventListener( 'click', function() {
				if( idx !== self.current ) {
					self._showItem( idx );
				}
			} );
		} );
	}

	TiltSlider.prototype._showItem = function( pos ) {
		if( this.isAnimating ) {
			return false;
		}
		this.isAnimating = true;

		classie.removeClass( this.navDots[ this.current ], 'current' );

		var self = this,
			// the current item
			currentItem = this.items[ this.current ];

		this.current = pos;

		// next item to come in
		var nextItem = this.items[ this.current ],
			outEffect = this.animEffectsOut[2],
			inEffect = this.animEffectsIn[2];

		currentItem.setAttribute( 'data-effect-out', outEffect );
		nextItem.setAttribute( 'data-effect-in', inEffect );

		classie.addClass( this.navDots[ this.current ], 'current' );

		var cntAnims = 0,
			// the number of elements that actually animate inside the current item
			animElemsCurrentCount = currentItem.querySelector( '.tiltview' ).children.length, 
			// the number of elements that actually animate inside the next item
			animElemsNextCount = nextItem.querySelector( '.tiltview' ).children.length,
			// keep track of the number of animations that are terminated
			animEndCurrentCnt = 0, animEndNextCnt = 0,
			// check function for the end of each animation
			isFinished = function() {
				++cntAnims;
				if( cntAnims === 2 ) {
					self.isAnimating = false;
				}
			},
			// function for the end of the current item animation
			onEndAnimationCurrentItem = function() {
				++animEndCurrentCnt;
				var endFn = function() {
					classie.removeClass( currentItem, 'hide' );
					classie.removeClass( currentItem, 'current' );
					isFinished();
				};
					
				if( !isSupported ) {
					endFn();
				}
				else if( animEndCurrentCnt === animElemsCurrentCount ) {
					currentItem.removeEventListener( animEndEventName, onEndAnimationCurrentItem );
					endFn();
				}
			},
			// function for the end of the next item animation
			onEndAnimationNextItem = function() {
				++animEndNextCnt;
				var endFn = function() {
					classie.removeClass( nextItem, 'show' );
					classie.addClass( nextItem, 'current' );
					isFinished();
				};

				if( !isSupported ) {
					endFn();
				}
				else if( animEndNextCnt === animElemsNextCount ) {
					nextItem.removeEventListener( animEndEventName, onEndAnimationNextItem );
					endFn();
				}
			};

		classie.addClass( currentItem, 'hide' );
		classie.addClass( nextItem, 'show' );

		if( isSupported ) {
			currentItem.addEventListener( animEndEventName, onEndAnimationCurrentItem );
			nextItem.addEventListener( animEndEventName, onEndAnimationNextItem );
		}
		else {
			onEndAnimationCurrentItem();
			onEndAnimationNextItem();
		}
	}

	// add to global namespace
	window.TiltSlider = TiltSlider;

})( window );
