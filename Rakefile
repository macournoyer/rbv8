task :build do
  sh "cd v8 && scons mode=release sample sample=shell"
end
task :default => :build

task :clean do
  rm_f ".opcode.js"
  sh "cd v8 && scons -c sample sample=shell"
  rm_rf "v8/obj"
end

task :test do
  sh "bin/rbv8 sample/concat.rb"
  sh "bin/rbv8 sample/fib.rb"
end