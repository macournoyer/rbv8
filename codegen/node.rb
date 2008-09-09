class Node
  Mapping = {}
  
  def self.kind(name)
    Mapping[name] = self
  end
  
  def self.for(sexp, compiler)
    name = sexp.shift
    node = (Mapping[name] || raise("Unknown node: #{name}")).new(sexp)
    node.compiler = compiler
    node
  end
  
  attr_reader :sexp
  attr_accessor :compiler
  
  def initialize(sexp)
    @sexp = sexp.dup
  end
  
  def generator
    @compiler.generator
  end
  
  def shift_lit
    sexp.shift
  end

  def shift_node
    Node.for(sexp.shift, compiler)
  end
end