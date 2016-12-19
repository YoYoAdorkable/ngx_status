----
local stats = ngx.shared.ngx_stats;
local keys = stats:get_keys()

---- 将字典中每个key的值重置为0
for k,v in pairs(keys)do
    stats:set(v, 0)
end
