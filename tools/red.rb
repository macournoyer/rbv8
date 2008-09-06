require 'rubygems'
require 'red'
require 'red/executable'

module Red
  def compile(source)
    hush_warnings { source.string_to_node }.compile_node
  end
end