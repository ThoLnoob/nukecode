-- Tho Lnoob Hub - Auto Farm (Dùng đúng Melee đang trang bị)

local Fluent = loadstring(game:HttpGet("https://github.com/dawid-scripts/Fluent/releases/latest/download/main.lua"))()
local Window = Fluent:CreateWindow({
    Title = "Tho Lnoob Hub",
    SubTitle = "Auto Farm",
    Size = UDim2.fromOffset(530, 350),
    Theme = "Dark",
    Acrylic = true
})

-----------------------------------------------------
-- Nút bật/tắt menu (Fluent không dùng Window.Enabled)
-----------------------------------------------------
local MenuVisible = true

local toggleButton = Instance.new("ImageButton")
toggleButton.Parent = game.CoreGui
toggleButton.Position = UDim2.new(0.9, 0, 0.1, 0)
toggleButton.Size = UDim2.new(0, 50, 0, 50)
toggleButton.Image = "rbxassetid://89300403770535"

toggleButton.MouseButton1Click:Connect(function()
    MenuVisible = not MenuVisible
    if MenuVisible then
        Window:Show()
    else
        Window:Hide()
    end
end)

-----------------------------------------------------
-- Tabs
-----------------------------------------------------
local Tabs = {
    Main = Window:AddTab({ Title = "Main Farm", Icon = "home" }),
}

local AutoFarmEnabled = false

Tabs.Main:AddButton({
    Title = "Bật/Tắt Auto Farm",
    Callback = function()
        AutoFarmEnabled = not AutoFarmEnabled
    end
})

-----------------------------------------------------
-- Auto Farm Variables
-----------------------------------------------------
local player = game.Players.LocalPlayer
local vu = game:GetService("VirtualUser")
local enemies = workspace:WaitForChild("Enemies")

-----------------------------------------------------
-- Tự cập nhật nhân vật khi chết
-----------------------------------------------------
local function getChar()
    local c = player.Character or player.CharacterAdded:Wait()
    return c, c:WaitForChild("HumanoidRootPart")
end

-----------------------------------------------------
-- Tìm quái gần nhất
-----------------------------------------------------
local function getClosestEnemy(hrp)
    local closest, dist = nil, math.huge
    for _, mob in pairs(enemies:GetChildren()) do
        if mob:FindFirstChild("HumanoidRootPart") and mob:FindFirstChild("Humanoid") and mob.Humanoid.Health > 0 then
            local mag = (hrp.Position - mob.HumanoidRootPart.Position).Magnitude
            if mag < dist then
                closest, dist = mob, mag
            end
        end
    end
    return closest
end

-----------------------------------------------------
-- Gom quái
-----------------------------------------------------
local function gatherEnemies(hrp)
    for _, mob in pairs(enemies:GetChildren()) do
        if mob:FindFirstChild("HumanoidRootPart") and mob:FindFirstChild("Humanoid") and mob.Humanoid.Health > 0 then
            mob.HumanoidRootPart.CFrame = hrp.CFrame * CFrame.new(math.random(-5, 5), 0, math.random(-5, 5))
        end
    end
end

-----------------------------------------------------
-- Đánh bằng Melee đang trang bị
-----------------------------------------------------
local function attackWithMelee()
    local tool = player.Character:FindFirstChildOfClass("Tool")
    if tool and tool.ToolTip == "Melee" then
        tool:Activate()
    end
end

-----------------------------------------------------
-- AUTO FARM LOOP
-----------------------------------------------------
task.spawn(function()
    while true do
        if AutoFarmEnabled then
            local char, hrp = getChar()
            local enemy = getClosestEnemy(hrp)

            if enemy then
                hrp.CFrame = enemy.HumanoidRootPart.CFrame * CFrame.new(0, 0, 3)
                gatherEnemies(hrp)
                attackWithMelee()
            end
        end
        task.wait(0.3)
    end
end)
