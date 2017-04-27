local turbo = require 'turbo'

local handler = class("handler", turbo.web.RequestHandler)
function handler:post()
    local q = self:get_argument("q" )
    local body = self.request.body
    self:write({
        query=q,
        body=body
    })
    self:set_status(200)
end
local handler2 = class("handler2", turbo.web.RequestHandler)
function handler2:post(a1)
    local q = self:get_argument("q" )
    local body = self.request.body
    self:write({
        query=q,
        parg=a1,
        body=body
    })
    self:set_status(200)
end

local app = turbo.web.Application:new({
        -- {"/", handler},
        {"/test/(.*)", handler2}
})
app:listen(8080,"0.0.0.0")
turbo.ioloop.instance():start()