require 'tools/red'

KERNEL_SRC = FileList["kernel/*.rb"]
EXEC       = "build/rbv8"

task :build => [EXEC, 'kernel:build', 'codegen:build']
task :default => :build

task :clean do
  sh "cd vm/v8 && scons -c"
  rm_rf "vm/v8/obj"
  rm_rf "build"
end

task :spec do
  sh "mspec/bin/mspec ci spec"
end

# == VM

file "vm/v8/libv8.a" do
  sh "cd vm/v8 && scons mode=release"
end

file EXEC => "vm/v8/libv8.a" do |f|
  mkdir_for EXEC
  sh "g++ -o #{f.name} -Ivm/v8/include -Lvm/v8 -lv8 -lpthread vm/shell.cc"
end


# == Kernel

namespace :kernel do
  desc "Compile kernel Ruby files to JavaScript"
  task :build => KERNEL_SRC.ext("js").sub(/^/, "build/")
  
  KERNEL_SRC.each do |rb|
    js = "build/kernel/" + File.basename(rb).ext('js')
    file js => rb do |t|
      mkdir_for js
      File.open(js, 'w') { |f| f << Red.compile(File.read(rb)) }
    end
  end
end


# == CodeGen

namespace :codegen do
  task :build => "codegen/ruby_parser.rb"
  
end

rule '.rb' => '.y' do |t|
  sh "racc -l -t -E -o #{t.name} #{t.source}"
end


# == Utils

def mkdir_for(file)
  mkdir_p File.dirname(file)
end