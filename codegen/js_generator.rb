class Compiler
  class JSGenerator
    def call(receiver, func, args)
      if func == :new
        new_call(receiver, func, args)
      else
        "#{receiver}.#{func}(#{args.join(", ")});"
      end
    end
    
    def new_call(receiver, func, args)
      "new #{receiver}(#{args.join(", ")});"
    end
    
    def lit(value)
      value.is_a?(Fixnum) ? value : %Q{"#{value}"}
    end
  end
end