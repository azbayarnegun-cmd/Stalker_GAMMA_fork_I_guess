local base = '/workspace/scratch/633dfd297ac4/'
local old = base .. 'build/SA_Layered_Pouches_Addon_1.5.3_SquaredAway_3.1.0_VideoConfirmed_r9/gamedata/scripts/zzz_amp_grid.script'
local root = base .. 'build/SA_Layered_Pouches_Addon_1.5.3_SA310_PouchGrid_r11/'
local new = root .. 'gamedata/scripts/zzz_amp_grid.script'
local function read(p)
    local f = assert(io.open(p, 'rb')); local s = f:read('*a'); f:close(); return s
end
local function check_guard(path, id, deferred, expected)
    local s = read(path)
    local a = assert(s:find('function G.restore(cc, list)', 1, true))
    local b = assert(s:find('\nfunction G.our_bag()', a, true))
    local code = s:sub(a, b - 1)
    -- Run the actual restore function through its preconditions. Stop at
    -- Reset before UI rendering: this test is specifically for the guard.
    G = { reflow=function() end, zones=function() return {{}} end,
          capacity=function() return 3, 4 end, claim=function() end }
    local setup = "local SIDE_ID='amp_layers_side'; local writes_layout=function() return true end; local log=function() end; "
    assert(load(setup .. code))()
    local cc = { ID=id, cols=3, deferredInitialized=true, deferred=deferred,
        scroll={GetCurrentScrollPos=function() return 0 end},
        Reset=function() error('REACHED_GRID_RESET') end }
    local ok, result = pcall(G.restore, cc, {})
    local reached = not ok and tostring(result):find('REACHED_GRID_RESET',1,true) ~= nil
    assert(reached == expected, path .. ': unexpected guard result ' .. tostring(result))
end
check_guard(old, 'amp_layers_side', false, false)
check_guard(new, 'amp_layers_side', false, true)
check_guard(new, 'amp_layers_side', true, true)
check_guard(new, 'actor_bag', false, false)
check_guard(new, 'actor_bag', true, false)
print('PASS: original empty-side defect reproduced; r11 reaches grid rebuild; backpack deferral preserved (5 cases)')
for _, name in ipairs({'zzz_amp_grid.script','zzz_amp_layers.script','zzz_armor_mag_pouches.script'}) do
    assert(loadfile(root .. 'gamedata/scripts/' .. name))
end
print('PASS: all three integration scripts parse')
assert(not read(new):find('pouch%-area routed'))
assert(read(root .. 'gamedata/scripts/zzz_amp_layers.script'):find('pcall(grid.restore_layer_view, cc, items)',1,true))
print('PASS: direct side rebuild wired; no r10 autorouting')

local source = read(new)
local function extract(text, name)
    local a = assert(text:find('function ' .. name .. '(', 1, true))
    local b = assert(text:find('\nend', a, true))
    return text:sub(a,b+3)
end
local zone = {x0=1,y0=2,cols=3,rows=3,pouch_id=123}
G = {enabled=true, reflow=function() end, zones=function() return {zone} end,
     capacity=function() return 3,4 end, claim=function() end,
     head_rows=function() return 0 end, zone_allows=function() return true end}
for _, name in ipairs({'G.zone_of','G.fits','G.make_rows','G.take_dead','G.restore'}) do
    assert(load("local SIDE_ID='amp_layers_side'; local writes_layout=function() return true end; local log=function() end; local dbg=function() end; " .. extract(source,name)))()
end
UICellContainer={}
local sota = read(base .. 'work/sota_ui/UI Rework G.A.M.M.A. Style - Sota/gamedata/scripts/utils_ui.script'):gsub('\r\n','\n')
assert(load(extract(sota,'UICellContainer:IsFreeRoom')))()
local cc={ID='amp_layers_side', cols=3,grid={},cell={},deferredInitialized=true,
    scroll={GetCurrentScrollPos=function() return 0 end},
    Reset=function(self) self.grid={} end,
    Grow=function(self) self.grid[#self.grid+1]={} end,
    TakeRoom=function(self,r,c) self.grid[r][c]=false end,
    Scroll_Reinit=function() end, Print=function() end,
    IsFreeRoom=UICellContainer.IsFreeRoom}
assert(G.restore(cc,{}))
assert(#cc.grid==4 and cc:IsFreeRoom(2,1,1,1))
assert(not cc:IsFreeRoom(1,1,1,1))
cc:TakeRoom(2,1)
assert(not cc:IsFreeRoom(2,1,1,1))
print('PASS: actual restore builds empty pouch rows; Sota accepts a free cell, rejects header and occupied cell')
