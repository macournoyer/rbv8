require "node"

class Node
  class Call < Node
    kind :call
    
    def emit
      receiver = shift_node.emit
      func     = shift_lit
      arglist  = shift_node.emit
      generator.call(receiver, func, arglist)
    end
  end
  
  class ArgList < Node
    kind :arglist
    
    def emit
      [shift_node.emit]
    end
  end

  class Lit < Node
    kind :lit
    
    def emit
      generator.lit(shift_lit)
    end
  end
  
  class Str < Lit
    kind :str
  end
  
  class Const < Node
    kind :const
    
    def emit
      shift_lit
    end
  end
end