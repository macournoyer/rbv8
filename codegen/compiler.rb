require "ruby_parser"
require "nodes"
require "js_generator"

class Compiler
  class CompiledCode
    attr_reader :code, :filename
    
    def initialize(code, filename)
      @code = code
      @filename = filename
    end
  end
  
  def self.compile_string(string, filename="(eval)", line=1)
    sexp = RubyParser.new.parse(string)
    node = new(JSGenerator).build_node(sexp)
    CompiledCode.new(node.emit, filename)
  end
  
  attr_reader :generator
  
  def initialize(generator)
    @generator = generator.new
  end
  
  def build_node(sexp)
    Node.for(sexp, self)
  end
end