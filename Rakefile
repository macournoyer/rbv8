task :build => "vm/vm"
task :default => :build

task :clean do
  sh "cd v8 && scons -c"
  rm_rf "v8/obj"
end

file "v8/libv8.a" do
  sh "cd v8 && scons mode=release"
end

file "vm/vm" => "v8/libv8.a" do |f|
  sh "g++ -o #{f.name} -Iv8/include -Lv8 -lv8 -lpthread vm/shell.cc"
end