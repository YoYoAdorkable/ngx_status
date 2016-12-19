(function (L) {
    var _this = null;
    L.Status = L.Status || {};
    _this = L.Status = {
        data: {
        },

        //init: function () {
        //    _this.initEvents();
        //},

        //initEvents: function () {
        //   _this.startStatusMonit();
        //},

        startStatusMonit: function() {
            function infor(){
                $.ajax({
                    url : '/summary',
                    type : 'get',
                    cache: false,
                    data : {},
                    dataType : 'json',
                    success : function(result) {
                        if(result){
                            var tpl = $("#status-tpl").html();
                            var html = juicer(tpl, {
                                status: result
                            });
                            $("#wrapper").html(html);
                        }
                    },
                    error : function() {
                        $("#wrapper").html("something went wrong...");
                    }
                });
            };
            infor();
            setInterval(infor,20000)
        },
        
        init: function () {
            _this.initEvents();
        },

        initEvents: function () {
           _this.startStatusMonit();
        },
        
    };
}(APP));

