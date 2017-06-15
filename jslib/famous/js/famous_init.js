
define('app/FooterView', function(require, exports, module) {
    var ImageSurface = require('famous/surfaces/ImageSurface');
    var Modifier     = require('famous/core/Modifier');
    var Transform    = require('famous/core/Transform');
    var View         = require('famous/core/View');

    function FooterView() {
        View.apply(this, arguments);
        _createFooter.call(this);
    }

    FooterView.prototype = Object.create(View.prototype);
    FooterView.prototype.constructor = FooterView;

    FooterView.DEFAULT_OPTIONS = {};

    function _createFooter() {
        var footerSurface = new ImageSurface({
            size: [23, 35],
            content: "Footer",
            properties: {
                fontSize: '16px',
                right: "42%",
                top: "15px"
            },
        });

        footerSurface.setContent('/jslib/famous/img/arrows/right-arrow-2.png');

        footerSurface.pipe(this._eventOutput);

        this.add(footerSurface);
    }

    module.exports = FooterView;
});

define('app/HeaderView', function(require, exports, module) {
    var ImageSurface = require('famous/surfaces/ImageSurface');
    var Modifier     = require('famous/core/Modifier');
    var Transform    = require('famous/core/Transform');
    var View         = require('famous/core/View');

    function HeaderView() {
        View.apply(this, arguments);
        _createHeader.call(this);
    }

    HeaderView.prototype = Object.create(View.prototype);
    HeaderView.prototype.constructor = HeaderView;

    HeaderView.DEFAULT_OPTIONS = {};

    function _createHeader() {
        var headerSurface = new ImageSurface({
            size: [23, 35],
            content: "Header",
            classes: ["header"],
            properties: {
                fontSize: '16px',
                bottom: '-15px',
                left: '42%'
            }
        });

        headerSurface.setContent('/jslib/famous/img/arrows/left-arrow-2.png');

        var modifier = new Modifier({
            origin: [0, 0],
            transform: Transform.translate(0, 0, 0)
        });

        headerSurface.pipe(this._eventOutput);

        this.add(modifier).add(headerSurface);
    }

    module.exports = HeaderView;
});
define('app/ContentView', function(require, exports, module) {
    var Surface                 = require('famous/core/Surface');
    var Modifier                = require('famous/core/Modifier');
    var Transform               = require('famous/core/Transform');
    var TouchSync               = require('famous/inputs/TouchSync');
    var GenericSync             = require('famous/inputs/GenericSync');
    var View                    = require('famous/core/View');
    var Transitionable          = require('famous/transitions/Transitionable');
    var TransitionableTransform = require('famous/transitions/TransitionableTransform');
    
    var PageView  = require('app/PageView');
    var templates = require('app/templates');

    function ContentView() {
        View.apply(this, arguments);
        _createPages.call(this);
    }

    ContentView.prototype = Object.create(View.prototype);
    ContentView.prototype.constructor = ContentView;

    ContentView.DEFAULT_OPTIONS = {};

    function _createPages() {
        this.pages = [];
        this.mods = [];
        this.currentPageIndex = 0;

        for (var key in templates) {
            this.pages.push(new PageView({
                content: templates[key]
            }));
        }

        var zIndex = this.pages.length;

        for (var x = 0; x < this.pages.length; x++) {
            this.mods.push(new Modifier({
                origin: [0, 0]
            }));

            this._add(this.mods[x]).add(this.pages[x]);

            this.pages[x].on('nextPage', function() {
                this._eventOutput.emit('nextPage');
            }.bind(this));

            // Gets event from slide transfers rotation to previous slide.
            this.pages[x].on('rotatePrevious', function(data) {
                if (this.currentPageIndex > 0) {
                    this.pages[this.currentPageIndex - 1].rotate(-data.radians);
                }

            }.bind(this));

            // Determines whether the previous slide will become current page or not
            this.pages[x].on('touchEndPrevious', function(data) {
                if (this.currentPageIndex > 0) {
                    this.pages[this.currentPageIndex - 1]._eventOutput.emit('end', data);
                    this._eventOutput.emit('prevPage');
                }
            }.bind(this));

            // Sets the zIndex so the page are stacked properly
            this.pages[x].setZIndex(zIndex);
            zIndex--;

            // Last flag disables page from turning.
            if (x == this.pages.length - 1) {
                this.pages[x].setOptions({
                    last: true,
                    classes: ["page", "last"]
                });
            }
        }

        /**
         * Event handler for a nextPage event. Increments pageIndex
         * @return {[type]} [description]
         */
        this.on('nextPage', function() {
            if (this.currentPageIndex < this.pages.length - 1) {
                this.currentPageIndex++;
            }
        }.bind(this));

        /**
         * Event handler for a prevPage event. Increments pageIndex
         * @return {[type]} [description]
         */
        this.on('prevPage', function() {
            if (this.currentPageIndex > 0) {
                this.currentPageIndex--;
            }
        }.bind(this));
    }

    /**
     * Manually triggers next page
     * @return {[type]} [description]
     */
    ContentView.prototype.nextPage = function() {
        if (this.currentPageIndex < this.pages.length - 1) {
            this.pages[this.currentPageIndex].turn();
            this._eventOutput.emit('nextPage');
        } else {
            this.pages[this.currentPageIndex].hop();
        }
    }

    /**
     * Manually triggers previous page
     * @return {[type]} [description]
     */
    ContentView.prototype.prevPage = function() {
        if (this.currentPageIndex > 0) {
            this._eventOutput.emit('prevPage');
            this.pages[this.currentPageIndex].turnBack();
        }
    }

    module.exports = ContentView;
});
define('app/AppView', function(require, exports, module) {
    var Surface            = require('famous/core/Surface');
    var Modifier           = require('famous/core/Modifier');
    var Transform          = require('famous/core/Transform');
    var View               = require('famous/core/View');
    var HeaderFooterLayout = require('famous/views/HeaderFooterLayout');

    var HeaderView  = require('app/HeaderView');
    var FooterView  = require('app/FooterView');
    var ContentView = require('app/ContentView');

    function AppView() {
        View.apply(this, arguments);
        _createLayoutView.call(this);
    }

    AppView.prototype = Object.create(View.prototype);
    AppView.prototype.constructor = AppView;

    AppView.DEFAULT_OPTIONS = {};

    function _createLayoutView() {
        this.mainLayout = new HeaderFooterLayout();

        this.headerView = new HeaderView();
        this.contentView = new ContentView();
        this.footerView = new FooterView();

        this.mainLayout.header.add(this.headerView); // attach header
        this.mainLayout.content.add(this.contentView);
        this.mainLayout.footer.add(this.footerView); // attach footer

        this.footerView.on('click', function() {
            this.contentView.nextPage();
        }.bind(this));

        this.headerView.on('click', function() {
            this.contentView.prevPage();
        }.bind(this));
        
        this.add(this.mainLayout)
    }

    module.exports = AppView;
});

