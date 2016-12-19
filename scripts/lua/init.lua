-- http://www.kyne.com.au/~mark/software/lua-cjson.php
cjson = require "cjson"
common = require "common"
cache_status = {"MISS", "BYPASS", "EXPIRED", "STALE", "UPDATING", "REVALIDATED", "HIT"}
local stats = ngx.shared.ngx_stats
ngx.update_time()

-- Geral stats
common.update(stats, common.key({'global', 'start_time'}), ngx.localtime())

--stats:set('start_time', ngx.localtime())
--stats:set('stats_start', ngx.now())
