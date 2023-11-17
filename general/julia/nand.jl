function ¬(x)
    x ⊼ x
end


function ∧(x, y)
    ¬(x ⊼ y)
end


function ∨(x, y)
   ¬(¬x ∧ ¬y)
end


⊻(x,y) = (x ⊼ y) ∧ (x ∨ y)


function bool_to_bit(B)
    return B ? 1 : 0
end


function half_adder(b₁, b₂)
    sum =  b₁ ⊻ b₂
    carry = b₁ ∧ b₂
    result = [sum, carry]
end 


function full_adder(b₁, b₂, cᵢ)
    sum₁, carry₁ = half_adder(b₁, b₂)
    sum, carry₂ = half_adder(cᵢ, sum₁)
    carry = carry₁ ∨ carry₂
    result = [sum, carry]
end


function add(bit_num₁::Array{Bool}, bit_num₂::Array{Bool})
    
