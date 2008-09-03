require 'json'

OUTPUT_COMPILE_OPTION = {
  :peephole_optimization    => true,
  :inline_const_cache       => false,
  :specialized_instruction  => false,
  :operands_unification     => false,
  :instructions_unification => false,
  :stack_caching            => false,
}

puts "var opcode = " + VM::InstructionSequence.compile_file(ARGV.first, OUTPUT_COMPILE_OPTION).to_a.to_json
