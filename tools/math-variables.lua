-- Quarto 1.9 leaves var shortcodes in Math nodes as encoded reader tokens.
-- Resolve only math variables, using the same _variables.yml as prose.
local reader_token = "b58fc729%-690b%-4000%-b19f%-365a4093b2ff;([A-Fa-f0-9]+);"
local variable = "{{<%s*var%s+([%w_-]+)%s*>}}"

local function resolve(name)
  local value = quarto.variables.get(name)
  if value == nil or value:match("^%s*$") then
    assert(false, "Missing value for math variable '" .. name .. "' in _variables.yml")
  end
  return value
end

function Math(element)
  element.text = element.text:gsub(reader_token, function(hex)
    local shortcode = hex:gsub("..", function(pair)
      return string.char(tonumber(pair, 16))
    end)
    -- A TeX group adjacent to a shortcode is encoded with it, for example
    -- \frac{{{< var numerator >}}}{{{< var denominator >}}}.
    local resolved, count = shortcode:gsub(variable, resolve)
    if count == 0 then
      assert(false, "Unsupported shortcode in math: " .. shortcode)
    end
    return resolved
  end)
  -- Also support readers that leave the original shortcode text in Math.
  element.text = element.text:gsub(variable, resolve)
  return element
end
