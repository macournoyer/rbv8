require File.dirname(__FILE__) + "/spec_helper"
require "compiler"

describe "Compiler" do
  it "should call new" do
    Compiler.compile_string("String.new('ohaie')").code.should == %Q{new String("ohaie");}
  end
end