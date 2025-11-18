--// Load RedzLib UI
local RedzLib = loadstring(game:HttpGet("https://raw.githubusercontent.com/REDzHUB/REDzLIB/main/Source.lua"))()
local Window = RedzLib:MakeWindow({
    Title = "Tho Lnoob Hub | Auto Farm",
    SubTitle = "Blox Fruits",
    SaveFolder = "ThoLnoobHub"
})

local Main = Window:MakeTab({Name = "Main"})
local AutoFarm = false

Main:AddToggle({
    Name = "Bật/Tắt Auto Farm",
    Default = false,
    Callback = function(v)
        AutoFarm = v
    end
})

-----------------------------------------------------
-- Nhân vật cơ bản
-----------------------------------------------------
local player = game.Players.LocalPlayer

local function getChar()
    local c = player.Character or player.CharacterAdded:Wait()
    return c, c:WaitForChild("HumanoidRootPart"), c:WaitForChild("Humanoid")
end

-----------------------------------------------------
-- Kiểm tra Melee (mọi võ)
-----------------------------------------------------
local function isMelee(tool)
    if not tool then return false end
    if tool:FindFirstChild("Handle") and tool:FindFirstChild("Attack") then
        return true
    end
    return false
end

-----------------------------------------------------
-- Tìm quái gần nhất
-----------------------------------------------------
local function getClosestEnemy(hrp)
    local enemies = workspace:FindFirstChild("Enemies")
    if not enemies then return nil end

    local closest, dist = nil, math.huge
    for _, mob in pairs(enemies:GetChildren()) do
        if mob:FindFirstChild("Humanoid") and mob:FindFirstChild("HumanoidRootPart") then
            if mob.Humanoid.Health > 0 then
                local d = (mob.HumanoidRootPart.Position - hrp.Position).Magnitude
                if d < dist then
                    closest = mob
                    dist = d
                end
            end
        end
    end

    return closest
end

-----------------------------------------------------
-- Gom quái
-----------------------------------------------------
local function gatherEnemies(hrp)
    local enemies = workspace:FindFirstChild("Enemies")
    if not enemies then return end

    for _, mob in pairs(enemies:GetChildren()) do
        if mob:FindFirstChild("HumanoidRootPart") and mob:FindFirstChild("Humanoid") and mob.Humanoid.Health > 0 then
            mob.HumanoidRootPart.CFrame = hrp.CFrame * CFrame.new(math.random(-4,4), 0, math.random(-4,4))
        end
    end
end

-----------------------------------------------------
-- Tấn công bằng Melee
-----------------------------------------------------
local function attack()
    local tool = player.Character:FindFirstChildOfClass("Tool")
    if isMelee(tool) then
        tool:Activate()
    end
end

-----------------------------------------------------
-- Vòng lặp Auto Farm
-----------------------------------------------------
task.spawn(function()
    while true do
        if AutoFarm then
            local char, hrp, hum = getChar()
            local enemy = getClosestEnemy(hrp)

            if enemy then
                -- TP đến quái
                hrp.CFrame = enemy.HumanoidRootPart.CFrame * CFrame.new(0, 0, 3)

                -- Gom quái
                gatherEnemies(hrp)

                -- Đánh
                attack()
            end
        end
        task.wait(0.18)
    end
end)
