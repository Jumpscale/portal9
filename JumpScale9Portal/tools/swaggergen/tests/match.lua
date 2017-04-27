local pattern = {
    '/pets',
    '/pets/(^%w$)'
}
local path = {
    '/pets',
    '/pets/',
    '/pets/12'
}
for _,pat in pairs(pattern) do
    for k,v in pairs(path) do
        print('pattern:' .. pat)
        print('path:' .. v)
        local match = {v:match(pat)}
        if #match > 0 then
           print('found')
        else
           print('not found')
        end
    end
end