define('app/PageView', function(require, exports, module) {
    var Surface = require('famous/core/Surface');
    var VideoSurface = require('famous/surfaces/VideoSurface');
    var ImageSurface = require('famous/surfaces/ImageSurface');

    var Modifier = require('famous/core/Modifier');
    var Transform = require('famous/core/Transform');
    var GenericSync = require('famous/inputs/GenericSync');
    var MouseSync = require('famous/inputs/MouseSync');
    var TouchSync = require('famous/inputs/TouchSync');
    var View = require('famous/core/View');
    var Transitionable = require('famous/transitions/Transitionable');
    var TransitionableTransform = require('famous/transitions/TransitionableTransform');
    var Easing = require('famous/transitions/Easing');

    GenericSync.register({mouse: MouseSync});
    GenericSync.register({touch: TouchSync});

    function PageView() {
        View.apply(this, arguments);
        _createPage.call(this);
    }

    PageView.prototype = Object.create(View.prototype);
    PageView.prototype.constructor = PageView;

    PageView.DEFAULT_OPTIONS = {
        last: false
    };

    function _createPage() {
        this.originMod = new Modifier({
            origin: [0, 0]
        });
        this.pageSurface = new Surface({
            size: [undefined, undefined],
            content: this.options.content,
            classes: ["page"],
            properties: {
                backgroundColor: '#111111',
                fontSize: '16px'
            }
        });

        var modifier = new Modifier({
            transform: Transform.rotateY(0)
        });

        this._add(this.originMod).add(this.pageSurface);

        this.position = 0;

        var sync = new GenericSync(['mouse', 'touch'], {
            direction: GenericSync.DIRECTION_X
        })

        this.pageSurface.pipe(sync);

        sync.on('start', function(data) {
            this.touchJustStarted = true;
        }.bind(this));

        sync.on('update', function(data) {
            var edge = window.innerWidth - (this.pageSurface.getSize()[0])

            if (this.touchJustStarted) {
                if (data.position >= 0 && data.velocity >= 0) {
                    this.rotatePrevious = true;
                } else {
                    this.rotatePrevious = false;
                }
                this.touchJustStarted = false;
            }

            if (!this.rotatePrevious) {
                if (data.position > edge) {
                    this.position = edge;
                } else if (data.position >= 0) {

                    this.position = 0;

                } else {
                    this.position = data.position;
                }

                // Converts position in pixels to degrees and then to radians. 
                var deg = (60 * Math.abs(this.position)) / window.innerWidth;
                var radians = -Math.floor(deg) * (Math.PI / 180); // Negative to flip forward
                this.rotate(radians);

            } else { // Previous Page Rotate
                this.position = data.position;

                var prevDeg = 120 - (180 * Math.abs(-data.position)) / window.innerWidth;
                var prevRadians = Math.floor(prevDeg) * (Math.PI / 180); // Negative to flip forward
                this._eventOutput.emit('rotatePrevious', {
                    radians: prevRadians
                });
            }
        }.bind(this));

        sync.on('end', function(data) {
            if (this.rotatePrevious) {
                this._eventOutput.emit('touchEndPrevious', data);
            } else {
                if (data.velocity.toFixed(2) < 0 && !this.options.last) {
                    this.turn();
                    this._eventOutput.emit('nextPage');
                } else {
                    this.turnBack();
                }
            }

            this.position = 0;
        }.bind(this));

        // End event for touchEndPrevious. @todo make this clearer.
        this.on('end', function(data) {
            if (data.velocity.toFixed(2) < 0 && !this.options.last) {
                this.turn();
                this._eventOutput.emit('nextPage');
            } else {
                this.turnBack();
            }

            this.position = 0;
        }.bind(this));
    }

    PageView.prototype.setZIndex = function(index) {
        this.pageSurface.setProperties({
            zIndex: index
        });
    }

    PageView.prototype.setDisplay = function(display) {
        this.pageSurface.setProperties({
            display: display
        });
    }

    PageView.prototype.rotate = function(radians) {
        this.originMod.setTransform(Transform.rotateY(radians));
    }

    PageView.prototype.turn = function() {
        this.originMod.setTransform(Transform.rotateY(-2), {
            duration: 800,
            curve: 'easeIn'
            // curve: "easeOutBounce"
            
        });
    }

    /**
     * Page half jump animation for page that can't turn.
     * @return {[type]} [description]
     */
    PageView.prototype.hop = function() {
        this.originMod.setTransform(
            Transform.rotateY(-.3), {
                duration: 300,
                curve: 'easeIn'
            }, function() {
                this.originMod.setTransform(Transform.rotateY(0), {
                    duration: 300,
                    curve: 'easeIn'
                });
            }.bind(this));
    }

    PageView.prototype.turnBack = function() {
        this.originMod.setTransform(Transform.rotateY(0), {
            duration: 800,
            curve: 'easeIn'
        });

        this.position = 0;
    }

    module.exports = PageView;
});

define('famous_init', function(require, exports, module) {
    var Engine = require('famous/core/Engine');
    
    var Modifier        = require('famous/core/Modifier');
    var Transform       = require('famous/core/Transform');

    var AppView = require('app/AppView');
    var destElement = document.getElementById("famous-container");
    var mainContext = Engine.createContext(destElement);  
    var appView = new AppView();

    
    mainContext.setPerspective(1000);
    mainContext.add(appView);

});
